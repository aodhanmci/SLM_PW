#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 10:29:53 2023

@author: anthonylu
"""

# 1080 x 1920
from PIL import Image, ImageOps, ImageFont, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
# import cv2
import math
from scipy import signal
# import display
# pip3 install diffractio
# import diffractio
# from diffractio import um, nm, mm, np
# from diffractio.scalar_sources_X import Scalar_source_X
# from diffractio.scalar_masks_X import Scalar_mask_X

# width = 1920
# height = 1080

# width = 1028
# height = 1080

# # Create a completely black image

# img = Image.new(mode = "RGB", size = (width, height), color = (255,255,255))
# img = Image.new(mode = "RGB", size = (width, height), color = (0,0,0))
# img = ImageOps.grayscale(img)
# img.save("/Users/anthonylu/Documents/LBNL/SLM/black.png")




# # # Open the black image to edit

img = Image.open("/Users/anthonylu/Documents/LBNL/SLM/black.png")
img = ImageOps.grayscale(img)
imgMap = img.load()
width, height = img.size


# # Create a striped test image

# img = Image.open("/Users/anthonylu/Documents/LBNL/SLM/black.png")
# img = ImageOps.grayscale(img)
# pixelMap = img.load()
# width, height = img.size
# for h in np.arange(height):
#     for w in np.arange(width):
#         if 2*height/5 <= h <= 3*height/5 and width/3 <= w <= 2*width/3:
#             pixelMap[w,h] = int(255/2)
#         if 2*height/5 <= h <= 3*height/5 and 2*width/3 <= w <= width:
#             pixelMap[w,h] = int(255)    
#         if 2*width/3 - 80 <= w <= 2*width/3 + 80:
#             pixelMap[w,h] = 0
#         if width/3 - 80 <= w <= width/3 + 80:
#             pixelMap[w,h] = 255
# display(img)
# # img.save("/Users/anthonylu/Documents/LBNL/SLM/testImage.png")



# # Make the shape, assign the pixel values from 0 to 255

# # circleSoft

# for i in np.arange(width):
#     for j in np.arange(height):
#         d = np.sqrt((i - width/2)**2 + (j - height/2)**2)
#         # if d < height/2 - 100 and d != 0:
#         if d != 0:
#             pixelMap[i,j] = int((width/d)*30)

# Save the image

# display(img)
# img.save("/Users/anthonylu/Google Drive/My Drive/SLM/testImages/circles/circleSoftLarger.png")


# # gradient

# for i in np.arange(width):
    # d = np.sqrt((i - width/2)**2 + (j - height/2)**2)
        # if d < height/2 - 100 and d != 0:
    # if d != 0:
    # pixelMap[i,j] = int((height/d)*30)

# # Save the image

# grayImg.save("/Users/anthonylu/Documents/LBNL/SLM/circleSoft.png")



# # Super Gaussian

# x = np.round(np.linspace(-width/2, width/2, width),0)
# y = np.round(np.linspace(-height/2, height/2, height),0)
# xx, yy = np.meshgrid(x, y)
# super_gaussian = np.exp(-((xx**2+yy**2)/300**2)**2)
# # print(y)
# # print(super_gaussian[1079][1919])
# for i in np.arange(width):
#     for j in np.arange(height):
#         # print(j)
#         imgMap[i,j] = int(super_gaussian[int(j)][int(i)]*255)
#         if imgMap[i,j] >= 150:
#             imgMap[i,j] = 150
# # for i in x:
# #     for j in y:
# #         # print(i,j)
# #         pixelMap[i-1,j-1] = int(super_gaussian[int(i+979)][int(j+539)])
# # print(pixelMap[width/2, height/2])
# strip = []
# for i in np.arange(1920):
#     strip = np.append(strip, imgMap[i, 1080/2])
# plt.plot(np.arange(width), strip)
# plt.show()

# # grayImg.save('blazed.png')
# # img.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/feedbackAlgorithm/targetImage.png")
# display(img)



# grayImg.save("/Users/anthonylu/Documents/LBNL/SLM/superGaussian.png")


# Add diffraction grating to airy disk 1

# x = np.linspace(-500, 500, 4096)
# t0 = Scalar_mask_X(x, 706)
# t0.slit(x0=0, size = 250)
# t0.draw(filename='test.png')


# Define function to automatically add diffraction pattern to an image

# def makeImage(saveAs, wavelength = width, initialImage=None, x_shift = (3/2)*np.pi, y_shift = 1, amplitude = 255):
#     global width
#     # nonlocal width
#     # wavelength = width
#     # print("Width at beginning: " + str(width))
#     # print("WL at beginning: " + str(wavelength))
#     width = 0
#     if initialImage != None:
#         # print("Width2 = " + str(width))
#         # print("WL2 = " + str(wavelength))
#         img = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM" + str(initialImage) + ".png")
#         width, height = img.size
#         # print("Width of uploaded image: " + str(width))
#         # print("Wavelength: " + str(wavelength))
#         img = ImageOps.grayscale(img)
#         imgMap = img.load()
#         amplitude2 = amplitude/2
#     else:
#         img = Image.open("/Users/anthonylu/Documents/LBNL/SLM/black.png")
#         width, height = img.size
#         # print("Width of black image: " + str(width))
#         # print("Wavelength: " + str(wavelength))
#         img = ImageOps.grayscale(img)
#         imgMap = img.load()
#         amplitude2 = amplitude/2
#     # print("Width3 = " + str(width))
#     # print("WL3 = " + str(wavelength))
#     wavelength = width/100
#     # print("WL4 = " + str(wavelength))
#     k = (2*np.pi)/wavelength
#     strip = []
#     newImg = []
#     for i in np.arange(width):
#         for j in np.arange(height):
#             val = (np.sin((k * i) + x_shift) + y_shift) * amplitude2
#             pixel = img.getpixel((i,j))
#             imgMap[i, j] = int(pixel*0.5 + val*0.5)
#             if j == height/2:
#                 strip = np.append(strip, pixel)
#                 newImg = np.append(newImg, imgMap[i,j])
#             # imgMap[i,j] = int(val)
#     # plt.plot(np.arange(width), (np.sin((k * np.arange(width)) + x_shift) + y_shift) * amplitude2)
#     # plt.show()
#     plt.plot(np.arange(width), strip, label = "Original Image")
#     plt.plot(np.arange(width), newImg, label = "New Image")
#     plt.legend()
#     plt.show()
#     display(img)
#     # print("Width at end: " + str(width))
#     # img.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/" + str(saveAs) + ".png")
#     # return print("Done")
    
# # makeImage(initialImage = "/testImages/dogs/EXULUS_CGH_Sample500", wavelength = width)
# # # print("Between width & WL: " + str(width) + str(wavelength))
# # # print("")
# # # makeImage(wavelength = width)
# makeImage(initialImage = "/testImages/vortex/vortex20", 
#           saveAs = "/vortex/vortex20_diffGrating_widthOver100_0.7_to_0.3")











# img = Image.open("/Users/anthonylu/Documents/LBNL/SLM/testImage.png")
# img = ImageOps.grayscale(img)
# pixelMap = img.load()
# width, height = img.size

# for i in np.arange(width):
#     for j in np.arange(height):
        


# display(img)


















# Create sinusoidal diffraction grating


# x = np.arange(width)
# # Wavelength is the distance between peaks, in PIXELS
# # 5lpmm = 31.68
# wavelength = 1920/5
# k = (2*np.pi)/wavelength
# x_shift = (3/2)*np.pi
# y_shift = 1
# amplitude = 255/2
# sinVal = (np.sin((k * x) + x_shift) + y_shift) * amplitude
# width, height = img.size
# # print(sinVal[-1])
# # plt.plot(x, sinVal)
# # plt.xlim([0,2*np.pi])
# # plt.show()

# strip = []
# for i in np.arange(width):
#     for j in np.arange(height):
#         val = (np.sin((k * i) + x_shift) + y_shift) * amplitude
#         imgMap[i, j] = int(val)
#         if j == height/2:
#             strip = np.append(strip, imgMap[i,j])
# display(img)

# plt.plot(np.arange(width), strip)
# plt.xlabel("X (px)")
# plt.ylabel("Y (px)")
# plt.title("Cross Section of Sinusoidal Grating, 0.0025 lines per mm")
# plt.savefig("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/Presentation/0.0025lpmmSinusoidalCS.png")
# plt.show()
# img.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/Presentation/0.0025lpmmSinusoidal.png")



# Try to rotate the grating




# Add diffraction grating to dog


# dog = Image.open("/Users/anthonylu/Documents/LBNL/SLM/EXULUS_CGH_Sample500.png")
# dog = ImageOps.grayscale(dog)
# dogMap = dog.load()


# for i in np.arange(476):
#     for j in np.arange(500):
#         val = (np.sin((k * i) + x_shift) + y_shift/2) * amplitude
#         pixel = dog.getpixel((i,j))
#         dogMap[i, j] = int(pixel/2 * int(val))
# display(dog)
# dog.save("/Users/anthonylu/Google Drive/My Drive/SLM/testImages/dogs/dogWithGrating80.png")



# # Create constant grayscale ramp



# # img = Image.open("/Users/anthonylu/Documents/LBNL/SLM/black.png")
# # img = Image.open("/Users/anthonylu/Documents/LBNL/SLM/testImage.png")
# img = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/vortex/vortex20.png")
# img = ImageOps.grayscale(img)
# pixelMap = img.load()
# width, height = img.size
# # x = np.arange(0, width, 0.0001)
# # Wavelength is the distance between peaks, in PIXELS
# wavelength = width/100
# k = (2*np.pi)/wavelength
# x_shift = (3/2)*np.pi
# y_shift = 1
# amplitude = 255/2
# # sinVal = (np.sin((k * x) + x_shift) + y_shift) * amplitude
# # print(sinVal[-1])
# # plt.plot(x, sinVal)
# # plt.xlim([0,2*np.pi])
# # plt.show()

# def makeGrating(n):
#     strip = []
#     newImg = []
#     # for i in np.arange(width/n):
#     #     for j in np.arange(height):
#     #         val = 255/(width)
#     #         # print(i*val)
#     #         pixel = img.getpixel((i,j))
#     #         pixelMap[i, j] = int(pixel/2 + i*val)
#     for l in np.arange(n):
#         for i in np.arange(width/n):
#             for j in np.arange(height):
#                 val = 255/(width/n)
#                 # print(i*val)
#                 pixel = img.getpixel((((l*width)/n + i,j)))
#                 imgMap[(l*width)/n + i, j] = int((pixel/2) + i*val/2)
#                 if j == height/2:
#                     if len(strip) >= width:
#                         break
#                     strip = np.append(strip, pixel)
#                     newImg = np.append(newImg, pixelMap[i,j])
#     plt.plot(np.arange(width), strip, label = "Original Image")
#     plt.plot(np.arange(width), newImg, label = "New Image")
#     plt.legend()
#     plt.show()
#     display(img)

# makeGrating(10)

# # img.save('/Users/anthonylu/Documents/LBNL/SLM/testGrating2.png')
# # img.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/diffGratings/vortex20_with_blazed100.png")

# # img = Image.open('/Users/anthonylu/Documents/LBNL/SLM/testGrating2.png')
# img = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/vortex/vortex20.png")
# img = ImageOps.grayscale(img)
# pixelMap = img.load()
# width, height = img.size

# testStrip = []
# for i in np.arange(width):
#     testStrip = np.append(testStrip, pixelMap[i, height/2])

# plt.plot(np.arange(width), testStrip)
# plt.show()
# display(img)




# # Create sawtooth grating

# # print(np.arange(36))

# def blazed(steps, numReps):
#     width = 36
#     height = 500
#     y = []
#     n = 0
#     # for i in np.arange(width):
#     #     for j in np.arange(steps):
#     #         if n <= width/(numReps * j):
#     #             print(n/steps)
#     #             y = np.append(y, n/steps)
#     for i in np.arange(width):
#         gap = width/(numReps * steps)
#         # print("Gap: " + str(gap))
#         if i <= width/(numReps * steps):
#             # print(n/steps)
#             a = 0
#             val = n/steps
#             # if val.is_integer() == True:
#             #     a = n/steps
#             #     # print(a)
#             y = np.append(y, 1/steps)
#             # y.append(1/steps)
#             print(val)
#         if i >= width/(numReps * steps):
#             n += 1
#             val = n/steps
#             if val.is_integer() == True:
#                 a = n/steps
#                 # print(a)
#             print(val)
#             y = np.append(y, 1/steps + a)

#     print(y)
        
    
#     plt.plot(np.arange(width), y)
#     plt.show()
    
# # blazed(4, 2)



# def blazed2(steps, numReps):
#     width = 36
#     y = []
#     n = 0
#     gap = width/(numReps * steps)
#     for i in np.arange(width):
#         if i == np.round(gap,0):
#             n += 1/steps
#         y = np.append(y, n)
    
#     plt.plot(np.arange(width), y)
#     plt.show()


# blazed2(4,2)






# # Test blazed pattern

# img = Image.open("/Users/anthonylu/Documents/LBNL/SLM/black500.png")
# img = ImageOps.grayscale(img)
# pixelMap = img.load()

# width, height = img.size

# x = 0

# for i in np.arange(width/(20)):
#     a = 0
#     for j in np.arange(width/(20*4)):
#         b = 0
#         for k in np.arange(height):
#             val = int((k/4)*255)
#             print(x, k, val)
#             pixelMap[x,k] = val
#             if x == 500:
#                 x = 0
#                 break
#         b += 1
#         if x == 500:
#             break
#     a += 1
#     if x == 500:
#         break

# display(img)



# # Aodhan's grating code

# width = 1920
# # width = 5004
# height = 1080

# img = Image.new('P', size = (width, height))
# grayImg = ImageOps.grayscale(img)
# pixelMap = grayImg.load()
# x = np.linspace(0, 1, int(width))
# y = np.linspace(0, 1, int(height))
# [MeshX, MeshY]=np.meshgrid(x,y) 
# # signal = ((signal.sawtooth(2 * np.pi * 10 * MeshY * (height/width))+1)/2)*255
# signal = ((signal.sawtooth(2 * np.pi * 100 * MeshX)+1)/2)*255
# # signal2 = np.zeros(len(x))
# grayImg.putdata(signal.ravel().astype(int))
# # grayImg.save('blazed.png')
# display(grayImg)

# strip = []
# for i in np.arange(width):
#     strip = np.append(strip, pixelMap[i, height/2])
# plt.plot(np.arange(width), strip)
# plt.show()



def makeBlazed(saveAs = "testImg", n = 10, imageScale = 0.5, blazeScale = 0.5, initialImage=None, x_shift = (3/2)*np.pi, y_shift = 1, amplitude = 255, angle = 0, SG = None, save = None, circle = None, invert = None, strip = None, yshift = 255, text = False, saveStrip = False, half = 0, flip = False):
    global width
    
    # SLM screen size: 12.5mm (width) x 7.1mm (height)

    
    from scipy import signal
    # nonlocal width
    # wavelength = width
    # print("Width at beginning: " + str(width))
    # print("WL at beginning: " + str(wavelength))
    width = 0
    if initialImage != None:
        # print("Width2 = " + str(width))
        # print("WL2 = " + str(wavelength))
        img = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM" + str(initialImage) + ".png")
        width, height = img.size
        # print("Width of uploaded image: " + str(width))
        # print("Wavelength: " + str(wavelength))
        img = ImageOps.grayscale(img)
        imgMap = img.load()
    elif SG != None:
        img = Image.open("/Users/anthonylu/Documents/LBNL/SLM/black.png")
        img = ImageOps.grayscale(img)
        imgMap = img.load()
        width, height = img.size
        x = np.round(np.linspace(-width/2, width/2, width),0)
        y = np.round(np.linspace(-height/2, height/2, height),0)
        xx, yy = np.meshgrid(x, y)
        super_gaussian = np.exp(-((xx**2+yy**2)/SG**2)**2)
        # print(y)
        # print(super_gaussian[809][819])
        for i in np.arange(width):
            for j in np.arange(height):
                # print(j)
                if invert:
                    imgMap[i,j] = int(super_gaussian[int(j)][int(i)]*(-255)+yshift)
                else:
                    imgMap[i,j] = int(super_gaussian[int(j)][int(i)]*255)
        # for i in x:
        #     for j in y:
        #         # print(i,j)
        #         pixelMap[i-1,j-1] = int(super_gaussian[int(i+979)][int(j+539)])
        # print(pixelMap[width/2, height/2])
        # strip = []
        # for i in np.arange(1920):
        #     strip = np.append(strip, pixelMap[i, 1080/2])
        # plt.plot(np.arange(width), strip)
        # plt.show()
        # display(img)
        # grayImg.save('blazed.png')
        # img.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/superGaussian200.png")
        # display(img)
    else:
        img = Image.open("/Users/anthonylu/Documents/LBNL/SLM/black.png")
        width, height = img.size
        # print("Width of black image: " + str(width))
        # print("Wavelength: " + str(wavelength))
        img = ImageOps.grayscale(img)
        imgMap = img.load()
    # print("Width3 = " + str(width))
    # print("WL3 = " + str(wavelength))
    # wavelength = width/100
    # print("WL4 = " + str(wavelength))
    # k = (2*np.pi)/wavelength
    # strip = []
    # newImg = []


    # Add blazed grating to image
    
    if initialImage != None:
        amplitude2 = amplitude
    else:
        amplitude2 = amplitude
        imageScale = 1
        blazeScale = 1
    
    blaze = Image.new('P', size = (width, height))
    blaze2 = Image.new('P', size = (width, height))
    blaze = ImageOps.grayscale(blaze)
    blaze2 = ImageOps.grayscale(blaze2)
    # blazeMap = blaze.load()
    x = np.linspace(0, 1, width)
    y = np.linspace(0, 1, height)
    [MeshX, MeshY]=np.meshgrid(x,y) 

    # blaze.putdata(signal.ravel().astype(int))
    from scipy import signal
    
    m = n*12.5
    
    if angle == 0:
        if flip:
            signal = ((signal.sawtooth(-2 * np.pi * m * MeshX)+y_shift)/2)*amplitude2
        else:
            signal = ((signal.sawtooth(2 * np.pi * m * MeshX)+y_shift)/2)*amplitude2
    if angle == 90:
        signal = ((signal.sawtooth(2 * np.pi * m * MeshY * height/width)+y_shift)/2)*amplitude2
    
    # if angle == 0:
        # signal = ((signal.sawtooth(2 * np.pi * m * MeshY * (height/width))+y_shift)/2)*amplitude2
        # signal = ((signal.sawtooth(2 * np.pi * m * MeshX)+y_shift)/2)*amplitude2
    # signal = ((signal.sawtooth(2 * np.pi * n * MeshX)+y_shift)/2)*amplitude2
    blaze2.putdata(signal.ravel().astype(int))
    
    for i in np.arange(width):
        for j in np.arange(height):
            imagePixel = img.getpixel((i,j))
            blazePixel = blaze.getpixel((i,j))
            blazePixel2 = blaze2.getpixel((i,j))
            # imgMap[i, j] = int(imagePixel*imageScale + blazePixel*blazeScale)
            # if 0.5*width <= i <= 0.75*width and 0.5*height <= j <= 0.75*height:
            #     imgMap[i, j] = int(imagePixel*imageScale + blazePixel2*blazeScale)
            # if np.sqrt((i-width/2)**2 + (j-height/2)**2) <= height/8:
            #     imgMap[i, j] = int(imagePixel*imageScale + blazePixel2*blazeScale)
            # imgMap[i, j] = int(imagePixel*imageScale + blazePixel2*blazeScale)
            # imgMap[i,j] = 190
            if SG != None:
                imgMap[i, j] = int((imagePixel/255)*(blazePixel2/amplitude2)*amplitude2)
                # imgMap[i, j] = int(imagePixel)
            elif circle != None:
                d = np.sqrt((i - width/2)**2 + (j - height/2)**2)
                if invert:
                    if d > (height/2)/circle:
                        imgMap[i,j] = int(blazePixel2)
                else:
                    if d < (height/2)/circle:
                        imgMap[i,j] = int(blazePixel2)
            else:
                imgMap[i, j] = int(imagePixel*imageScale + blazePixel2*blazeScale)
    
    # for i in np.arange(width/2):
    #     for j in np.arange(height):
    #         imgMap[i,j] = int(half)



            # Take a strip of pixels from the middle of the image and plot it
            # if i == width/2:
            #     strip = np.append(strip, imagePixel)
            #     newImg = np.append(newImg, imgMap[i,j])
            # if i == width/2:
                # strip = np.append(strip, imagePixel)
                # newImg = np.append(newImg, imgMap[i,j])
            # imgMap[i,j] = int(val)
    # draw = ImageDraw.Draw(img)
    # mf = ImageFont.truetype('/Users/anthonylu/Documents/LBNL/SLM/Roboto-Medium.ttf', 30)
    # linesmm = str("Lines per mm: " + str(n/12.5))
    # draw.text((30,30), linesmm, font=mf, fill = 255)
    # amp = str("Amplitude: " + str(amplitude))
    # draw.text((30,70), amp, font=mf, fill=255)
    display(img)    
    if strip == True:
        if angle == 0:
            newImg = []
            for i in np.arange(width):
                newImg = np.append(newImg, imgMap[i,height/2])
            plt.plot(np.arange(width), newImg)
        if angle == 90:
            newImg = []
            for i in np.arange(height):
                newImg = np.append(newImg, imgMap[width/2, i])
            plt.plot(np.arange(height), newImg)
        if saveStrip == True:
            if SG != None:
                if invert == True:
                    name = str(SG) + "_width_" + str(n) + "lpmm_" + str(amplitude2) + "amp_inv_plus" + str(yshift)
                    plt.title(name)
                    # plt.ylim((0,255))
                    filePath = "/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/results/blazed/partBlazed/circleCenter/200_width/images/"
                    plt.savefig(filePath + name + ".png")
                    plot = Image.open(filePath + name + ".png")
                    # display(plot)
                    plot = plot.resize((width,height))
                    ccd = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/results/blazed/partBlazed/circleCenter/200_width/5lpmm_" + str(SG) + "SG_" + str(amplitude2) + "amp_inv_plus" + str(yshift) + ".png")
                    # control = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/results/SGtest/smoothing/afternoon/control.png")
                    new_img = Image.new('RGB', (2*width, 2*height), (255, 255, 255))
                    new_img.paste(img,(0,0))
                    new_img.paste(plot,(0,height))
                    # new_img.paste(control,(width,0))
                    new_img.paste(ccd,(width,height))
                    # new_img.show()
                    new_img.save(filePath + name + "IMG.png")
                else:
                    name = str(SG) + "_width_" + str(n) + "lpmm_" + str(SG) + "SG_" + str(amplitude2) + "amp_plus" + str(yshift)
                    plt.title(name)
                    plt.savefig("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/results/SGtest/plots/" + name + ".png")
            elif circle != None:
                if invert:
                    name = str(n) + "lpmm_" + str(circle) + "radius_" + str(amplitude2) + "amp_inv"
                    plt.title(name)
                    plt.savefig("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/results/blazed/partblazed/circleCenter/plots/" + name + ".png")
                else:
                    name = str(n) + "lpmm_" + str(circle) + "radius_" + str(amplitude2) + "amp"
                    plt.title(name)
                    plt.savefig("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/results/blazed/partblazed/circleCenter/plots/" + name + ".png")
            else:
                img.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/results/blazed/plots/" + str(saveAs) + ".png")
        plt.ylim((0,260))
        plt.xlim((width/2-100, width/2+100))
        plt.show()
        
    # plt.plot(np.arange(width), (np.sin((k * np.arange(width)) + x_shift) + y_shift) * amplitude2)
    # plt.show()
    # plt.plot(np.arange(width), strip, label = "Original Image")
    # plt.plot(np.arange(height), newImg, label = "Cross Section")
    # plt.title("Cross Section Intensity of 4.8 lines/mm Hologram, Half Amplitude")
    # plt.xlabel("x (px)")
    # plt.ylabel("Intensity")
    # plt.savefig("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/partBlazed/circleOffCenter.png")
    # plt.legend()
    # plt.show()
    # display(img)
    
    if save:
        if SG != None:
            img.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/calibration/SGcircle/widths/"+str(SG) + "_width_" + str(n) + "lpmm_" + str(amplitude2) + "amp.png")
        elif circle != None:
            if invert:
                img.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/circles/5lpmm/" + str(n) + "lpmm_" + str(circle) + "radius_" + str(amplitude2) + "amp_inv.png")
            else:
                # img.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/circles/5lpmm/" + str(n) + "lpmm_" + str(circle) + "radius_" + str(amplitude2) + "amp.png")
                img.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/sharpCircle/5lpmm_2.5radius/" + str(amplitude2) + "amp.png")

        else:
            img.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/blazed/5lpmm/" + str(n) + "lpmm_" + str(amplitude2) + "amp.png")
    # img.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/calibration/" + str(n) + "lpmm_" + str(half) + "_half.png")
    # display(img)
    return img

# for i in np.arange(150, 250, 5):
#     makeBlazed(initialImage = "superGaussian200", n = 60, amplitude = i)
# makeBlazed(n = 5, angle = 90, SG = 200, amplitude = 200, save = True)
# for a in (30):
#     for b in (0):
# for c in np.arange(50, 350, 25):
#     for d in np.arange(50, 150, 20):
#         a = 20
#         b = 0
#         makeBlazed(n = a, angle = b, SG = c, amplitude = d, save = True)

# makeBlazed(initialImage = "testImages/gs/GSdog3", n = 100)

# makeBlazed(n=10, strip = True, flip = True, save = True)

# for i in np.arange(0, 260, 10):
#     makeBlazed(n = 39*2, half = i)

# for i in np.arange(0, 410, 10):
#     makeBlazed(n = i, amplitude = 190)

# for i in np.arange(50,255, 5):
#     makeBlazed(n = 200, amplitude = i)
# makeBlazed(n=400, amplitude=150)

# makeBlazed(n=5, angle = 0, circle = 3, invert=True, save=True)
# for i in np.arange(1, 11):
#     makeBlazed(n=5, circle = i, save = True)
    # makeBlazed(n=5, angle = 0, circle = i, invert=True, save=True)

# for i in np.arange(255, 495+40, 40):
#     # for j in (100, 150, 250):
# #         makeBlazed(n=5, SG = j, strip = True, amplitude = 190, save = True, yshift = i)
#     makeBlazed(n=5, SG = 200, strip = True, amplitude = 190, saveStrip = True, invert = True, yshift = i)
# makeBlazed(n=5, SG = 200, strip = True, amplitude = 190, saveStrip = True)
# makeBlazed(n=5, SG = 150, strip = True, amplitude = 190, saveStrip = True)
# makeBlazed(n=5, SG = 150, strip = True, amplitude = 230, saveStrip = True)
# makeBlazed(n=5, SG = 150, strip = True, amplitude = 70, saveStrip = True)
# makeBlazed(n=5, SG = 200, strip = True, amplitude = 190, saveStrip = True, invert = True, yshift = 255)

# for i in np.arange(250, 520, 20):
#     makeBlazed(n=10, strip = True, yshift = i, SG = 200, invert = True)
# makeBlazed(n=10, strip = True, yshift = 500, SG = 200, invert = True)

# for i in np.arange(10, 270, 20):
#     makeBlazed(n=5, strip=True, circle = 2.5, amplitude = i, save = True)
# makeBlazed(n=5, strip = True, SG = 500, amplitude = 210)

# for i in np.arange(100, 525, 25):
#     makeBlazed(n=5, strip = True, SG = i, amplitude = 210, save = True)

# for i in np.arange(0, 35, 5):
#     for j in np.arange(190, 220, 10):
#         makeBlazed(n = i, amplitude = j, save = True)

# makeBlazed(n=5, amplitude = 110, save = True)
# for i in np.arange(10, 270, 20):
#     makeBlazed(n=5, amplitude = i, save = True)

# Checkerboard pattern

def makeCheckerboard(circle = None):
    # img = Image.open("/Users/anthonylu/Documents/LBNL/SLM/black.png")
    width, height = img.size
    # width = 10
    # height = 10
    # img = Image.new(mode = "RGB", size = (width, height), color = (0,0,0))
    img = ImageOps.grayscale(img)
    imgMap = img.load()
    newImg = []
    
    for i in np.arange(width):
        for j in np.arange(height):
            if circle != None:
                d = np.sqrt((i - width/2)**2 + (j - height/2)**2)
                if d < height/circle:
                    if j % 2 == 0:
                        if i % 2 == 0:
                            imgMap[i,j] = 0
                        else:
                            imgMap[i,j] = 190
                    else:
                        if i % 2 == 0:
                            imgMap[i,j] = 190
                        else:
                            imgMap[i,j] = 0
                    if j == height/2:
                        newImg = np.append(newImg, imgMap[i,j])
            else:
                if j % 2 == 0:
                    if i % 2 == 0:
                        imgMap[i,j] = 0
                    else:
                        imgMap[i,j] = 190
                else:
                    if i % 2 == 0:
                        imgMap[i,j] = 190
                    else:
                        imgMap[i,j] = 0
                if j == height/2:
                    newImg = np.append(newImg, imgMap[i,j])
    
    # plt.plot(np.arange(width), newImg, label = "Cross Section")
    # plt.show()
    if circle != None:
        img.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/checkerboard/" + str(circle) + "_radius.png")
    display(img)

# makeCheckerboard(circle = 6)



# Test Gerchberg-Saxton algorithm

# """
# def GS_Python(image, maxIter):
#     global img
#     img = Image.open(image)
#     img = ImageOps.grayscale(img)
#     pixelMap = img.load()
#     width, height = img.size
#     initial = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/results/GStest/og.png")
#     initial = ImageOps.grayscale(initial)
    
