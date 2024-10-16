import pandas as pd
import numpy as np
import imageio

import matplotlib.pyplot as plt

test_name = 'Iteration5_2'
v = 1

columns = [str(i) for i in range(473)]
df = pd.DataFrame(columns=columns)

csv = open(f'geneticAlgo/{test_name}/v{v}.csv', 'r')
lines = csv.readlines()[1:]
csv.close()

for row, line in enumerate(lines):
    line = line.strip('\n').split(',')

    for i,item in enumerate(line):
        wc = item.split('g')[0]
        df.loc[row, str(i) ] = int(wc)




images = []

colors = np.random.rand(100, 3)

# Generate an image for each row
for index, row in df.iterrows():
    plt.bar(range(len(row)), row, color=colors)
    plt.xlabel('Individuals', fontsize='small')
    plt.ylabel('Word Count', fontsize='small')
    plt.title(f'Generation{index}')
    plt.grid(axis='y')
    
    # Save the plot as an image
    filename = f'animation/row_{index+1}.png'
    plt.savefig(filename)
    plt.close()
    
    # Read the image and append it to the list
    images.append(imageio.imread(filename))

# Save the list of images as a GIF
imageio.mimsave(f'animation/{test_name}_v{v}.gif', images, duration=30)
