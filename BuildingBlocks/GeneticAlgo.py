from Lexicon import Lexicon
from Judge import Judge
from PriorityQueue import PriorityQueue
import numpy as np
import pickle
from discordwebhook import Discord
import pandas as pd

discord = Discord(url="https://discord.com/api/webhooks/1281761924605804588/SQXoeys7zs2j5vWkiN5KXxHsO2QI5Sq_4zqXtD2HMnRxF8z7hi1yadfX5te2qquu2UT0")

class GeneticAlgo:
    """
    Class that implements a genetic algorithm to optimize the number of words in a set of n Building Blocks.

    Parameters
    ----------
    lexicon:Lexicon
        A Lexicon object that contains the alphabet and the word list.

    cubes:int
        The number of cubes in the Building Blocks.

    population_size:int
        The size of the population.

    generations:int
        The number of generations.

    elite_size:int
        The number of elite individuals that will be kept in the next generation.

    crossed_size:int
        The number of crossed offsprings that will be created for the next generation.

    mutated_size:int    
        The number of mutated offsprings that will be created for the next generation.

    random_size:int
        The number of random offsprings that will be created for the next generation.

    Methods
    -------
    random_permutation()
        Creates a random permutation of the elements in the base list.

    cross_child_of(parent1, parent2)
        Creates a crossed offspring from two parent individuals.
         
    mutate_child_from(parent)
        Creates a mutated offspring from a parent individual.

    crossover(elite_individuals, total_offsprings)  
        Makes the specified number of crossed offsprings from the elite individuals.

    mutate(elite_individuals, total_offsprings)
        Makes the given number of mutated offsprings from a list of elite individuals.

    run()
        Creates a random population of the specified size and runs the genetic algorithm for the specified number of generations
        creating the next generation based on the specified attributes.
    

    """

    def __init__(self, 
                 name:str,
                 lexicon:Lexicon,
                 cubes:int=6,
                 population_size:int=100, 
                 generations:int=1000, 
                 elite_size:int=20, 
                 crossed_size:int=60, 
                 mutated_size:int=10, 
                 random_size:int=10,
                 seed:int=202505,
                 random_state_path:str=None):
        self.name = name
        self.lex = lexicon
        self.cubes = cubes
        self.population_size = population_size
        self.generations = generations
        self.elite_size = elite_size
        self.crossed_size = crossed_size
        self.mutated_size = mutated_size
        self.random_size = random_size

        if random_state_path:
            with open(random_state_path, 'rb') as f:
                state = pickle.load(f)
            np.random.set_state(state)
        else:
            np.random.seed(seed) #set up the seed
        
        self.population = PriorityQueue(population_size)
        self.judge = Judge(self.lex.alphabet, self.lex.word_list)
        self.base = self.lex.calculate_letter_reps(cubes)[2]

        #create a dataframe to store the data of the population
        columns = [f'i{i}' for i in range(self.population_size)]
        self.data_frame = pd.DataFrame(columns=columns)
        

    def random_permutation(self):
        
        """
        Creates a random permutation of the elements in the base list.

        Returns:
            list: A randomly permuted list.
        """
        permutation = self.base.copy()

        for a in range(len(permutation)):
            #get a random index from the permutation list
            b = np.random.randint(0,len(permutation)-1)
            if a != b:
                #swap the item at index a with the item at index b
                permutation[a],permutation[b] = permutation[b],permutation[a]

        return permutation

    def cross_child_of(self, parent1:tuple, parent2:tuple):
        """
        Creates a crossed offspring from two parent individuals.

        Args:
            parent1 (tuple): Tuple representing the first parent individual (mono+rainbow, mono, (permutation:list, info:str)).
            parent2 (tuple): Tuple representing the second parent individual (mono+rainbow, mono, (permutation:list, info:str)).

        Returns:
            list: List representing the crossed offspring.

        Based on the fact that every individual is a list of letters and every 6 elements represent a cube,
        a crossed offspring is created by appending the i-th cube from either parent1 or parent2.
        The choice is made randomly for each cube.

        Example:
        parent1: [e, a, t, s, r, n, e, y, a, t, s, r, ..., b, t, s, r, n, e]
              \_______________/ \_______________/     \_______________/
                  cube-0              cube-1              cube-5
        parent2: [t, s, r, b, z, e, k, y, a, r, k, l, ..., c, h, k, u, o, e]
              \_______________/ \_______________/     \_______________/
                  cube-0              cube-1              cube-5
        offspring: [e, a, t, s, r, n, k, y, a, r, k, l, ..., b, t, s, r, n, e]
                  \_______________/ \_______________/     \_______________/
                  cube-0 from p1    cube-1 from p2          cube-5 from p1
        When deciding the cube-i for the offspring, we choose cube-i from either parent1 or parent2.
        """
        offspring = []

        #getting only the permutation from the parent (rainbow+mono, mono, permutation)
        parent1_permutation = parent1[2][0]
        parent2_permutation = parent2[2][0]

        for i in range(self.cubes):
                start = self.cubes*i
                end = start + self.cubes
                decision = np.random.randint(2)
                if decision == 0:
                    offspring+=parent1_permutation[start:end]
                else:
                    offspring+=parent2_permutation[start:end]

        return offspring
    
    def mutate_child_from(self, parent:tuple):
        """
        parent: tuple (priority:int, sub:int, (permutation:list, info:str))

        A mutated offspring is created by randomly swapping 2 letters in the permutation
        """
        offspring = parent[2][0].copy()

        a,b = random_different_pairs(len(offspring))

        offspring[a], offspring[b] = offspring[b], offspring[a]

        return offspring
    
    def crossover(self, elite_individuals:list, total_offsprings:int):
        """
        makes the specified number of crossed offsprings from the 20 elite individuals
        by choosing 2 random elite individuals and crossing them over
        """
        crossed_offsprings = []

        for i in range(total_offsprings):
            a, b = random_different_pairs(len(elite_individuals))
            parent1, parent2 = elite_individuals[a], elite_individuals[b]
            crossed_offsprings.append(self.cross_child_of(parent1, parent2))

        return crossed_offsprings
    
    def mutate(self, elite_individuals, total_offsprings):
        """
        makes the given number of mutated offsprings from a list of elite individuals
        by mutating the highest in the elite list
        """
        mutated_offsprings = []

        for i in range(total_offsprings):
            offspring = self.mutate_child_from(elite_individuals[i%len(elite_individuals)])
            mutated_offsprings.append(offspring)
        
        return mutated_offsprings
    

    def run(self, additional_individuals:list=None):
        """
        creates a random population of the specified size,
        then runs the genetic algorithm for the specified number of generations creating the next generation based on the specified parameters

        saves the information of the population to a csv file
        i.e (1800, 700, ['e', 'a', 't', 's', 'r', 'n', 'k', 'y', 'a', 'r', 'k', 'l', 'b', 't', 's', 'r', 'n', ..., 'e'])
        """
        

        #Check if there are arbitrary individuals to add to the initial population
        initial_population_size = self.population_size

        if additional_individuals:

            initial_population_size -= len(additional_individuals)

            for individual in additional_individuals:
                permutation = individual[0]
                info = individual[1]

                mono, rainbow = self.judge.count_words(permutation)
                priority = mono+rainbow
                sub = mono
                data_tuple = (permutation, f"g{0}{info}")
                self.population.put(priority, sub, data_tuple)
        

        #add random individuals to the initial population
        for _ in range(initial_population_size):
            individual = self.random_permutation()
            mono, rainbow = self.judge.count_words(individual)
            priority = mono+rainbow
            sub = mono
            data_tuple = (individual, f"g{0}")
            self.population.put(priority, sub, data_tuple)
        

        # Run the genetic algorithm for the specified number of generations
        for generation in range(0,self.generations):
                        
            population_list = []

            #traverse the population and save data to a dataframe
            for i in range(self.population_size):
                individual = self.population.get()
                priority = individual[0]
                info = individual[2][1]
                population_list.append(individual)

                #save the individual's priority aka mono+rainbow to the specified column and index
                self.data_frame.loc[generation,f'i{i}'] = f'{priority}{info}'

            
            # Select the number of best indviduals for reproduction that will be kept in the next population
            elite_individuals = population_list[:self.elite_size]
            
            # Create a dictionary to store the new offsprings
            new_individuals = {'c':[], 'm':[], 'r':[]} #crossed, mutated, random
            # Apply crossover and mutation to create new offspring off of the elite individuals
            new_individuals['c'] = self.crossover(elite_individuals, self.crossed_size)
            
            # Apply mutation to create new offspring off of the elite individuals
            new_individuals['m'] = self.mutate(elite_individuals, self.mutated_size)
            
            # Create random offspring
            new_individuals['r'] = [self.random_permutation() for _ in range(self.random_size)]
            
            #save time by not adding the items to the queue in the last generation
            if generation < self.generations-1:
                # Re-add the elite individuals to the population
                for individual in elite_individuals:
                    self.population.put(individual[0], individual[1], individual[2])

                #add new individuals to the population
                for key, list in new_individuals.items():
                    for individual in list:
                        mono, rainbow = self.judge.count_words(individual)
                        priority = mono+rainbow
                        sub = mono
                        data_tuple = (individual, f"g{generation}{key}")
                        self.population.put(priority, sub, data_tuple)
            
            print(f'gen{generation} done')

        #save the data to a csv file
        self.data_frame.to_csv(f'geneticAlgo/{self.name}.csv', index=False)

        
        #save the random state for later use
        state = np.random.get_state()
        file_name = f'geneticAlgo/{self.name}_random_state.pkl'
        with open(file_name, 'wb') as f:
            pickle.dump(state, f)


def random_different_pairs(target):
    """
    returns 2 random different integers from the interval [0, target-1]
    """
    a, b = np.random.randint(target), np.random.randint(target)
    while a == b:
        b = np.random.randint(target)
    return a, b