import os
from GeneticAlgorithm import GeneticAlgorithm
from Lexicon import Lexicon
from discordwebhook import Discord


if __name__ == '__main__':
    discord = Discord(url="https://discord.com/api/webhooks/1281761924605804588/SQXoeys7zs2j5vWkiN5KXxHsO2QI5Sq_4zqXtD2HMnRxF8z7hi1yadfX5te2qquu2UT0")
    lexicon = Lexicon()
    cubes = 6

    #parameters
    population_size = 100
    generations = 500
    elite_size = 20
    crossed_type1_size = 10
    crossed_type2_size = 10
    mutated_size = 40
    random_size = 20
    seed = 202505 #my grad year and month


    folder_name = 'Iteration5_CORRECTED' #CHANGE THIS EVERY TIME YOU MAKE A NEW TEST

    # Create a folder with the specified folder_name
    folder_path = os.path.join('/D/students/salazarordon/BuildingBlocks/geneticAlgo/', folder_name)
    os.makedirs(folder_path, exist_ok=True)


    description = ['Testing the genetic algorithm with only scenario 1',
                    'parameters:',
                    f'\tpopulation_size={population_size}\n',
                    f'\tgenerations={generations}\n',
                    f'\telite_size={elite_size}\n',
                    f'\tcrossed_type1_size={crossed_type1_size}\n',
                    f'\tcrossed_type2_size={crossed_type2_size}\n',
                    f'\tmutated_size={mutated_size}\n',
                    f'\trandom_size={random_size}\n',
                    f'\tseed={seed}\n'
                   ]
    
    # Create a text file called info.txt inside folder_name that will contain the contents of the description list
    file_path = os.path.join(folder_path, 'info.txt')
    with open(file_path, 'w') as file:
        file.writelines(description)
        file.close()


    discord.post(content='Genetic algorithm test started...')

    genetic_algo = GeneticAlgorithm(name=f'{folder_name}/v1',
                               lexicon=lexicon, 
                               cubes=cubes, 
                               population_size=population_size, 
                               generations=generations, 
                               elite_size=elite_size, 
                               crossed_type1_size=crossed_type1_size, 
                               crossed_type2_size=crossed_type2_size, 
                               mutated_size=mutated_size, 
                               random_size=random_size,
                               seed=seed)
    
    genetic_algo.run()

    discord.post(content=f'Genetic Algorithm {folder_name} done...')