from Judge import Judge
from Lexicon import Lexicon


lexicon = Lexicon()
judge = Judge(lexicon.alphabet, lexicon.word_list)

folder = 'out/best_first'
max_targets = ['mono', 'rainbow','sum']
roots = ['base', 'seed2k_best', 'random_search_best']


for root in roots:

    for max_target in max_targets:
        file = f'{folder}/{root}/{max_target}_max_best.txt'
        print(file)
        with open(file, 'r') as f:
            lines = f.readlines()[:10]
            for line in lines:
                data = line.split(',')
                found_at = data[-1]
                mono, rainbow = judge.count_words(list(data[1]))
                print(f'& {data[1]} & {mono} & {rainbow} & {mono+rainbow} & {found_at}\\\\')
        print('=======================')


