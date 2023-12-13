import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

class flattening_GA:
    def __init__(self, GA_population, GA_generations, GA_num_parents, GA_mutation_rate, SLMwidth, SLMheight):
        self.SLMwidth = SLMwidth
        self.SLMheight = SLMheight
        self.population_size = GA_population
        self.generations = GA_generations
        self.mutation_rate = GA_mutation_rate
        self.num_parents = GA_num_parents

        self.mutation_strength = 2 # Adjust as needed for smoother transitions
        self.population_of_generation = np.zeros((self.population_size, SLMwidth, SLMheight))
        self.fitness_of_population = np.zeros((self.population_size, 1))
        self.block_size_x = 80
        self.block_size_y = 80
        
        self.num_blocks_x = (SLMwidth // self.block_size_x)+1
        self.num_blocks_y = (SLMheight // self.block_size_y)+1 # adding a plus one because it doesn't tile it properly for some reason
        self.amplitudes =  np.zeros((self.population_size, self.num_blocks_x, self.num_blocks_y))
        self.parents = np.zeros((self.num_parents, self.num_blocks_x, self.num_blocks_y))
        self.binary_pattern = Image.open('./settings/PreSets/HAMAMATSU/HAMAMATSU_1px.png')
        self.goal_image = None



        self.basic_block_pattern = self.create_basic_block_pattern()

    def create_basic_block_pattern(self):
        # Create a 20x20 basic block with alternating 0s and 1s in the x-direction
        basic_block = np.zeros((self.block_size_x, self.block_size_y))
        basic_block[:, ::2] = 1
        return np.tile(basic_block, (self.num_blocks_x, self.num_blocks_y))

    def initialize_individual_block_based(self):
        # Initialize the amplitude matrix for each block
        return np.random.uniform(0, 250, (self.num_blocks_x, self.num_blocks_y))

    def apply_block_pattern_to_grid(self, amplitudes):
        # Tile the amplitudes to match the size of the basic block pattern
        tiled_amplitudes = np.repeat(np.repeat(amplitudes, self.block_size_x, axis=0), self.block_size_y, axis=1)

        # Apply the amplitudes to the basic block pattern
        pattern_grid = self.basic_block_pattern * tiled_amplitudes

        # Trim the pattern to fit the SLM dimensions
        return pattern_grid[:self.SLMwidth, :self.SLMheight]

    # def mutate_amplitudes(self, amplitudes):
    #     # Apply mutation to the amplitude matrix
    #     mutation_strength = 10  # Adjust as needed
    #     mutation_changes = np.random.uniform(-mutation_strength, mutation_strength, amplitudes.shape)
    #     mutated_amplitudes = np.clip(amplitudes + mutation_changes, 0, 200)
    #     return mutated_amplitudes

    def calculate_fitness(self, ccd_data):
        IntensityDifference =  ((np.sum(self.goal_image)/100 - np.sum(ccd_data)/100)**2)/1000
        fitness = IntensityDifference
        return -fitness

    def select_parents(self):
        parents = np.argsort(self.fitness_of_population[:, 0])[-self.num_parents:]
        counter = 0
        for i in parents:
            self.parents[counter, :, :] =  self.amplitudes[i, :, :]
            counter +=1


    def smooth_mutate(self, individual):
        for i in range(individual.shape[0]):
            for j in range(individual.shape[1]):
                if np.random.rand() < self.mutation_rate:
                    # Apply a smaller mutation, bounded by mutation_strength
                    change = np.random.uniform(-self.mutation_strength, self.mutation_strength)
                    individual[i, j] += change

                # Optionally, apply similar small changes to adjacent blocks
                    if i > 0:
                        individual[i - 1, j] += change / 4  # Adjust factor as needed
                    if i < individual.shape[0] - 1:
                        individual[i + 1, j] += change / 4
                    if j > 0:
                        individual[i, j - 1] += change / 4
                    if j < individual.shape[1] - 1:
                        individual[i, j + 1] += change / 4
        return individual

    # def smooth_mutate(self, individual):
    #     # the asterisks unpacks it
    #     # mutation_mask = np.random.rand(*individual.shape) < self.mutation_rate
    #     changes = np.random.uniform(-self.mutation_strength, self.mutation_strength, individual.shape)
    #     # individual += changes * mutation_mask
    #     individual +=changes
    #     return individual
    
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
        return child
    