#     # --- Assumptions
#     measuredAmplitudeSpace    = np.sqrt(img)
#     # measuredAmplitudeFourier  = np.ones((height, width))
#     measuredAmplitudeFourier  = np.sqrt(initial)
    
#     # --- Starting point
#     currentPhaseSpace         = np.random.rand(height, width)
    
#     # --- Initialization
#     currentPhaseFourier       = np.ones((height, width))

#     currentSpace = measuredAmplitudeSpace * np.exp(currentPhaseSpace * 1j)

#     for iter in range(maxIter):
#         # --- Enforce measured amplitude constraint in the Fourier domain
#         currentFourier            = np.fft.fft2(currentSpace)
#         currentPhaseFourier       = np.angle(currentFourier)
#         currentFourier            = measuredAmplitudeFourier * np.exp(1j * currentPhaseFourier)

#         # --- Enforce measured amplitude constraint in the spatial domain
#         currentSpace              = np.fft.ifft2(currentFourier)
#         currentPhaseSpace         = np.angle(currentSpace)
#         currentSpace              = measuredAmplitudeSpace * np.exp(1j * currentPhaseSpace) * 1.5

#     return currentPhaseFourier


# retrievedPhase = GS_Python("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/dogs/EXULUS_CGH_Sample_hd-modified.png", 
#                             50)



