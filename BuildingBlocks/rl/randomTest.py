from random import randint
from BBEnv_v1 import BBEnv
from Lexicon import Lexicon
from discordwebhook import Discord
import random


max_episode_steps = 500
lex = Lexicon()
env = BBEnv(cubes=6, words_list=lex.word_list, alphabet=lex.alphabet, max_epidose_steps=max_episode_steps)
discord = Discord(url="https://discord.com/api/webhooks/1258537167752396831/9YvFGoycowPsF1blWQ9CMjECy-vnulyu5I3X9SOH9LMio5nlYOIFdVj0NZCmoIf7z-va")

base = lex.calculate_letter_reps(6)[2]

random.seed(202405)

def random_permutation():
        """
        Creates a random permutation from reps_lits_indices
        """
        permutation = base.copy()

        for i in range(len(permutation)):
            #get a random index from the permutation list
            j = randint(0,len(permutation)-1)
            
            #swap the item at index i with the item at index j
            permutation[i],permutation[j] = permutation[j],permutation[i]
        return permutation  

number_of_episodes = 50

best_overall = {'wc': 0, 'permutation': ''}

discord.post(content="_____ Random Test Started______")

for episode in range(number_of_episodes):

    episode_cummulative_wc = 0
    permutation = random_permutation()
    best_in_episode = {'wc': 0, 'permutation': ''}

    for i in range(max_episode_steps):

        a,b = env.swaps[random.randint(0,179)]
        permutation[a], permutation[b] = permutation[b], permutation[a]

        mono, rainbow = env.judge.count_words(permutation)

        wc = mono + rainbow

        if wc > best_in_episode['wc']:
            best_in_episode['wc'] = wc
            best_in_episode['permutation'] = permutation.copy()

            if wc > best_overall['wc']:
                best_overall['wc'] = wc
                best_overall['permutation'] = permutation.copy()

        episode_cummulative_wc += wc

    episode_mean = episode_cummulative_wc/max_episode_steps
    
    print(f'episode {episode} best|| {best_in_episode["wc"]} | {best_in_episode["permutation"]}')
    print(f'episode {episode} last change|| {wc} | {permutation}')
    print(f'episode {episode} mean: {episode_mean}')
    print('_________________________')

print(f'_____ best overall|| {best_overall["wc"]} | {best_overall["permutation"]} _____')
discord.post(content="_____ Random Test Ended______")




