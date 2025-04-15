import math
import random
from ..common.Lexicon import Lexicon
from ..common.Judge import Judge
from ..common.PriorityQueue import PriorityQueue
import os

#set seed
random.seed(2000)


#create objects for Lexicon and Judge
lex = Lexicon()
judge = Judge(lex.alphabet,lex.word_list)



def get_neighbour(current):
    """
    Creates a new permutation by swapping two random elements
    """
    permutation = current.copy()

    a, b = random.sample(range(len(permutation)), 2)
    permutation[a], permutation[b] = permutation[b], permutation[a]

    return permutation



#Run the simulated annealing algorithm

maximization_case = 'rainbow' #CHANGE TO 'mono' or 'rainbow' or 'both'
queue = PriorityQueue(10) #queue just used to keep track of the n best permutations found

#initialize the simulated annealing parameters
temperature = 1000
cooling_rate = 0.9999
maximum_iterations = 250000 #CHANGE


current = lex.calculate_letter_reps(6)[2]
current_mono, current_rainbow = judge.count_words(current)

#set the priority number and sub (priority) number based on the specified maximization case
if maximization_case == 'mono':
    current_wc, sub = current_mono, current_rainbow
elif maximization_case == 'rainbow':
    current_wc, sub = current_rainbow, current_mono
else:
    current_wc, sub = current_mono + current_rainbow, current_mono
#P0 means that this is the initial permutation (zero)
queue.put(current_wc, sub, (''.join(current)+'-P0')) 


for iteration in range(maximum_iterations):

    neighbour = get_neighbour(current)
    neighbour_mono, neighbour_rainbow = judge.count_words(neighbour)

    #set the neighbour_wc based on the specified maximization case
    if maximization_case == 'mono':
        neighbor_wc = neighbour_mono
    elif maximization_case == 'rainbow':
        neighbor_wc = neighbour_rainbow
    else:
        neighbor_wc = neighbour_mono + neighbour_rainbow

    # Calculate the change in score
    delta_wc = neighbor_wc - current_wc

    #now decide wheter or not to accept the neighbour
    #always accept if the score is better
    #and allow a worse score to be accepted with a probability
    
    if delta_wc > 0 or random.random() < random.random() < math.exp(-delta_wc/temperature):
        current = neighbour
        current_wc = neighbor_wc

        if current_wc > queue.peek()[0]:
            #set the priority number and sub (priority) number based on the specified maximization case
            if maximization_case == 'mono':
                priority, sub = neighbour_mono, neighbour_rainbow
            elif maximization_case == 'rainbow':
                priority, sub = neighbour_rainbow, neighbour_mono
            else:
                priority, sub = neighbour_mono + neighbour_rainbow, neighbour_mono

             
            queue.put(priority, sub, (''.join(current)+'-P'+str(iteration)))

    #cool down the temperature
    temperature *= cooling_rate


# Ensure the output directory exists
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)
# Save the contents of the queue to a file
output_file = os.path.join(output_dir, f'{maximization_case}_max.txt')
with open(output_file, 'w') as f:
    f.write(f"Temperature: {temperature}\n")
    f.write(f"Cooling Rate: {cooling_rate}\n")
    f.write(f"Timesteps: {maximum_iterations}\n\n")
    while not queue.is_empty():
        item = queue.get()
        f.write(f"Score: {item[0]}, Mono: {item[1]}, Permutation: {item[2]}\n")

