import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO

from ..common.Judge import Judge
from ..common.Lexicon import Lexicon

from stable_baselines3.common.env_checker import check_env
from random import randint
import time

class BBEnv(gym.Env):
    """
    Custom Gym environment for a reinforcement learning task involving permutations of letters on cubes. This environment uses a delayed reward system.
    The environment rewards the agent based on the number of valid words formed by the letters on the cubes.
    """

    def __init__(self, cubes: int, words_list: list, alphabet: list, max_episode_steps=500):
        """
        Initialize the environment.

        Args:
            cubes (int): Number of cubes.
            words_list (list): List of valid words.
            alphabet (list): List of letters in the alphabet.
            max_episode_steps (int): Maximum number of steps per episode.
        """
        super().__init__()

        # Base permutation as a string (hardcoded for 6 cubes)
        self.base = 'eeeaarroottiissllnnudcpmhygbfwkvzxjq'

        # Number of cubes
        self.cubes = cubes

        # Judge object to count valid words
        self.judge = Judge(alphabet, words_list)

        # List of all valid words
        self.words_list = words_list

        # List of letters in the alphabet
        self.alphabet = alphabet

        # Observation space: 26 options per cube side
        self.observation_space = spaces.MultiDiscrete(np.array([26 for _ in range(cubes * 6)]))

        # Action space: 180 possible swaps
        self.action_space = spaces.Discrete(180)

        # Reward range
        self.reward_range = (-1, 1)

        # Maximum number of steps per episode
        self.max_episode_steps = max_episode_steps

        # Create the list of possible swaps
        self.create_swaps_list()

    def random_permutation(self):
        """
        Creates a random permutation of the base string.

        Returns:
            list: Randomly permuted list of letters.
        """
        permutation = list(self.base)
        for i in range(len(permutation)):
            j = randint(0, len(permutation) - 1)
            permutation[i], permutation[j] = permutation[j], permutation[i]
        return permutation

    def create_swaps_list(self):
        """
        Generates a list of 2-item tuples containing pairs of indices to be swapped.
        The first 90 items are for swaps within cubes, and the other 90 are for swaps within colors.
        """
        self.swaps = [None] * 180
        count = 0
        for i in range(self.cubes):
            for j in range(self.cubes - 1):
                for k in range(j + 1, self.cubes):
                    # Swaps within a cube
                    a, b = (6 * i + j), (6 * i + k)

                    # Swaps within colors
                    x, y = (6 * j + i), (6 * k + i)

                    self.swaps[count], self.swaps[count + 90] = (a, b), (x, y)
                    count += 1

    def reset(self, seed=None):
        """
        Resets the environment to an initial state and returns an initial observation.

        Args:
            seed (int, optional): Random seed.

        Returns:
            tuple: Initial observation and info dictionary.
        """
        self.permutation = self.random_permutation()
        self.visited = []
        mono, rainbow = self.judge.count_words(self.permutation)
        self.base_wc = mono + rainbow
        self.current_step = 0

        observation = np.array([self.alphabet.index(letter) for letter in self.permutation])
        info = {'inf': 'nothing'}
        self.episode_root = {'wc': self.base_wc, 'permutation': ''.join(self.permutation)}
        return observation, info

    def step(self, action):
        """
        Executes one time step within the environment.

        Args:
            action (int): The action to be executed.

        Returns:
            tuple: Observation, reward, terminated, truncated, and info dictionary.
        """
        self.current_step += 1

        a, b = self.swaps[action]

        # Swap the letters at indices a and b
        self.permutation[a], self.permutation[b] = self.permutation[b], self.permutation[a]

        mono, rainbow = self.judge.count_words(self.permutation)
        wc = mono + rainbow

        observation = np.array([self.alphabet.index(letter) for letter in self.permutation])

        reward = 0.0
        terminated = False

        if self.current_step >= self.max_episode_steps:
            difference = wc - self.base_wc
            reward = difference / 1000
            terminated = True

        truncated = False
        info = {'sum': wc}

        return observation, reward, terminated, truncated, info
