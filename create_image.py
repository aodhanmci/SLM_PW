import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.signal import sawtooth

SLMwidth = 1280
SLMheight = 1024

pixel_x = np.linspace(0, SLMwidth, SLMwidth)
pixel_y = np.linspace(0, SLMheight, SLMheight)
MeshX, MeshY = np.meshgrid(pixel_x, pixel_y)
Meshr = (MeshX- SLMwidth/2)**2 + (MeshY- SLMheight/2)**2
MeshX=MeshX.T
basic_block = np.zeros((SLMwidth, SLMheight))
gaussian_mask = np.ones_like(basic_block)
basic_block[::2, :] = 255
# sawtooth_wave = ((sawtooth(2 * np.pi * 400 * MeshX/np.max(MeshX))+1)/2)*255


radius = 100
gaussian_mask=gaussian_mask*np.exp(-(Meshr.T/(radius**2)))


# image = basic_block*gaussian_mask
# image=sawtooth_wave*gaussian_mask
# image=sawtooth_wave
image = basic_block

fig, ax = plt.subplots()
ax.imshow(image)
plt.show()

fig2, ax2 = plt.subplots()
ax2.plot(pixel_x, image[:, int(SLMheight/2)])
ax2.set_xlim(0, 50)
plt.show()
image = image.T
image = Image.fromarray(image.astype(np.uint8))

# Save the image
image.save("./data/greyscale_image400.bmp")