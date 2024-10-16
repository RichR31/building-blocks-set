import random
from Lexicon import Lexicon


random.seed(2000)

lex = Lexicon()

base = lex.calculate_letter_reps(6)[2]
def random_permutation():
    """
    Creates a random permutation from reps_lits_indices
    """
    permutation = base.copy()
    for i in range(len(permutation)):
        #get a random index from the permutation list
        j = random.randint(0,len(permutation)-1)
        
        #swap the item at index i with the item at index j
        permutation[i],permutation[j] = permutation[j],permutation[i]
    return permutation  

seed2k = random_permutation()
print(''.join(seed2k))

h = [list('esdauoygtjcrrlhbfesikveitqnxwmlazpno')]*3
print(h)