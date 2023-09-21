import tkinter as tk
from tkinter import ttk, PhotoImage, filedialog
from tkinter.filedialog import askopenfile
from tkinter.constants import *
import oneCameraCapture
from PIL import Image, ImageTk, ImageOps
import numpy as np
import cv2
import PIL
from SLM_HAMAMATSU import *
import screeninfo
from screeninfo import get_monitors
import pandas as pd
import os



# image = Image.open("TESTIMG.png")
# image_array = asarray(image)
# image_blurred = cv2.blur(image_array, (3,3))

# detected_circles = cv2.HoughCircles(image_blurred,
#                                     cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
#                                     param2 = 30, minRadius = 0, maxRadius = 0)

# if detected_circles != None:
#     print("Detected circles!")
#     detected_circles = np.uint16(np.around(detected_circles))

#     for pt in detected_circles[0,:]:
#         a, b, r = pt[0], pt[1], pt[2]

#         cv2.circle(image_array, (a,b), r, 255, 2)

#         cv2.circle(image_array, (a,b), 1, 255, 3)
#     image = Image.fromarray(image_array)
#     image.show()
# else:
#     print("No circles detected.")

# image_blurred = Image.fromarray(image_blurred)

# image_blurred.show()


image = iio.imread("TESTIMG.png")
x, y, dx, dy, phi = lbs.beam_size(image)
detected_circle = np.uint16((x,y,dx,dy,phi))
cv2.circle(image, (detected_circle[0],detected_circle[1]), detected_circle[2], 255, 2)
cv2.circle(image, (detected_circle[0],detected_circle[1]), detected_circle[3], 255, 2)
cv2.circle(image, (detected_circle[0],detected_circle[1]), 1, 255, 3)

cv2.imshow("Detected Circle", image)
cv2.waitKey(0)