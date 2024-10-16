
import random
import numpy as np
from Judge import Judge
from Lexicon import Lexicon

lex = Lexicon()
jud = Judge(lex.alphabet, lex.word_list)

cubes = 6

base = list('eeeaarroottiissllnnudcpmhygbfwkvzxjq')

best = list('wtemcglrtndseiaeyorshlnkslbptduoiaea') 

corrected = list('wtzmcglrvndseiaeyorshlnkxfbptjuoiqea')
mono, rainbow = jud.count_words(corrected)

print(mono+rainbow)


