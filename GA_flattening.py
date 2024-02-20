import matplotlib.pyplot as plt
from scipy.signal import sawtooth
import numpy as np
from PIL import Image
from matplotlib.colors import LogNorm
from scipy.ndimage import zoom
from scipy.ndimage import gaussian_filter

def shift_array(arr, n, direction):
    rows, cols = arr.shape
    new_arr = np.zeros_like(arr)  # Initialize a new array filled with zeros

    if direction == 'right':
        new_arr[:, n:cols] = arr[:, :cols-n]
    elif direction == 'left':
        new_arr[:, :cols-n] = arr[:, n:cols]
    elif direction == 'down':
        new_arr[n:rows, :] = arr[:rows-n, :]
    elif direction == 'up':
        new_arr[:rows-n, :] = arr[n:rows, :]

    return new_arr


class flattening_GA:
    def __init__(self, GA_population, GA_generations, GA_num_parents, GA_mutation_rate, SLMwidth, SLMheight):
        self.SLMwidth = SLMwidth
        self.SLMheight = SLMheight
        self.population_size = GA_population
        self.generations = GA_generations
        self.mutation_rate = GA_mutation_rate
        self.num_parents = GA_num_parents

        self.mutation_strength = 100 # Adjust as needed for smoother transitions

        self.block_size_x = 10
        self.block_size_y = 10

        self.num_blocks_x = (SLMwidth // self.block_size_x) + 1
        self.num_blocks_y = (SLMheight // self.block_size_y) + 1# adding a plus one because it doesn't tile it properly for some reason
        
        self.weights = np.load('./settings/GA_adjusted_weights.npy')
        zoom_factors = [self.SLMheight / self.weights.shape[0],
                self.SLMwidth / self.weights.shape[1]]
        self.tiled_weights = gaussian_filter(zoom(self.weights , zoom_factors, order=3), sigma=50)
        self.tiled_weights = np.ones_like(self.tiled_weights)
        # self.tiled_weights = shift_array(self.tiled_weights, 50, 'left')
        # self.tiled_weights = shift_array(self.tiled_weights, 50, 'up')

        self.population_of_generation = np.zeros((self.population_size, SLMheight, SLMwidth))
        self.fitness_of_population = np.zeros((self.population_size, 1))
        self.amplitudes =  np.zeros((self.population_size, self.num_blocks_y, self.num_blocks_x))
        
        self.parents = np.zeros((self.num_parents, self.num_blocks_y, self.num_blocks_x))
        self.binary_pattern = Image.open('./settings/PreSets/HAMAMATSU/HAMAMATSU_1px.png')

        # self.binary_pattern = Image.open('THORLABSBLACK2.png')
        self.goal_image = None
        self.positive_goal_index = None
        self.negative_goal_index = None
        self.GA_convergence = np.zeros((self.generations, 3))
        x = np.linspace(0, self.num_blocks_x, self.num_blocks_x)
        y = np.linspace(0, self.num_blocks_y, self.num_blocks_y)
        self.x, self.y = np.meshgrid(x, y)

        self.basic_block_pattern = self.create_basic_block_pattern()

    
    def create_basic_block_pattern(self):
        # Create a 20x20 basic block with alternating 0s and 1s in the x-direction
        
        basic_block = np.zeros((self.block_size_y, self.block_size_x))
        basic_block[:, ::2] = 1
        # x_blocks = np.linspace(0, self.block_size_x, self.block_size_x)
        # y_blocks = np.linspace(0, self.block_size_y, self.block_size_y)
        # meshX, meshY = np.meshgrid(x_blocks, y_blocks)
        
        # basic_block = (sawtooth(2 * np.pi * 4000 * meshX/np.max(meshX))+1)/2
        return np.tile(basic_block, (self.num_blocks_y, self.num_blocks_x))
    

    def initialize_individual_block_based(self, population_number):
        initial_guess = np.random.uniform(0, 200, (self.num_blocks_y, self.num_blocks_x))
        # initial_guess = np.zeros(( (self.num_blocks_x, self.num_blocks_y)))
        # number_of_gauss = 1
        # # # these are some initial guesses
        # gaussian =100*np.exp(-((self.x-np.random.randint(0, self.SLMwidth/2))**2 +(self.y-np.random.randint(0, self.SLMheight/2))**2)/((2*1)**2)).T
        # for counter in range(0, number_of_gauss):
        #     gaussian =100*np.exp(-((self.x-np.random.randint(0, self.num_blocks_x))**2 +(self.y-np.random.randint(0, self.num_blocks_y))**2)/((2*1)**2)).T
        # initial_guess = gaussian / (number_of_gauss)

        return initial_guess


    def apply_block_pattern_to_grid(self, amplitudes):
  
        # Tile the amplitudes to match the size of the basic block pattern
        tiled_amplitudes = np.repeat(np.repeat(amplitudes, self.block_size_y, axis=0), self.block_size_x, axis=1)

        # Apply the modulated amplitudes to the basic block pattern
        try:
            pattern_grid = self.basic_block_pattern * np.transpose(tiled_amplitudes)
        except:
            pattern_grid = self.basic_block_pattern * tiled_amplitudes

        # Trim the pattern to fit the SLM dimensions        
        return pattern_grid[:self.SLMheight, :self.SLMwidth]
        
        # return pattern_grid

    def calculate_fitness(self, ccd_data):
        # max_difference = np.size(ccd_data[ccd_data>self.goal_image])

        # IntensityDifference =  ((np.sum(self.goal_image[380:800, 600:1030])/100 - np.sum(ccd_data[380:800, 600:1030])/100)**2)/1000
        # IntensityDifference =  ((np.sum(self.goal_image) - np.sum(ccd_data))**2)/1000
        # reward = IntensityDifference
        # fitness = reward
        # print(self.positive_goal_index)
        reward = (np.sum(ccd_data[self.positive_goal_index]) - np.sum(self.goal_image[self.positive_goal_index]))**2
        penalise = (np.sum(ccd_data[self.negative_goal_index]) - np.sum(self.goal_image[self.negative_goal_index]))**2
        fitness = reward + penalise

        # number_above = ccd_data[ccd_data>100]
        # reward = 20*number_above.size
         
        # mask = (ccd_data >= 10) & (ccd_data <= 100)
        # changed_pixels_below_threshold = np.sum(ccd_data[mask] != self.goal_image[mask])
        # penalty = 0.001 * changed_pixels_below_threshold
        # print(f'reward:{reward}, penalty:{penalty}')
        # print(f'max difference {max_difference}, intensity difference {IntensityDifference}')
        return fitness

    def select_parents(self):
        self.fitness_of_population = self.fitness_of_population[:, 0]
        # print(self.fitness_of_population)
        self.fitness_of_population[self.fitness_of_population <0.01] = np.NaN
        parents = np.argsort(self.fitness_of_population)[:self.num_parents]
        counter = 0
        for i in parents:
            self.parents[counter, :, :] =  self.amplitudes[i, :, :]
            counter +=1
        # print(np.nanmin(self.fitness_of_population))


    # def smooth_mutate(self, individual):
    #     for i in range(individual.shape[0]):
    #         for j in range(individual.shape[1]):
    #             if np.random.rand() < self.mutation_rate:
    #                 # Apply a smaller mutation, bounded by mutation_strength
    #                 change = np.random.uniform(-self.mutation_strength, self.mutation_strength)
    #                 individual[i, j] += change

    #             # Optionally, apply similar small changes to adjacent blocks
    #                 if i > 0:
    #                     individual[i - 1, j] += change / 4  # Adjust factor as needed
    #                 if i < individual.shape[0] - 1:
    #                     individual[i + 1, j] += change / 4
    #                 if j > 0:
    #                     individual[i, j - 1] += change / 4
    #                 if j < individual.shape[1] - 1:
    #                     individual[i, j + 1] += change / 4
    #     return individual

    def smooth_mutate(self, individual):
        # the asterisks unpacks it
        mutation_mask = np.random.rand(*individual.shape) < self.mutation_rate
        changes = np.random.uniform(-self.mutation_strength, self.mutation_strength, individual.shape)
        individual += changes * mutation_mask
        # individual +=changes
        return individual
    
    # def smooth_crossover(self, parent1, parent2):
    #     child = np.copy(parent1)
    #     for i in range(self.num_blocks_x):
    #         for j in range(self.num_blocks_y):
    #             if np.random.rand() < self.mutation_rate:
    #                 # Blend the values from both parents
    #                 child[i, j] = (parent1[i, j] + parent2[i, j]) / 2
    #     return child
    def smooth_crossover(self, parent1, parent2):
        child = (parent1 + parent2) / 2
        # return np.transpose(child)
        return child
    