# img = Image.open("/Users/anthonylu/Documents/LBNL/SLM/black.png")
# # img = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/dogs/EXULUS_CGH_Sample_hd.png")
# img = ImageOps.grayscale(img)
# # print(np.sqrt(img))
# imgMap = img.load()
# width, height = img.size
# # print(width, height)

# strip = []
# for i in np.arange(width):
#     for j in np.arange(height):
#         imgMap[i,j] = int((retrievedPhase[j][i]+np.pi)*220/(2*np.pi))
#         if j == height/2:
#             strip = np.append(strip, imgMap[i,j])
# display(img)
# plt.plot(np.arange(width), strip)
# plt.show()
# img.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/gs/GSdog4.png")
# """

# plt.figure(1)

# # --- Reference image
# plt.subplot(131)
# plt.imshow(img)
# plt.title('Reference image')

# # --- Retrieved Fourier phase
# plt.subplot(132)
# plt.imshow(retrievedPhase)
# plt.title('Retrieved Fourier phase')

# plt.subplot(133)
# recoveredImage = np.fft.ifft2(np.exp(retrievedPhase * 1j))
# plt.imshow(np.absolute(recoveredImage)**2)
# plt.title('Recovered image')

# plt.show()



# # Make number images

# img = Image.open("/Users/anthonylu/Documents/LBNL/SLM/black.png")
# img = ImageOps.grayscale(img)
# # pixelMap = img.load()
# draw = ImageDraw.Draw(img)
# mf = ImageFont.truetype('/Users/anthonylu/Documents/LBNL/SLM/Roboto-Medium.ttf', 200)

