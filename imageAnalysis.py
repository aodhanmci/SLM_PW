#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 11:00:07 2023

@author: anthonylu
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageOps, ImageFont, ImageDraw
from scipy.optimize import curve_fit
from numpy import asarray


d = {}


# for i in np.arange(110, 120, 2):
for i in (20, 40, 60, 100, 160):
    # d["x{0}".format(a)], d["y{0}".format(a)], d["amp{0}".format(a)] = peaks[a]
    d["255_blazed_{0}gap_standard".format(i)] = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/twoRectContrast/255_blazed_" + str(i) + "gap_1_standard.png")
    d["255_blazed_{0}gap_standard_map".format(i)] = d["255_blazed_{0}gap_standard".format(i)].load()
    d["255_blazed_{0}gap_standard_array".format(i)] = asarray(d["255_blazed_{0}gap_standard".format(i)])
    # d["190_{0}_extended".format(i)] = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/twoRectContrast/190_" + str(i) + "_extended.png")
    # d["190_{0}_extended_map".format(i)] = d["190_{0}_extended".format(i)].load()
    # d["190_{0}_extended_array".format(i)] = asarray(d["190_{0}_extended".format(i)])

blazed_255 = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/twoRectContrast/255_blazed_40gap_1_standard_halfBlocked.png")
rect_255 = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/twoRectContrast/255_standard.png")
blazed_255_map = blazed_255.load()
rect_255_map = rect_255.load()

width = 1920
height= 1080

for img in (20, 40, 60, 100, 160):
# for img in ("blazed_255", "rect_255"):
    strip = []
    strip_s = []
    strip_e = []
    for i in np.arange(width):
        # strip = []
        strip_s = np.append(strip_s, d["255_blazed_" + str(img) + "gap_standard_map"][i,height/2])
        # strip_e = np.append(strip_e, d["190_"+str(img)+"_extended_map"][i,height/2])
    # plt.plot(np.arange(width), strip_s, label = str(img) + "_gap_standard")
    # plt.plot(np.arange(width), strip_e, label = str(img) + "_amp_extended")

strip1 = []
strip2 = []
for i in np.arange(width):
    strip1 = np.append(strip1, blazed_255_map[i,height/2])
    strip2 = np.append(strip2, rect_255_map[i,height/2])
plt.plot(np.arange(width), strip1, label = "Blazed")
plt.plot(np.arange(width), strip2, label = "Rectangle")
    

plt.xlim(850, 1050)
# plt.ylim(0,255)
# plt.title("Varying Gap Sizes, 1st Order, Different Axis Scaling")
plt.legend()
plt.show()
# display(d["100"])