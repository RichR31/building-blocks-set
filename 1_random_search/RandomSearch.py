import multiprocessing
import random
from ..common.Lexicon import Lexicon
from ..common.Judge import Judge
from datetime import datetime
from ..common.PriorityQueue import PriorityQueue

#create objects for Lexicon and Judge
lex = Lexicon()
judge = Judge(lex.alphabet,lex.word_list)

#import number of past iterations
past_iterations_file = open('out/random_search/iterations.txt', 'r')
past_iterations = int(past_iterations_file.readline())
past_iterations_file.close()

#import best on record
best = {'mono_max': None,
        'rainbow_max': None,
        'sum_max': None}

for name in best.keys():
    best_file = open("output/random_search/"+str(name)+"_best"+".txt",'r')
    best_data = best_file.readlines()
    best_file.close()
    
    pq = PriorityQueue(10)

    for item in best_data:
        wc, permutation, found_at = item[:-1].split(',')
        wc = int(wc)
        pq.put(wc,(permutation,found_at))
    
    best[name] = pq


top_mono_wc, top_mono_per = best['mono_max'].peek()
top_rainbow_wc, top_rainbow_per = best['rainbow_max'].peek()
top_sum_wc, top_sum_per = best['sum_max'].peek()

num_cubes = 6
base_permutation = [lex.alphabet[i] for i in lex.calculate_letter_reps(num_cubes)[1]]


def random_permutation():
    """
    Creates a random permutation from reps_lits_indices
    """
    permutation = base_permutation.copy()
    for i in range(len(permutation)):
        #get a random index from the permutation list
        j = random.randint(0,len(permutation)-1)
        
        #swap the item at index i with the item at index j
        permutation[i],permutation[j] = permutation[j],permutation[i]
    return permutation  


def run(max_iterations=100, shared_list:list=[], lock=None)-> tuple:
    """
    will create random permutations looking only for the best permutation 
    for mono words, for the specified number of iterations
    """
    process_name = multiprocessing.current_process().name
    mono_q = PriorityQueue(10)
    mono_q.put(top_mono_wc, top_mono_per)

    rainbow_q = PriorityQueue(5)
    rainbow_q.put(top_rainbow_wc, top_rainbow_per)

    sum_q = PriorityQueue(5)
    sum_q.put(top_sum_wc, top_sum_per)


    #will keep count of how many iterations are performed
    iterations=0
    
    #will keep track of how many times the current process 
    #found a better permutation than the one in record
    updates = {'mono_max':[], 'rainbow_max':[], 'sum_max':[]}
    
    while iterations < max_iterations:
        #increase the iteration count
        iterations +=1

        #generate new random permutation
        permutation = random_permutation()
        
        string_version = ''.join(permutation)

        #get the total mono words that can be spelled
        mono, rainbow = judge.count_words(permutation)
        
        sum = mono + rainbow
        current_iteration = iterations+past_iterations
        
        #increase the number of updates for every case
        if mono >= mono_q.peek()[0]:
            updates['mono_max'].append(current_iteration)
        
        if rainbow >= rainbow_q.peek()[0]:
            updates['rainbow_max'].append(current_iteration)
        
        if sum >= sum_q.peek()[0]:
            updates['sum_max'].append(current_iteration)

        #try to add to their respective priority queues regardless
        mono_q.put(mono,(string_version,current_iteration))      
        rainbow_q.put(rainbow,(string_version,current_iteration))
        sum_q.put(sum, (string_version, current_iteration))      
        

    with lock:
        shared_list.append((process_name,{
            'mono_max': ([str(item) for item in updates['mono_max']], mono_q),
            'rainbow_max': ([str(item) for item in updates['rainbow_max']], rainbow_q),
            'sum_max': ([str(item) for item in updates['sum_max']], sum_q)}))



if __name__ == '__main__':
    

    #A manager for multiprocessing
    manager = multiprocessing.Manager()
    #a lock object
    lock = multiprocessing.Lock()

    iterations = 150000
    processes = 10 #Dont change this number
    processes_list = []

    #create a shared list
    shared_output = manager.list()

    #initialize, name and start 5 processes for mono and 5 others for rainbow
    for i in range(processes):

        #mono process
        p = multiprocessing.Process(target=run, args=(iterations, shared_output, lock))
        p.name = str(i)
        #append to their respective lists and start them
        processes_list.append(p)
        p.start()
        print(p.name,"started...")


    #join the processes
    for p in processes_list:
        p.join()
    

    #export results
    for process_name, data_dictionary in shared_output:

        for key, value in data_dictionary.items():
            updates_file = open("output/"+str(key)+"_iterations"+".txt",'a')

            #unpacking data: (list, PriorityQueue)
            updates, q = value
            updates = ", ".join(updates)
            updates_file.write("after a batch of "+str(iterations)+" iterations, updates were found in iterations: "+updates+'\n')
            updates_file.close()

            while not q.is_empty():
                p,d = q.get()
                best[key].put(p, d)

    for name, q in best.items():
        best_file = open("output/"+str(name)+"_best"+".txt",'w')
        while not q.is_empty():
            number, data = q.get()
            permutation, update = data
            best_file.write(str(number)+','+str(permutation)+','+str(update)+'\n')
        
        best_file.close()

    #export number of past iterations
    past_iterations_file = open('out/iterations.txt', 'w')
    past_iterations_file.write(str(past_iterations + iterations))
    past_iterations_file.close()

    print('Program DONE!')



