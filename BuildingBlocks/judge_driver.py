from Judge import Judge
from Lexicon import Lexicon

lex = Lexicon()
judge = Judge(lex.alphabet, lex.word_list)

permutation = list('yqoiaektdpvflnsjhrxaeouitegbwcrmlnzs')

mono, rainbow = judge.count_words(permutation)

print(mono+rainbow)