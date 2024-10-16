from Lexicon import Lexicon
from Judge import Judge
from random import randint
from random import shuffle

lex = Lexicon()
judge = Judge(lex.alphabet,lex.word_list)

base_reps, base_indices, base_permutation = lex.calculate_letter_reps(6)

target = list('wtemcglrtndseiaeyorshlnkslbptduoiaea')
missing_letters = base_permutation.copy()
for letter in target:
    if letter in missing_letters:
        missing_letters.remove(letter)

letter_reps_target = dict()

for i, letter in enumerate(target):
    if letter in letter_reps_target:
        letter_reps_target[letter].append(i)
    else:
        letter_reps_target[letter] = [i]

indices_to_replace = []

for letter, indices in letter_reps_target.items():
    if len(indices) > base_reps[letter]:
        difference = len(indices) - base_reps[letter]
        for _ in range(difference):
            index = randint(0, len(indices) - 1)
            indices_to_replace.append(indices.pop(index))

print(missing_letters)
print(indices_to_replace)
print(letter_reps_target)

shuffle(missing_letters)

for index in indices_to_replace:
    target[index] = missing_letters.pop()

print(''.join(target))

