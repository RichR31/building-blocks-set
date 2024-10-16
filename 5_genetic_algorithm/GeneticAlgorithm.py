from random import shuffle
from ..common.Lexicon import Lexicon
from ..common.Judge import Judge
from ..common.PriorityQueue import PriorityQueue
import numpy as np
import pandas as pd

class GeneticAlgorithm:
    """
    Class that implements a genetic algorithm to optimize the number of words in a set of n Building Blocks.

    Parameters
    ----------
    lexicon : Lexicon
        A Lexicon object that contains the alphabet and the word list.
    cubes : int
        The number of cubes in the Building Blocks.
    population_size : int
        The size of the population.
    generations : int
        The number of generations.
    elite_size : int
        The number of elite individuals that will be kept in the next generation.
    crossed_size : int
        The number of crossed offsprings that will be created for the next generation.
    mutated_size : int    
        The number of mutated offsprings that will be created for the next generation.
    random_size : int
        The number of random offsprings that will be created for the next generation.

    Methods
    -------
    random_permutation()
        Creates a random permutation of the elements in the base list.
    cross_child_of(parent1, parent2)
        Creates a crossed offspring from two parent individuals.
    v2_cross_child_of(parent1, parent2)
        Creates a crossed offspring from two parent individuals, ensuring the offspring has the same number of letter repetitions as the base.
    mutate_child_from(parent)
        Creates a mutated offspring from a parent individual.
    crossover(population)
        Makes the specified number of crossed offsprings from the elite individuals.
    mutate(population)
        Makes the given number of mutated offsprings from a list of elite individuals.
    run(additional_individuals=None)
        Creates a random population of the specified size and runs the genetic algorithm for the specified number of generations,
        creating the next generation based on the specified attributes.
    """

    def __init__(self, 
                 name: str,
                 lexicon: Lexicon,
                 cubes: int = 6,
                 population_size: int = 100, 
                 generations: int = 1000, 
                 elite_size: int = 20, 
                 crossed_type1_size: int = 60, 
                 crossed_type2_size: int = 60, 
                 mutated_size: int = 10, 
                 random_size: int = 10,
                 seed: int = 202505):
        self.name = name
        self.lex = lexicon
        self.cubes = cubes
        self.population_size = population_size
        self.generations = generations
        self.elite_size = elite_size
        self.crossed_type1_size = crossed_type1_size
        self.crossed_type2_size = crossed_type2_size
        self.mutated_size = mutated_size
        self.random_size = random_size

        np.random.seed(seed)  # set up the seed

        self.population = PriorityQueue(population_size)
        self.judge = Judge(self.lex.alphabet, self.lex.word_list)
        self.letter_rep, self.indices, self.base = self.lex.calculate_letter_reps(cubes)

        # create a dataframe to store the data of the population
        columns = [f'i{i}' for i in range(self.population_size)]
        self.data_frame = pd.DataFrame(columns=columns)

    def random_permutation(self):
        """
        Creates a random permutation of the elements in the base list.

        Returns
        -------
        list
            A randomly permuted list.
        """
        permutation = self.base.copy()

        for a in range(len(permutation)):
            # get a random index from the permutation list
            b = np.random.randint(0, len(permutation) - 1)
            if a != b:
                # swap the item at index a with the item at index b
                permutation[a], permutation[b] = permutation[b], permutation[a]

        return permutation

    def cross_child_of(self, parent1: tuple, parent2: tuple):
        """
        Creates a crossed offspring from two parent individuals.

        Parameters
        ----------
        parent1 : tuple
            Tuple representing the first parent individual (mono+rainbow, mono, (permutation:list, info:str)).
        parent2 : tuple
            Tuple representing the second parent individual (mono+rainbow, mono, (permutation:list, info:str)).

        Returns
        -------
        list
            List representing the crossed offspring.

        Based on the fact that every individual is a list of letters and every 6 elements represent a cube,
        a crossed offspring is created by appending the i-th cube from either parent1 or parent2.
        The choice is made randomly for each cube.

        Example
        -------
        parent1: [e, a, t, s, r, n, e, y, a, t, s, r, ..., b, t, s, r, n, e]
                 \_______________/ \_______________/     \_______________/
                  cube-0              cube-1              cube-5
        parent2: [t, s, r, b, z, e, k, y, a, r, k, l, ..., c, h, k, u, o, e]
                 \_______________/ \_______________/     \_______________/
                  cube-0              cube-1              cube-5
        offspring: [e, a, t, s, r, n, k, y, a, r, k, l, ..., b, t, s, r, n, e]
                  \_______________/ \_______________/     \_______________/
                  cube-0 from p1    cube-1 from p2          cube-5 from p1
        """
        child = []

        # getting only the permutation from the parent (rainbow+mono, mono, permutation)
        parent1_permutation = parent1[2][0]
        parent2_permutation = parent2[2][0]

        for i in range(self.cubes):
            start = self.cubes * i
            end = start + self.cubes
            decision = np.random.randint(2)
            if decision == 0:
                child += parent1_permutation[start:end]
            else:
                child += parent2_permutation[start:end]

        return child

    def v2_cross_child_of(self, parent1: tuple, parent2: tuple):
        """
        Creates a crossed offspring from two parent individuals, ensuring the offspring has the same number of letter repetitions as self.base.

        Parameters
        ----------
        parent1 : tuple
            Tuple representing the first parent individual (mono+rainbow, mono, (permutation:list, info:str)).
        parent2 : tuple
            Tuple representing the second parent individual (mono+rainbow, mono, (permutation:list, info:str)).

        Returns
        -------
        list
            List representing the crossed offspring.
        """
        child = self.cross_child_of(parent1, parent2)
        missing_letters = self.base.copy()
        
        for letter in child:
            if letter in missing_letters:
                missing_letters.remove(letter)

        if missing_letters:
            letter_reps_target = dict()

            for i, letter in enumerate(child):
                if letter in letter_reps_target:
                    letter_reps_target[letter].append(i)
                else:
                    letter_reps_target[letter] = [i]

            indices_to_replace = []

            for letter, indices in letter_reps_target.items():
                if len(indices) > self.letter_rep[letter]:
                    difference = len(indices) - self.letter_rep[letter]
                    for _ in range(difference):
                        index = np.random.randint(0, len(indices))
                        indices_to_replace.append(indices.pop(index))
            
            shuffle(missing_letters)

            for index in indices_to_replace:
                child[index] = missing_letters.pop()
        
        return child

    def mutate_child_from(self, parent: tuple):
        """
        Creates a mutated offspring from a parent individual.

        Parameters
        ----------
        parent : tuple
            Tuple representing the parent individual (priority:int, sub:int, (permutation:list, info:str)).

        Returns
        -------
        list
            List representing the mutated offspring.

        A mutated offspring is created by randomly swapping 2 letters in the permutation.
        """
        offspring = parent[2][0].copy()

        a, b = random_different_pairs(len(offspring))

        offspring[a], offspring[b] = offspring[b], offspring[a]

        return offspring

    def crossover(self, population: list):
        """
        Makes the specified number of crossed offsprings from the elite individuals.

        Parameters
        ----------
        population : list
            List of individuals in the population.

        Returns
        -------
        list
            List of crossed offsprings.
        """
        crossed_children = []
        
        # type 1 is for the crossed offsprings of the elite individuals
        for i in range(self.crossed_type1_size):
            a, b = random_different_pairs(self.elite_size)
            parent1, parent2 = population[a], population[b]
            crossed_children.append(self.v2_cross_child_of(parent1, parent2))

        # type 2 is for the crossed offsprings of one elite individual and one non-elite individual
        for i in range(self.crossed_type2_size):
            a = i % self.elite_size
            b = np.random.randint(low=self.elite_size, high=self.population_size)
            parent1, parent2 = population[a], population[b]
            crossed_children.append(self.v2_cross_child_of(parent1, parent2))

        return crossed_children

    def mutate(self, population: list):
        """
        Makes the given number of mutated offsprings from a list of elite individuals.

        Parameters
        ----------
        population : list
            List of individuals in the population.

        Returns
        -------
        list
            List of mutated offsprings.
        """
        mutated_offsprings = []

        for i in range(self.mutated_size):
            offspring = self.mutate_child_from(population[i % self.elite_size])
            mutated_offsprings.append(offspring)
        
        return mutated_offsprings

    def run(self, additional_individuals: list = None):
        """
        Creates a random population of the specified size and runs the genetic algorithm for the specified number of generations,
        creating the next generation based on the specified parameters.

        Parameters
        ----------
        additional_individuals : list, optional
            List of additional individuals to add to the initial population (default is None).

        Saves the information of the population to a CSV file and the final population to a text file.
        """
        # Check if there are arbitrary individuals to add to the initial population
        initial_population_size = self.population_size

        if additional_individuals:
            initial_population_size -= len(additional_individuals)

            for permutation in additional_individuals:
                permutation = permutation[0]
                info = permutation[1]

                mono, rainbow = self.judge.count_words(permutation)
                priority = mono + rainbow
                sub = mono
                data_tuple = (permutation, f"g{0}{info}")
                self.population.put(priority, sub, data_tuple)

        # add random individuals to the initial population
        for _ in range(initial_population_size):
            permutation = self.random_permutation()
            mono, rainbow = self.judge.count_words(permutation)
            priority = mono + rainbow
            sub = mono
            data_tuple = (permutation, f"g{0}")
            self.population.put(priority, sub, data_tuple)

        # Run the genetic algorithm for the specified number of generations
        for generation in range(self.generations):
            population_list = []

            # traverse the population and save data to a dataframe
            for i in range(self.population_size):
                permutation = self.population.get()
                priority = permutation[0]
                info = permutation[2][1]
                population_list.append(permutation)

                # save the individual's priority aka mono+rainbow to the specified column and index
                self.data_frame.loc[generation, f'i{i}'] = f'{priority}{info}'

            # Select the number of best individuals for reproduction that will be kept in the next population
            elite_individuals = population_list[:self.elite_size]
            
            # Create a dictionary to store the new offsprings
            new_individuals = {'c': [], 'm': [], 'r': []}  # crossed, mutated, random
            # Apply crossover and mutation to create new offspring off of the elite individuals
            new_individuals['c'] = self.crossover(population_list)
            
            # Apply mutation to create new offspring off of the elite individuals
            new_individuals['m'] = self.mutate(population_list)
            
            # Create random offspring
            new_individuals['r'] = [self.random_permutation() for _ in range(self.random_size)]
            
            # Re-add the elite individuals to the population
            for permutation in elite_individuals:
                self.population.put(permutation[0], permutation[1], permutation[2])

            # add new individuals to the population
            for key, list in new_individuals.items():
                for permutation in list:
                    mono, rainbow = self.judge.count_words(permutation)
                    priority = mono + rainbow
                    sub = mono
                    data_tuple = (permutation, f"g{generation}{key}")
                    self.population.put(priority, sub, data_tuple)
            
            print(f'gen{generation} done')
        
        final_population = []
        for i in range(self.population_size):
            wc, mono, permutation = self.population.get()
            final_population.append(permutation[0])

        # Save the contents of the final population to a txt file
        with open(f'output/{self.name}_final_population.txt', 'w') as f:
            for permutation in final_population:
                f.write(' '.join(permutation) + '\n')
        
        # save the data to a csv file
        self.data_frame.to_csv(f'output/{self.name}.csv', index=False)


def random_different_pairs(target: int):
    """
    Returns 2 random different integers from the interval [0, target-1].

    Parameters
    ----------
    target : int
        The upper limit (exclusive) for the random integers.

    Returns
    -------
    tuple
        A tuple containing two different random integers.
    """
    a, b = np.random.randint(target), np.random.randint(target)
    while a == b:
        b = np.random.randint(target)
    return a, b