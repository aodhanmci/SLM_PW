import numpy as np

class GA_weight:
    def __init__(self, SLMwidth, SLMheight):
        self.SLMwidth = SLMwidth
        self.SLMheight = SLMheight
        self.weight_block_size_x = 40
        self.weight_block_size_y = 40

        self.weight_num_blocks_x = (SLMwidth // self.weight_block_size_x)+1
        self.weight_num_blocks_y = (SLMheight // self.weight_block_size_y)+1 # adding a plus one because it doesn't tile it properly for some reason
        self.weight_population_size = self.weight_num_blocks_x *self.weight_num_blocks_y
        self.weights = np.zeros((self.weight_num_blocks_x, self.weight_num_blocks_y))



        self.weight_basic_block_pattern = self.create_basic_block_weight_pattern()

    def create_basic_block_weight_pattern(self):
        # Create a 20x20 basic block with alternating 0s and 1s in the x-direction
        
        basic_block = np.zeros((self.weight_block_size_x, self.weight_block_size_y))
        basic_block[:, ::2] = 1
        # x_blocks = np.linspace(0, self.block_size_x, self.block_size_x)
        # y_blocks = np.linspace(0, self.block_size_y, self.block_size_y)
        # meshX, meshY = np.meshgrid(x_blocks, y_blocks)
        
        # basic_block = (sawtooth(2 * np.pi * 4000 * meshX/np.max(meshX))+1)/2
        return np.tile(basic_block, (self.weight_num_blocks_x, self.weight_num_blocks_y))


    def initialize_weight_individual_block_based(self, population_number):
        # initial_guess = np.random.uniform(0, 255, (self.num_blocks_x, self.num_blocks_y))
        initial_guess = np.zeros(( (self.weight_num_blocks_x, self.weight_num_blocks_y)))

        # Convert 1D index to 2D index
        row, col = np.unravel_index(population_number, initial_guess.shape)
        initial_guess[row, col] = 255
        return initial_guess

    def apply_weight_block_pattern_to_grid(self, amplitudes):
  
        # Tile the amplitudes to match the size of the basic block pattern
        tiled_amplitudes = np.repeat(np.repeat(amplitudes, self.weight_block_size_x, axis=0), self.weight_block_size_y, axis=1)

        # Apply the modulated amplitudes to the basic block pattern
        pattern_grid = self.weight_basic_block_pattern * tiled_amplitudes

        # Trim the pattern to fit the SLM dimensions
        return pattern_grid[:self.SLMwidth, :self.SLMheight]
    
    def input_weights(self, population_number, ccd_data):
        IntensityDifference =  np.sum(ccd_data)/100
        row, col = np.unravel_index(population_number, self.weights.shape)
        self.weights[row, col] = IntensityDifference
        print(f'pop: {population_number}, row:{row}, column:{col}, int diff:{IntensityDifference}')