import multiprocessing
import os
from ..common.Lexicon import Lexicon
from ..common.Judge import Judge
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
    
    best_mono, best_rainbow = judge.count_words(permutation)
    parent = permutation

    updates= []

    best_wc = 0
    pq = PriorityQueue(10)

    if subname == 'mono_max':
        best_wc = best_mono
    elif subname == 'rainbow_max':
        best_wc = best_rainbow
    elif subname == 'sum_max':
        best_wc = best_mono + best_rainbow

    pq.put(best_wc,(''.join(permutation),'root'))

    unique_permutations = 0  
    generation = 0  
    visited = []
    
    while unique_permutations < max_num_permutations:

        generation_best = {'permutation':None, 'wc': 0}

        
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
                #NOTE: I unpacked the judge return for possible changes in maximization logic
                mono,rainbow = judge.count_words(parent)

                if subname == 'mono_max':
                    wc = mono
                elif subname == 'rainbow_max':
                    wc = rainbow
                elif subname == 'sum_max':
                    wc = mono + rainbow
                
                #check if the current permutation is the best so far
                if wc > best_wc:
                    best_wc = wc
                    updates.append(unique_permutations)
                
                if wc > generation_best['wc']:
                    generation_best.update({'permutation': parent.copy(), 'wc': wc})
                
                #add to queue anyways
                pq.put(wc,(string_version,"gen"+str(generation)+"-iter"+str(unique_permutations)))

            #un-do swap from before
            parent[a],parent[b] = parent[b],parent[a]
        
        parent = generation_best['permutation']
        
        generation += 1

    #export the results
    best_file = open('output/'+name+'/'+subname+'_best.txt', 'w')
    updates_file = open('output/'+name+'/'+subname+'_updates.txt', 'w')
    iteration_file = open('output/'+name+'/'+subname+'_iterations.txt', 'w')

    while not pq.is_empty():
        wc, data = pq.get()
        permutation, updt = data
        best_file.write(str(wc)+','+str(permutation)+','+str(updt)+'\n')
    best_file.close()

    for item in updates:
        updates_file.write(str(item)+'\n')
    updates_file.close()

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
    #the roots for the different trees
    starting_point ={

        'base': [base]*3,
        'random_search_best':[
            list('ovrsmgbijtefnruektsezlxiwoyahadcqpln'), list('esvrlgoraxbwycutsiinomehjtklqepdafnz'), list('tpndaqaeiiuocrxleyltvhoebzrfkmjwgssn')
        ],
        'random':[random_permutation()]*3
    }

    processes_list = []

    #start each tree as a separate process
    for name, data in starting_point.items():
        # Ensure the output directory exists
        output_dir = f'output/{name}'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        best = {'mono_max': data[0],
        'rainbow_max': data[1],
        'sum_max': data[2]}

        for subname, permutation in best.items():
            
            p = multiprocessing.Process(target=run, args=(130000, name,subname, permutation))
            p.name = str(str(name)+"-"+str(subname))
            processes_list.append(p)
            p.start()

    #wait for all processes to finish
    for p in processes_list:
        p.join()
    
    print("DONE")


    