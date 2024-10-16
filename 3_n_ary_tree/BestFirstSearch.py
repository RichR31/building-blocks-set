import multiprocessing
from ..common.Lexicon import Lexicon
from ..common.Judge import Judge
from datetime import datetime
from ..common.PriorityQueue import PriorityQueue
import random

lex = Lexicon()
judge = Judge(lex.alphabet,lex.word_list)
random.seed(2000)

num_cubes = 6


#generates a list of 2-item tuples that contain the pair of indices to be swaps
#the first 90 items will be for all the swaps within cubes
#the other half will be for swaps within colors
swaps = [None]*180
count = 0
for i in range(num_cubes):
    for j in range(num_cubes-1):
        for k in range(j+1,num_cubes):
            #for swaps within a cube
            a,b = (6*i+j),(6*i+k)

            #for swaps within colors
            x,y = (6*j+i),(6*k+i)

            swaps[count],swaps[count+90] = (a,b),(x,y)
            count +=1


base = [lex.alphabet[i] for i in lex.calculate_letter_reps(6)[1]]

def run(max_num_permutations:int=0, name:str='', subname:str='', permutation:list=None ):

    print(str(name)+':'+str(subname)+' has started')
    
    mono, rainbow = judge.count_words(permutation)
    parent = permutation

    updates= []
    unique_permutations = 0  
    generation = 0  
    visited = []

    best = {'target':0, 'sub':0, 'permutation': ''.join(permutation), 'update':'root'}
    
    pq = PriorityQueue(360)

    if subname == 'mono_max':
        best['target'] = mono
    elif subname == 'rainbow_max':
        best['target'] = rainbow
    elif subname == 'sum_max':
        best['target'] = mono + rainbow
    
    best['sub'] = mono + rainbow

    pq.put(best['target'],best['sub'],(''.join(permutation),'root'))
    visited.append(''.join(permutation))

    
    while unique_permutations < max_num_permutations:

        data = pq.get()[1]
        parent = data[0]
        parent = list(parent)
        
        #check the children nodes using the swaps list
        for swap in swaps:

            a,b = swap
            #swap items at indices a and b in parent
            parent[a],parent[b] = parent[b],parent[a]
            
            string_version = "".join(parent)

            if string_version not in visited:

                #make record of the current swap
                visited.append(string_version)
   
                unique_permutations+=1

                #count how many words can be spelled with this changes
                mono,rainbow = judge.count_words(parent)
                sum = mono+rainbow

                if subname == 'mono_max':
                    wc = mono
                elif subname == 'rainbow_max':
                    wc = rainbow
                elif subname == 'sum_max':
                    wc = sum
                

                if wc > best['target']:
                    best = {'target':wc, 'sub': sum,  'permutation': string_version, 'update': "gen"+str(generation)+"-iter"+str(unique_permutations)}    
                    updates.append(unique_permutations)

                #add to queue
                pq.put(wc, sum, (string_version, "gen"+str(generation)+"-iter"+str(unique_permutations)))

            #un-do swap from before
            parent[a],parent[b] = parent[b],parent[a]
        generation += 1

    #add the best found, to the priority queue, so that it is included in the output file
    pq.put(best['target'], best['sub'], (best['permutation'], best['update']))

    #export the results
    best_file = open('output/'+name+'/'+subname+'_best.txt', 'w')
    updates_file = open('output/'+name+'/'+subname+'_updates.txt', 'w')
    iteration_file = open('output/'+name+'/'+subname+'_iterations.txt', 'a')

    
    #best
    while not pq.is_empty():
        wc, data = pq.get()
        permutation, updt = data
        best_file.write(str(wc)+','+str(permutation)+','+str(updt)+'\n')
    best_file.close()

    #updates
    for item in updates:
        updates_file.write(str(item)+'\n')
    updates_file.close()

    #iterations
    iteration_file.write(str(unique_permutations)+'\n')
    iteration_file.close()

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


if __name__ == '__main__':

    max_iter = 150000
    #root elements
    starting_point ={
        'base': [base]*3,
        'sim_ann_best':[
            list('ovrsmgbijtefnruektsezlxiwoyahadcqpln'), list('esvrlgoraxbwycutsiinomehjtklqepdafnz'), list('tpndaqaeiiuocrxleyltvhoebzrfkmjwgssn')
        ],
        'random':[random_permutation()]*3
    }

    processes_list = []

    for name, data in starting_point.items():
        
        best = {'mono_max': data[0],
        'rainbow_max': data[1],
        'sum_max': data[2]}

        for subname, permutation in best.items():
            #creating the processes
            p = multiprocessing.Process(target=run, args=(max_iter, name,subname, permutation))
            p.name = str(name)+"-"+str(subname)
            processes_list.append(p)
            p.start()

    for p in processes_list:
        p.join()
    
    print("DONE")

    