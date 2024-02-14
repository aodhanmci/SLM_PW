import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
# Parameters
width, height = 1280, 1080
x_pos, y_pos = 645, 280  # Center of the Gaussian
sigma_x, sigma_y = 10, 10  # Width and height of the Gaussian
grating_period = 5 # Grating period in pixels
power =0.5
amplitude = 250

x = np.linspace(0, width - 1, width)
y = np.linspace(0, height - 1, height)
X, Y = np.meshgrid(x, y)
binary_grating = np.zeros_like(X)
binary_grating[:, ::2] = 1
# binary_grating[::2, :] = 1
# binary_grating[:, ::2] = 1

wavefront_sigma_x, wavefront_sigma_y = 1*sigma_x, 1*sigma_y
    # Create blazed grating
blazed_grating = np.mod(X, grating_period) / grating_period
    # Create Gaussian function
gaussian_amp = np.exp(-(((X - x_pos) ** 2) / (2 * sigma_x ** 2) + ((Y - y_pos) ** 2) / (2 * sigma_y ** 2))**power)
gaussian_wavefront = np.exp(-(((X - x_pos) ** 2) / (2 * wavefront_sigma_x ** 2) + ((Y - y_pos) ** 2) / (2 * wavefront_sigma_y ** 2))**power)

radius = 3
xcenter = x_pos
ycenter = y_pos
SignMask = np.sign(1-np.sign((X-xcenter)**2+(Y-ycenter)**2-radius**2))
# SignMask = SignMask/np.max(SignMask)
print(np.max(SignMask))
# th = np.linsapce(0, 2*np.pi, 90)
# result = blazed_grating * gaussian
smooth_mask = gaussian_filter(SignMask, 5)
smooth_mask = smooth_mask/np.max(smooth_mask)
# binary_mask = SignMask*blazed_grating
wavefront_amp = 250
flat_phase = np.ones_like(X)
flat_wavefront = flat_phase*wavefront_amp

result = wavefront_amp + gaussian_amp*amplitude*binary_grating - wavefront_amp*gaussian_wavefront
# result =  wavefront_amp + gaussian_amp*amplitude - wavefront_amp*gaussian_wavefront
image =result

image = image.astype(np.uint8)
image_pillow = Image.fromarray(image)

# Save the image to a file
# image_path = ".\\testimg\\kHz\\binary_grating_gaussian_x_" + str(x_pos) + '_y_' + str(y_pos) + ".png"
image_path =  ".\\testimg\\kHz\\fake.png"
# image_path = "blazed_grating_gaussian.png"
image_pillow.save(image_path)

print(f"Image saved as {image_path}")