# for i in np.arange(0, 1):
#     img = Image.open("/Users/anthonylu/Documents/LBNL/SLM/black.png")
#     img = ImageOps.grayscale(img)
#     # pixelMap = img.load()
#     draw = ImageDraw.Draw(img)
#     mf = ImageFont.truetype('/Users/anthonylu/Documents/LBNL/SLM/Roboto-Medium.ttf', 30)
#     text = str("Lines per mm: " + str(i/12.5))
#     draw.text((30,70), text, font=mf, fill = 255)
#     img.show()
#     # img.save("/Users/anthonylu/Documents/LBNL/SLM/nums/" + str(i) + ".png")

# draw.text((60,50), "10", font=mf, fill = 300)
# img.show()
# Im.save("/Users/anthonylu/Documents/LBNL/SLM/num.png")






# Make image with sharp edge text




def makeText(lpmm, amp, message, fontSize, save = False):
    # img = Image.open("/Users/anthonylu/Documents/LBNL/SLM/white.png")
    # img = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/text/5lpmm.png")
    img = makeBlazed(n = lpmm, amplitude = amp)
    W, H = img.size
    img = ImageOps.grayscale(img)
    imgMap = img.load()
    newImg = []
    
    draw = ImageDraw.Draw(img)
    mf = ImageFont.truetype('/Users/anthonylu/Documents/LBNL/SLM/Roboto-Medium.ttf', fontSize)

    # draw.text((width/2,height/2), "10", font=mf, fill = 300)
    # display(img)
    
    # message = "Hello World"
    
    _, _, w, h = draw.textbbox((0, 0), message, font=mf)
    draw.text(((W-w)/2, (H-h)/2), message, font=mf, fill="black")
    img = ImageOps.flip(img)
    img = ImageOps.mirror(img)
    display(img)
    if save:
        img.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/text/" + str(lpmm) + "lpmm_" + str(amp) + "amp_" + str(message) + "_" + str(fontSize) + "_5lpmm_black.png")


