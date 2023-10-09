#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 09:11:20 2023

@author: anthonylu
"""

from PIL import Image, ImageTk, ImageOps
import matplotlib.pyplot as plt
import cv2, numpy as np

SLMimg = Image.open("/Users/anthonylu/Documents/GitHub/SLM_PW/calibration/HAMAMATSU/crosshairNums.png")
CCDimg = Image.open("/Users/anthonylu/Documents/GitHub/SLM_PW/crosshairNumsResult.png")
CCDimg = CCDimg.resize(SLMimg.size, Image.Resampling.LANCZOS)
CCDwidth, CCDheight = CCDimg.size
SLMwidth, SLMheight = SLMimg.size

def clickCorners(SLMimg, CCDimg):
    output_path = '/Users/anthonylu/Documents/GitHub/SLM_PW/CCD_clicks.csv'
    
    # Mouse callback function
    global CCD_click_list, SLM_click_list
    positions, CCD_click_list = [], []
    def callback(event, x, y, flags, param):
        if event == 1: CCD_click_list.append((x,y))
    cv2.namedWindow('img')
    cv2.setMouseCallback('img', callback)
    
    img = np.asarray(CCDimg)
    
    print("Step 1/2: Please click the four crosshair corners in numerical order. The window will switch once you have clicked all four corners.")
    
    # Mainloop - show the image and collect the data
    while True:
        cv2.imshow('img', img)    

        if len(CCD_click_list) == 4:
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            break
        k = cv2.waitKey(1)
        # If user presses 'esc' break 
        if k == 27:
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            break
    
    # Write data to a spreadsheet
    import csv
    with open(output_path, 'w') as csvfile:
        fieldnames = ['x_position', 'y_position']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        for position in CCD_click_list:
            x, y = position[0], position[1]
            writer.writerow({'x_position': x, 'y_position': y})
    
    # Do the same for the crosshairs
    
    output_path = '/Users/anthonylu/Documents/GitHub/SLM_PW/SLM_clicks.csv'

    positions, SLM_click_list = [], []
    def callback(event, x, y, flags, param):
        if event == 1: SLM_click_list.append((x,y))
    cv2.namedWindow('img')
    cv2.setMouseCallback('img', callback)
    
    img = np.asarray(SLMimg)
    
    print("Step 2/2: Please click the four crosshair corners in numerical order. The window will disappear once you have clicked all four corners.")
    
    # Mainloop - show the image and collect the data
    while True:
        cv2.imshow('img', img)    

        if len(SLM_click_list) == 4:
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            break
        k = cv2.waitKey(1)
        # If user presses 'esc' break 
        if k == 27:
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            break
    
    # Write data to a spreadsheet
    import csv
    with open(output_path, 'w') as csvfile:
        fieldnames = ['x_position', 'y_position']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        for position in SLM_click_list:
            x, y = position[0], position[1]
            writer.writerow({'x_position': x, 'y_position': y})
    
    CCD_click_list = list(CCD_click_list)
    SLM_click_list = list(SLM_click_list)

clickCorners(SLMimg, CCDimg)



def dots(image, click_list):
    # for i in np.arange(len(click_list)):
    #     cv2.circle(image, (click_list[i][0], click_list[i][1]), 1, int(255-i*255/4), 500)
    Image.fromarray(image).show()


# print(CCD_click_list)
# print(SLM_click_list)
p1, p2, p3, p4 = CCD_click_list
p1, p2, p3, p4 = list(p1), list(p2), list(p3), list(p4)


# # Mirror or flip to correct orientation
# if p1[0] > p2[0]:
#     print("Mirroring")
#     CCDimg = ImageOps.mirror(CCDimg)
#     p1[0] = int(CCDwidth/2 - abs(CCDwidth/2 - p1[0]))
#     p2[0] = int(CCDwidth/2 + abs(CCDwidth/2 - p2[0]))
#     p3[0] = int(CCDwidth/2 - abs(CCDwidth/2 - p3[0]))
#     p4[0] = int(CCDwidth/2 + abs(CCDwidth/2 - p4[0]))
# if p1[1] > p3[1]:
#     print("Flipping")
#     CCDimg = ImageOps.flip(CCDimg)
#     p1[1] = int(CCDheight/2 - abs(CCDheight/2 - p1[1]))
#     p2[1] = int(CCDheight/2 + abs(CCDheight/2 - p2[1]))
#     p3[1] = int(CCDheight/2 - abs(CCDheight/2 - p3[1]))
#     p4[1] = int(CCDheight/2 + abs(CCDheight/2 - p4[1]))

new_CCD_click_list = [p1, p2, p3, p4]

img = np.asarray(CCDimg)

input_pts = np.float32([new_CCD_click_list])
output_pts = np.float32([SLM_click_list])

# Compute the perspective transform M
M = cv2.getPerspectiveTransform(input_pts,output_pts)

# Apply the perspective transformation to the image
out = cv2.warpPerspective(img,M,(img.shape[1], img.shape[0]),flags=cv2.INTER_LINEAR)

# Display the transformed image
plt.imshow(out)

dots(np.asarray(SLMimg), SLM_click_list)
dots(np.asarray(CCDimg), new_CCD_click_list)

Image.fromarray(out).show()






























