import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def create_blazed_grating_with_gaussian(x_pos, y_pos, sigma, grating_period, power, peak):
    # Create coordinate grids


    # Create Gaussian function
    gaussian = np.exp(-(((X - x_pos) ** 2) / (2 * sigma ** 2) + ((Y - y_pos) ** 2) / (2 * sigma ** 2))**power)

    return gaussian

width, height = 1280, 1080
x = np.linspace(0, width - 1, width)
y = np.linspace(0, height - 1, height)
X, Y = np.meshgrid(x, y)

binary_grating = np.zeros_like(X)
binary_grating[:, ::2] = 255

gaussian_positions = [[400, 400], 
                      [600, 400],
                      [400, 600],
                      [600, 600]]
# Parameters
sigmas = [25, 25, 25, 25]

# x_pos, y_pos = 640, 540  # Center of the Gaussian
sigma_x, sigma_y = 75, 75  # Width and height of the Gaussian
grating_period = 20 # Grating period in pixels
power = 1
peak = 122
# Create the image
gaussian_envelope = np.zeros_like(X)
counter =0
for positions in gaussian_positions:
    print(positions)
    x_pos = positions[0]
    y_pos = positions[1]
    sigma = sigmas[counter]
    gaussian = create_blazed_grating_with_gaussian(x_pos, y_pos, sigma, grating_period, power, peak)
    gaussian_envelope +=gaussian
    counter +=1

# image = create_blazed_grating_with_gaussian(x_pos, y_pos, sigma_x, sigma_y, grating_period, power, peak)
final_image = binary_grating*gaussian_envelope
final_image = final_image.astype(np.uint8)
# # Convert the NumPy array to a Pillow Image object
image_pillow = Image.fromarray(final_image)

# # Save the image to a file
image_path = ".\\testimg\\gaussian_calibration.png"
# image_path = "blazed_grating_gaussian.png"
image_pillow.save(image_path)

print(f"Image saved as {image_path}")