# makeText(10, 210, "BELLA", 300, save = True)



def makeLines(n = 5, amp = 255):
    img = Image.open("/Users/anthonylu/Documents/LBNL/SLM/black.png")
    img = ImageOps.grayscale(img)
    imgMap = img.load()
    width, height = img.size
    
    count = 0
    
    # for i in np.arange(width):
    for j in np.arange(height):
        for a in np.arange(n):
            if count % 2 == 0:
                imgMap[np.arange(width),j] = int(amp)
            else:
                imgMap[np.arange(width),j] = 0
        count += 1
# display(img)

# makeLines(n = 1000)



def makeRectangle():
    img = Image.open("/Users/anthonylu/Documents/LBNL/SLM/black.png")
    blazed = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/blazed/10lpmm_255amp.png")
    fblazed = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/blazed/10lpmm_255amp_flipped.png")
    width, height = img.size
    # width = 10
    # height = 10
    # img = Image.new(mode = "RGB", size = (width, height), color = (0,0,0))
    img = ImageOps.grayscale(img)
    imgMap = img.load()
    blazedMap = blazed.load()
    fblazedMap = fblazed.load()
    
    for i in np.arange(width):
        for j in np.arange(height):
            # STRIPES
            if i % 2 == 0:
                imgMap[i,j] = 190
            
            # LONG RECTANGLES
            # if -width/10 + width/2 <= i <= -5 + width/2:
            #     # imgMap[i,j] = fblazedMap[i,j]
            #     imgMap[i,j] = 255
            # if width/2 + 5 <= i <= width/2 + width/10:
            #     # if -height/8 + height/2 <= j <= height/8 + height/2:
            #     # imgMap[i,j] = blazedMap[i,j]
            #     imgMap[i,j] = 255
            
            # TWO RECTANGLES
            # if -width/15 + width/2 <= i <= -10 + width/2 or width/2 + 10 <= i <= width/2 + width/15:
            #     if -height/8 + height/2 <= j <= height/8 + height/2:
            #         # imgMap[i,j] = 255
            #         imgMap[i,j] = blazedMap[i,j]
            
            # CROSSHAIRS
            # if width/3-2 <= i <= width/3+2 or height/3-2 <= j <= height/3+2 or 2*width/3-2 <= i <= 2*width/3+2 or 2*height/3-2 <= j <= 2*height/3+2:
            #     imgMap[i,j] = 255
    
    display(img)
    img.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/feedbackAlgorithm/190_rectangle_vertical_lines_1px.png")


makeRectangle()


















