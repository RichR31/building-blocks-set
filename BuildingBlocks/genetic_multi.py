import multiprocessing
import os
import sys
from GeneticAlgo3 import GeneticAlgo
from Lexicon import Lexicon
from discordwebhook import Discord



def worker(name:str, 
            lex:Lexicon, 
            cubes:int, 
            population_size:int, 
            generations:int, 
            elite_size:int, 
            crossed_size:int,
            mutated_size:int,
            random_size:int,
            seed:int,
            additional_individuals:list=None):
    """
    Worker function to run the genetic algorithm
    """

    genetic_algo = GeneticAlgo(name=name,
                               lexicon=lex, 
                               cubes=cubes, 
                               population_size=population_size, 
                               generations=generations, 
                               elite_size=elite_size, 
                               crossed_size=crossed_size, 
                               mutated_size=mutated_size, 
                               random_size=random_size,
                               seed=seed)
    
    genetic_algo.run(additional_individuals)
    

if __name__ == '__main__':
    discord = Discord(url="https://discord.com/api/webhooks/1281761924605804588/SQXoeys7zs2j5vWkiN5KXxHsO2QI5Sq_4zqXtD2HMnRxF8z7hi1yadfX5te2qquu2UT0")
    lexicon = Lexicon()
    cubes = 6

    #parameters
    population_size = 100
    generations = 1000
    elite_size = 20
    crossed_size = 20
    mutated_size = 40
    random_size = 20
    seed = 202505 #my grad year and month


    folder_name = 'Iteration9' #CHANGE THIS EVERY TIME YOU MAKE A NEW TEST

    # Create a folder with the specified folder_name
    folder_path = os.path.join('/D/students/salazarordon/BuildingBlocks/geneticAlgo/', folder_name)
    os.makedirs(folder_path, exist_ok=True)


    description = ['Testing the genetic algorithm with multiple versions of the permutation\n',
                   'This iteration uses GenetiAlgov5: with a modified way to make the crossover: a half elite-elite and the nother elite-nonelite(from the 40-60%\n',
                   'it also keeps track of the best individual in each generation, and after 50 times of it being repeated it will keep only the best and re populate the rest spots with random individuals\n',
                    'v1: no arbitrary initial individuals\n',
                    'v2: arbitrary added: Base permutation, Seed2000, and best from simmulated Annealing\n',
                    'v3: arbitrary added: Best from Greedy Algorithm (GA), Best from Algorithm2 (A2) and best from Best First Search (BFS)\n',
                    'parameters:',
                    f'\tpopulation_size={population_size}\n',
                    f'\tgenerations={generations}\n',
                    f'\telite_size={elite_size}\n',
                    f'\tcrossed_size={crossed_size}\n',
                    f'\tmutated_size={mutated_size}\n',
                    f'\trandom_size={random_size}\n',
                    f'\tseed={seed}\n'
                   ]
    
    # Create a text file called info.txt inside folder_name that will contain the contents of the description list
    file_path = os.path.join(folder_path, 'info.txt')
    with open(file_path, 'w') as file:
        file.writelines(description)
        file.close()
    

    info ={
        'v1': None,
        'v2': [(lexicon.calculate_letter_reps(6)[2],'B'), #(960 words) base permutation 
               (list('esdauoygtjcrrlhbfesikveitqnxwmlazpno'), 'R2K'), #(1550 words) random permutation with seed=2000
               (list('tpndaqaeiiuocrxleyltvhoebzrfkmjwgssn'),'SA') #(1881 words) best permutation from the sum optimization of simulated annealing
               ],
        'v3': [
            (list('eioxauioehjanqsrlrptgdkvbyctfsmezlnw'),'GA'), #(2268 words) yielded best sum. from greedy search rainbow max
            (list('wozeuakycgtelsdjnhiieoaqmbfpvtrnslxr'),'A2'),   #(2360 words) yielded best sum 36. from algorithm_v2 sum max
            (list('yqoiaektdpvflnsjhrxaeouitegbwcrmlnzs'),'BFS') #(2328 words) yielded best sum. from Best first search sum max
        ]
    }

    # Create three worker processes
    processes = []

    discord.post(content='Genetic algorithm test started...')
    
    for name, additional_individuals in info.items():

        p = multiprocessing.Process(target=worker, args=(f'{folder_name}/{name}', 
                                                        lexicon, 
                                                        cubes, 
                                                        population_size, 
                                                        generations, 
                                                        elite_size, 
                                                        crossed_size,
                                                        mutated_size,
                                                        random_size,
                                                        seed,
                                                        additional_individuals))
        p.start()
        processes.append(p)

    

    # Wait for all processes to finish
    for p in processes:
        p.join()
    
    discord.post(content=f'Genetic Algorithm {folder_name} done...')