import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

weights = np.load('./settings/GA_weights.npy')
weights[0:5, :] = 0
weights[8:, :] = 0
weights[:, :5] = 0
weights[:, 8:] = 0
plt.imshow(weights, norm=LogNorm())
plt.show()
weights = np.save('./settings/GA_adjusted_weights.npy', weights)
