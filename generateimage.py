import numpy as np
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import os.path

headers = ['timestamp', 'population', 'generation', 'mutation_rate', 'num_parents', '0', '1', '2']

df = pd.read_csv('.\data\convergence.csv', delimiter='\t')

# print(df)
fitness = df['1'].tail(-1).to_numpy()
time = df['2'].tail(-1).to_numpy()

plt.plot(time, fitness)

newfile = False
i = 0

# print(os.path.isfile('.\data\GA_param_testing\graph1.png'))
while newfile == False:
    print(os.path.isfile('.\data\GA_param_testing\graph' + str(i) + '.png'))
    if os.path.isfile('.\data\GA_param_testing\graph' + str(i) + '.png') == False:
        plt.savefig('.\data\GA_param_testing\graph' + str(i) + '.png')
        newfile == True
        break
    else:
        i += 1

plt.show()