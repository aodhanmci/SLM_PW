import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Given numbers
# chosen = [ 1, 23, 19, 15, 14, 24, 26, 21, 17, 11]
# fitness = np.array([2513662.3134281, 3011882.7389929, 3835387.8163049, 3933467.14544  ,
#        3586602.5720656, 4021761.5185476, 3471092.5443136, 3721114.7832281,
#        3624285.8877696, 3526068.0517225, 3375607.5458225, 3362179.3675161,
#        3540892.3683216, 3583094.9105601, 3264474.4502544, 3249380.8702121,
#        3482919.6750625, 3330321.52836  , 3441859.0199225, 3131817.4312784,
#        2987644.5060036, 3314514.6452081, 3405985.4980676, 3016542.1357225,
#        3288990.61056  , 3483356.0640704, 3289930.1643136, 3478838.9472576,
#                    np.nan,             np.nan])

# parents = np.argsort(fitness)[:10]
# print(chosen)
# print(parents)
block_size_x = 10
block_size_y = 10
basic_block = np.zeros((block_size_x, block_size_y))
basic_block[:, ::2] = 1
plt.imshow(basic_block)
plt.show()