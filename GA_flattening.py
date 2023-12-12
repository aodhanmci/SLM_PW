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

        self.mutation_strength = 2  # Adjust as needed for smoother transitions
        self.population_of_generation = np.zeros((self.population_size, SLMwidth, SLMheight))
        self.fitness_of_population = np.zeros((self.population_size, 1))
        self.block_size_x = 40
        self.block_size_y = 40
        self.num_blocks_x = (SLMwidth // self.block_size_x)+1
        self.num_blocks_y = (SLMheight // self.block_size_y)+1 # adding a plus one because it doesn't tile it properly for some reason
        self.binary_pattern = Image.open('./settings/PreSets/HAMAMATSU/HAMAMATSU_1px.png')
        self.goal_image = None
        self.parents = None



    def initialize_individual_block_based(self):
        return np.random.uniform(0, 20, (self.num_blocks_x, self.num_blocks_y))

    ## takes your macro block and tiles it across the SLM size. then it trims it to get it to the right size
    def apply_block_pattern_to_grid(self, initial):
        expanded_pattern = np.repeat(np.repeat(initial, self.block_size_x, axis=0), self.block_size_y, axis=1)
        expanded_pattern = expanded_pattern[:self.SLMwidth, :self.SLMheight]
        return  expanded_pattern 

    def calculate_fitness(self, ccd_data):
        IntensityDifference = np.sum(self.goal_image - ccd_data)
        intensity_fitness = np.sum(IntensityDifference)
        fitness = -intensity_fitness
        return fitness

    def select_parents(self):
        parents = np.argsort(self.fitness_of_population)[-self.num_parents:]
        return [self.population_of_generation[i] for i in parents]

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
        return individual
    
    # def smooth_crossover(self, parent1, parent2):
    #     child = np.copy(parent1)
    #     for i in range(self.num_blocks_x):
    #         for j in range(self.num_blocks_y):
    #             if np.random.rand() < 0.5:
    #                 # Blend the values from both parents
    #                 child[i, j] = (parent1[i, j] + parent2[i, j]) / 2
    #     return child
    def smooth_crossover(self, parent1, parent2):
        child = (parent1 + parent2) / 2
        return child
    

