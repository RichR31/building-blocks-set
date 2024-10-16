from stable_baselines3 import PPO
import gymnasium as gym
from stable_baselines3.common.env_util import make_vec_env

from BBEnv_v1 import BBEnv
from ..common.Lexicon import Lexicon


if __name__ == '__main__':

    dir_path = '/tmp/gym'
    lex = Lexicon()

    print("_____ EVAL PPO v1 STARTED ______")
    text_file = open("output/ppo_v1.txt", "w")

    max_episode_steps = 500
    number_of_episodes = 50

    vec_env = make_vec_env(BBEnv, n_envs=1, env_kwargs=dict(cubes=6, words_list=lex.word_list, alphabet=lex.alphabet, max_epidose_steps=max_episode_steps))
    loaded_model = PPO.load(f"{dir_path}/PPO-BuildingBlocks_v1")

    obs = vec_env.reset()
    n_steps = max_episode_steps*number_of_episodes

    best_overall = {'wc': 0, 'permutation': ''}
    episode_cummulative_wc = 0
    episode = 0
    best_in_episode = {'wc': 0, 'permutation': ''}
    for _ in range(n_steps):
        action, _states = loaded_model.predict(obs, deterministic=False)
        obs, rewards, dones, info = vec_env.step(action)

        permutation = ''.join([lex.alphabet[i] for i in obs[0].tolist()])
        wc = info[0]['sum']

        if wc > best_in_episode['wc']:
            best_in_episode['wc'] = wc
            best_in_episode['permutation'] = permutation

            if wc > best_overall['wc']:
                best_overall['wc'] = wc
                best_overall['permutation'] = permutation

        episode_cummulative_wc += wc


        if dones:
            obs = vec_env.reset()
            episode_mean = episode_cummulative_wc/max_episode_steps
            print('_________________________')
            print(f'episode {episode} best|| {best_in_episode["wc"]} | {best_in_episode["permutation"]}')
            print(f'episode {episode} last change|| {wc} | {permutation}')
            print(f'episode {episode} mean: {episode_mean}')
            print('_________________________')

            text_file.write(f'episode {episode} best|| {best_in_episode["wc"]} | {best_in_episode["permutation"]}\n')
            text_file.write(f'episode {episode} last change|| {wc} | {permutation}\n')
            text_file.write(f'episode {episode} mean: {episode_mean}\n')
            text_file.write('_________________________\n')

            episode += 1
            episode_cummulative_wc = 0
            best_in_episode = {'wc': 0, 'permutation': ''}


    print(f'best overall|| {best_overall["wc"]} | {best_overall["permutation"]}')
    text_file.write(f'best overall|| {best_overall["wc"]} | {best_overall["permutation"]}\n')
    text_file.close()
        




    