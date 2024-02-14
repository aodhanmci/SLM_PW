import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import laserbeamsize as lbs

filepath = '.\PW5loop.png'

image = Image.open(filepath)
image_array = np.asarray(image)

width, height = image.size
x = np.arange(width)
y = np.arange(height)

image_array = np.copy(image_array)

cx, cy, dx, dy, phi = lbs.beam_size(image_array)
detected_circle = np.uint16((cx,cy,(dx/3+dy/3)/2,phi))

center_y = image_array[detected_circle[1],:]
plt.plot(x, center_y)
plt.show()

cv2.line(image_array, (0, detected_circle[1]), (width, detected_circle[1]), color=255, thickness=1)
cv2.circle(image_array, (detected_circle[0],detected_circle[1]), detected_circle[2], 255, 1)
cv2.circle(image_array, (detected_circle[0],detected_circle[1]), 1, 255, 2)

image = Image.fromarray(image_array)

image.show()

umpx = 12.817

dx = 451.8813559
dy = 422.6779661
dx_cm = dx*umpx/10000
dy_cm = dy*umpx/10000

d_avg = (dx+dy)/2
d_avg_cm = (dx_cm+dy_cm)/2
energy = 0.035
fluence = (2*energy)/(3.14*(d_avg_cm)**2)

print("Average beam diameter (cm): " + str(d_avg_cm))
print("Assuming mircons per pixel: " + str(umpx))
print("Assuming laser energy = " + str(energy))
print("Peak fluence: " + str(np.round(fluence, 3)))
