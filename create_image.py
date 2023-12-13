import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
SLMwidth = 1280
SLMheight = 1024

pixel_x = np.linspace(0, SLMwidth, SLMwidth)
pixel_y = np.linspace(0, SLMheight, SLMheight)
MeshX, MeshY = np.meshgrid(pixel_x, pixel_y)
Meshr = (MeshX- SLMwidth/2)**2 + (MeshY- SLMheight/2)**2
basic_block = np.zeros((SLMwidth, SLMheight))
gaussian_mask = np.ones_like(basic_block)
radius = 100
gaussian_mask=gaussian_mask*np.exp(-(Meshr.T/(radius**2)))
basic_block[::2, :] = 200

image = basic_block*gaussian_mask

fig, ax = plt.subplots()
ax.imshow(image)
plt.show()

fig2, ax2 = plt.subplots()
ax2.plot(pixel_y, image[int(SLMwidth/2), :])
plt.show()
image = image.T
image = Image.fromarray(image.astype(np.uint8))

# Save the image
image.save("./data/greyscale_image.png")