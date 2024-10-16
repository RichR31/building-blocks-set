import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO

from ..common.Judge import Judge
from ..common.Lexicon import Lexicon

from stable_baselines3.common.env_checker import check_env
from random import randint

class BBEnv(gym.Env):
    """
    A custom OpenAI Gym environment for a reinforcement learning task involving permutations of letters on cubes, that uses the immediate reward system.
    Attributes:
    ----------
    base : str
        A hardcoded base permutation string, which is currently set to work for 6 cubes.
    cubes : int
        The number of cubes in the environment.
    judge : Judge
        An instance of the Judge class used to evaluate word counts.
    words_list : list
        A list containing all the words to be used in the environment.
    alphabet : list
        A list containing the alphabet.
    observation_space : gym.spaces.MultiDiscrete
        The observation space representing the 26 options of letters per cube side.
    action_space : gym.spaces.Discrete
        The action space representing 180 possible swap actions.
    reward_range : tuple
        The range of possible rewards, set to (-1, 1).
    max_episode_steps : int
        The maximum number of steps per episode.
    swaps : list
        A list of 2-item tuples containing pairs of indices to be swapped.
    Methods:
    -------
    __init__(self, cubes:int, words_list:list, alphabet:list, max_epidose_steps=500):
        Initializes the BBEnv environment with the given parameters.
    random_permutation(self):
        Creates a random permutation from the base permutation string.
    create_swaps_list(self):
        Generates a list of 2-item tuples that contain the pairs of indices to be swapped.
    reset(self, seed=None):
        Resets the environment to an initial state and returns the initial observation and info.
    step(self, action):
        Executes one step in the environment by performing the given action.
    """
    
    def __init__(self, cubes:int, words_list:list, alphabet:list, max_epidose_steps=500):
        super().__init__()
        # Base permutation as a string
        # This is hardcoded and will only work for 6 cubes
        self.base = 'eeeaarroottiissllnnudcpmhygbfwkvzxjq'

        # Number of cubes
        self.cubes = cubes

        # A Judge object
        self.judge = Judge(alphabet, words_list)

        # A list with all the words
        self.words_list = words_list

        # A list containing the alphabet
        self.alphabet = alphabet

        # Observation space is [26, 26, 26, ..., 26] representing the 26 options of letters per cube side
        self.observation_space = spaces.MultiDiscrete(np.array([26 for _ in range(cubes * 6)]))

        # Action space is 180 options
        self.action_space = spaces.Discrete(180)

        # Specifying the range for the reward
        self.reward_range = (-1, 1)

        self.max_episode_steps = max_epidose_steps

        self.create_swaps_list()

    def random_permutation(self):
        """
        Creates a random permutation from the base permutation string.
        Returns:
        list: A list representing the random permutation of the base string.
        """
        permutation = list(self.base)

        for i in range(len(permutation)):
            # Get a random index from the permutation list
            j = randint(0, len(permutation) - 1)
            
            # Swap the item at index i with the item at index j
            permutation[i], permutation[j] = permutation[j], permutation[i]
        return permutation  

    def create_swaps_list(self):
        """
        Generates a list of 2-item tuples that contain the pairs of indices to be swapped.
        The first 90 items will be for all the swaps within cubes.
        The other half will be for swaps within colors.
        """
        self.swaps = [None] * 180
        count = 0
        for i in range(self.cubes):
            for j in range(self.cubes - 1):
                for k in range(j + 1, self.cubes):
                    # For swaps within a cube
                    a, b = (6 * i + j), (6 * i + k)

                    # For swaps within colors
                    x, y = (6 * j + i), (6 * k + i)

                    self.swaps[count], self.swaps[count + 90] = (a, b), (x, y)
                    count += 1

    def reset(self, seed=None):
        """
        Resets the environment to an initial state and returns the initial observation and info.
        Parameters:
        seed (int, optional): A seed for the random number generator. Defaults to None.
        Returns:
        tuple: A tuple containing:
            - observation (np.array): An array representing the initial state of the environment.
            - info (dict): A dictionary containing additional information about the initial state, 
              including the 'permutation' key which holds the initial permutation as a string.
        """
        self.permutation = self.random_permutation()
        self.visited = []
        mono, rainbow = self.judge.count_words(self.permutation)
        self.base_wc = mono + rainbow
        self.current_step = 0

        observation = np.array([self.alphabet.index(letter) for letter in self.permutation])
        info = {'permutation': ''.join(self.permutation)}
        self.episode_root = {'wc': self.base_wc, 'permutation': ''.join(self.permutation)}
        return observation, info

    def step(self, action):
        """
        Execute one step in the environment by performing the given action.
        Parameters:
        action (int): The index of the swap action to perform.
        Returns:
        tuple: A tuple containing:
            - observation (np.array): The current state of the environment represented as an array of indices.
            - reward (float): The reward obtained from performing the action.
            - terminated (bool): Whether the episode has terminated.
            - truncated (bool): Whether the episode has been truncated.
            - info (dict): Additional information, including the sum of mono and rainbow words.
        """
        self.current_step += 1

        a, b = self.swaps[action]
        
        # Swap
        self.permutation[a], self.permutation[b] = self.permutation[b], self.permutation[a]

        mono, rainbow = self.judge.count_words(self.permutation)

        current_permutation = ''.join(self.permutation)
        wc = mono + rainbow

        if current_permutation in self.visited:
            reward = -1.0
        else:
            difference = wc - self.base_wc
            reward = difference / 1000

            self.visited.append(current_permutation)
        
        observation = np.array([self.alphabet.index(letter) for letter in self.permutation])

        if self.current_step >= self.max_episode_steps:
            terminated = True
        else:
            terminated = False
        truncated = False
        info = {'sum': wc}

        return observation, reward, terminated, truncated, info
