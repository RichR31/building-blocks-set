
from stable_baselines3 import PPO
import gymnasium as gym
from stable_baselines3.common.env_util import make_vec_env

from BBEnv_v1 import BBEnv
from ..common.Lexicon import Lexicon

dir_path = '/tmp/gym'

if __name__ == '__main__':

    lex = Lexicon()
    print("_____ TRAINING PPO STARTED (v1) ______")

    #Environment parameters
    max_episode_len = 500
    train_steps = max_episode_len * 1000
    n_envs = 1
    vec_env = make_vec_env(BBEnv, n_envs=n_envs, env_kwargs=dict(cubes=6, words_list=lex.word_list, alphabet=lex.alphabet, max_epidose_steps=max_episode_len))
    
    #model
    model = PPO(
        policy='MlpPolicy', 
        env=vec_env, 
        verbose=1,
        learning_rate=0.0001,
        n_steps=2048
        )
    
    #train model
    model.learn(total_timesteps=train_steps)
    #save model
    model.save(f"{dir_path}/PPO-BuildingBlocks_v1")

    
    print("_____ TRAINING PPO ENDED (v1)______")