import numpy as np
import matplotlib.pyplot as plt
grid_3x3 = np.array([[0, 0, 0],
                     [0, 1, 0],
                     [0, 0, 0]])

# Repeat each element of the grid 3 times along the rows and then 3 times along the columns
grid_9x9 = np.repeat(np.repeat(grid_3x3, 3, axis=0), 3, axis=1)

plt.imshow(grid_3x3)
plt.show()
plt.imshow(grid_9x9)
plt.show()