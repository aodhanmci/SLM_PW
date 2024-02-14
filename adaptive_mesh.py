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


# Example: 2D array
array_2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Let's say you have a 1D index
index_1d = 0  # For example

# Convert 1D index to 2D index
row, col = np.unravel_index(index_1d, array_2d.shape)

print("Row:", row, "Column:", col)
print("Value at index:", array_2d[row, col])