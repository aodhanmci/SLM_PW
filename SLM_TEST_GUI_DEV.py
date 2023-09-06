##############################
# code to look at the effect of an SLM on the amplitude and phase of a beam
# originally written by Jeroen, converted by Aodhan
##############################

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from scipy import signal
from PIL import Image, ImageOps, ImageFont, ImageDraw, ImageFilter
from numpy import asarray
import cv2
from scipy.ndimage import gaussian_filter
import time
from os import listdir
from os.path import isfile, join
# from IPython.display import display

def calibration(input, xZoom = 1, yZoom = 1, xShift = 0, yShift = 0 ,angle = 1.2):
    # lenspaper = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/lensPaper/crosshair4Img3.png")
    # lenspaper = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/feedbackAlgorithm/test51/crosshairImg.png")
    # lenspaper = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/feedbackAlgorithm/testResult.png")
    # display(lenspaper)
    lenspaper = Image.fromarray(input)
    lenspaper = ImageOps.flip(ImageOps.mirror(lenspaper))
    # display(lenspaper)
    
    crosshair4 = Image.open('/Users/loasis/Documents/GitHub/SLM_PW/crosshair4.png')
    width, height = crosshair4.size
    # display(crosshair4)
    # lenspaper = lenspaper.resize([int(width*2), int(height)])
    
    w, h = lenspaper.size
    x = width/2 - xShift
    y = height/2 + yShift
    lenspaper = lenspaper.crop((x - w / 2, y - h / 2,
                                x + w / (2 * xZoom), y + h / (2 * yZoom)))
    lenspaper = lenspaper.resize((width, height), Image.Resampling.LANCZOS)
    lenspaper = lenspaper.rotate(angle)

    return asarray(lenspaper)


    # def zoom_at(img, xZoom = xZoom, yZoom = yZoom, xShift = xShift, yShift = yShift):
    #     global w, h
    #     w, h = img.size
    #     # print(w,h)
    #     zoom2 = 2
    #     x = width/2 - xShift
    #     y = height/2 + yShift
    #     img = img.crop((x - w / zoom2, y - h / zoom2, 
    #                     x + w / (zoom2*xZoom), y + h / (zoom2*yZoom)))
    #     return img.resize((width, height), Image.Resampling.LANCZOS)
    
    # lenspaper = zoom_at(lenspaper, 151, 15)
    # lenspaper = lenspaper.rotate(1.2)
    
    # lenspaper.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/lensPaper/crosshair4ImgFlipped.png")
    
    # display(lenspaper)
    display(crosshair4)
    display(lenspaper)
    
    lenspaperArray = asarray(lenspaper)
    
    # # edges = cv2.Canny(lenspaper, 50, 150, apertureSize = 3)
    # edges = cv2.Canny(image = lenspaperArray, 
    #                    threshold1 = 120, 
    #                    threshold2 = 550
    #                   )
    
    # edgeImg = Image.fromarray(edges)
    # # display(edgeImg)
    
    # # lines = cv2.HoughLinesP(edges, 
    # #                         rho = 10000, 
    # #                         theta = np.pi/180, 
    # #                         threshold = 0, 
    # #                         # minLineLength = 100
    # #                         )
    
    # lines = cv2.HoughLinesP(edges,
    #                         rho = 0.05,
    #                         theta = np.pi/180,
    #                         threshold = 200,
    #                         # minLineLength = 100,
    #                         maxLineGap = 100)
    # print(len(lines))
    # print(lines)
    # for line in lines:
    #     # rho, theta = line[0]
    #     # print(line)
    #     a = np.cos(theta)
    #     b = np.sin(theta)
    #     x0 = a*rho
    #     y0 = b*rho
    #     x1 = int(x0 + 1000*(-b))
    #     y1 = int(y0 + 1000*(a))
    #     x2 = int(x0 - 1000*(-b))
    #     y2 = int(y0 - 1000*(a))
    #     cv2.line(lenspaper, (x1, y1), (x2, y2), (0, 0, 255), 2)
    
    # overlay = lenspaper.copy()
    # overlay = overlay.convert("RGB")
    
    # draw = ImageDraw.Draw(overlay)
    # # draw.line((0,0,1000,1000), fill = (255, 0, 0))
    # # draw.rectangle((10, 0, 1010, 1000), fill = (255, 0, 0))
    # for line in lines:
    #     draw.line((line[0][0], line[0][1]+10, line[0][2], line[0][3]+10), fill = (255, 0, 0))
    # draw.line((0, overlay.size[1], overlay.size[0], 0), fill = 255)
    
    # display(overlay)
    
    
    
    # cv2.imshow('image', lenspaper)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()





width = 1920
height = 1080

def zoom_at(img, x, y, zoom):
    global w, h
    w, h = img.size
    # print(w,h)
    zoom2 = zoom * 2
    img = img.crop((x - w / zoom2, y - h / zoom2, 
                    x + w / (zoom2*0.86), y + h / (zoom2*1.1)))
    return img.resize((width, height), Image.Resampling.LANCZOS)










def displayt(image, text):
    # print(image)
    image2 = image.copy()
    draw = ImageDraw.Draw(image2)
    # mf = ImageFont.truetype('/Users/anthonylu/Documents/LBNL/SLM/Roboto-Medium.ttf', 30)
    mf = ImageFont.truetype('/Users/loasis/Documents/GitHub/SLM_PW/Roboto-Medium.ttf', 30)
    # text = str(text)
    draw.text((30,30), text, font=mf, fill = 255*255*255)
    display(image2)


















#####

# Feedback algorithm takes initial beam image, calculates pixels above threshold, applies phase grating to those pixels.

# Initial: PNG filepath of initial beam image ("input") stored in SLM folder of GDrive. Should not include ".png". 
# Example: initial = "feedbackAlgorithm/test51/initial"

# testno: Test number, with all images stored in separate numbered folder. Just used for testing. Will not be part of final implementation

# count: Also just an index used for testing. Lazy way to simulate feedback loop. Will improve before implementation.

# threshold: Pixel intensity value (0-255) to flatten beam to. All pixels above this threshold create the "hotspot area"

# blur: The radius of Gaussian blurring to apply to the outer edges of the hotspot area. Required to prevent sudden phase shift (grating-to-zero) edges, which cause unwanted discontinuities in the output beam. Testing has shown blur = 5 to be optimal.

# innerBlur: The radius of Gaussian blurring to apply to the inner hotspot area. Without this value, grating would gain problematic and unwanted noise. Testing has shown innerBlur = 15 to be optimal, but can vary between ~5-25.

# range: Theoretically used to calculate the max absolute difference between input image and goal image to check how close the input beam is to being "flat". However, not currently being used.

# maxIter: Number of max iterations of the function to try and flatten the beam before exiting. Currently not being used.

# yshift: Adding constant vertical shift to the applied grating. For testing purposes

# plot: When set to True, will plot whichever lineouts are uncommented. To visualize certain steps in the process for testing and debugging.

#####




def feedback(testno = 0, count = 0, initial = None, initialArray = None, threshold = None, centerShift = 50, blur = 5, innerBlur = 15, range = 5, maxIter = 100, yshift = 4, plot = False):
    global aboveMultArray, belowMultArray, totalMultArray, totalMultImg, xi, yi, goalImg, goalArray, stacked, stacked2, x, y
    
    #####
    # Open the initial beam image from the "SLM" folder in GDrive. Function input should be a PNG filepath with no extension
    # For implementation: input is in the form of a numpy 2D array (initialArray)
    #####
    
    if initial != None:
        initialImg = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/" + str(initial) + ".png")
    
    if np.any(initialArray != None):
        initialImg = Image.fromarray(initialArray)
        print(initialImg.mode)
    
    blazed = Image.open('/Users/loasis/Documents/GitHub/SLM_PW/190_rectangle_vertical_lines_1px.png')
    blazedData = asarray(blazed)

    # initialImg.show()

    # display(initialImg)
    
    #####
    # A smaller version of the calibration function. Not the final implementation. Aligns CCD image to SLM screen, rescales, resizes
    #####
    
    # width, height = initialImg.size
    
    initialImg = ImageOps.flip(ImageOps.mirror(initialImg))     # With current setup, beam gets rotated 180° between the SLM and the CCD. Must align CCD image to match SLM screen before calculating grating
    
    initialImg = zoom_at(initialImg, width/2 - 275, height/2 + 13, 1)     # Not final implementation of zoom function
    initialImg = initialImg.rotate(1.2)     # Image is rotated 2°
    # initialImg = initialImg.convert("L")
    initialImgArray = asarray(initialImg)
    # initialImgArray = cv2.normalize(initialImgArray, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8U)
    # print(type(initialImgArray[0][0]))
    initialImg = Image.fromarray(initialImgArray)
    # display(initialImgTest)
    initialMap = initialImg.load()
    
    # print(initialImg.mode)     # mode: I (32 signed)
    # displayt(initialImg, "initialImg")
    # print(np.amax(initialImg))
    
    # INT32 MAX: 2**31 = 2,147,483,648
    int32max = 2**31
    
    initialArray = asarray(initialImg)     # Turn initial image into 2D array of pixel intensity values
    # print(type(initialArray[0][0]))     # np.int32
    
    
    #####
    # Initial testing to use peak-to-valley to find "threshold image" instead of manually inputting a threshold
    #####
    
    
    
    
    
    
    #####
    # Creating "goal" or "target" image (turn every pixel above the threshold to the threshold). What the final beam should look like.
    # For every additional trial (count != 0), any pixels above the threshold which were not previously above the threshold ("unique") are added to the goal image and included in the current grating calculation
    #####
    
    if count == 0:
        if threshold == None:
            initialMax = np.average(sorted(initialArray.flatten(), reverse=True)[:50])
            print(initialMax)
            threshold = 0.75*initialMax
        xi, yi = (initialArray >= int(threshold-5)).nonzero()
        # xi, yi = (np.any((initialArray >= int(threshold-5))|(initialArray )))
        stacked = np.stack((xi, yi), axis=-1)     # Must stack array in order to properly append new pixel coordinates to the array
        # print(xi, yi)
        # print(len(stacked))
    else:
        x, y = (initialArray >= int(threshold-10)).nonzero()
        stacked2 = np.stack((x, y), axis = -1)
        # print(x, y)
        # print(len(stacked2))
        unique = np.unique(np.concatenate((stacked, stacked2)),axis=0)
        # unique = (stacked2 != stacked).nonzero()
        # print(len(stacked), len(stacked2), len(unique))
        unstacked = np.stack(unique, axis=1)
        xi, yi = unstacked[0], unstacked[1]
        
    goalArray = initialArray.copy()
    goalArray[xi,yi] = int(threshold)
    goalImg = Image.fromarray(goalArray)
    goalMap = goalImg.load()
    
    
    # yshiftArray = gaussian_filter(yshiftArray, sigma = 15)
    goalArrayBlurred = gaussian_filter(goalArray, sigma = 10)
    goalImgBlurred = Image.fromarray(goalArrayBlurred)
    # displayt(goalImg, "GoalImg")
    # displayt(goalImgBlurred, "GoalBlurred")
    
    
    # goalArray = gaussian_filter(goalArray, sigma = 10)
    
    # xi = np.append(xi, (initialArray >= int(threshold)).nonzero()[0])
    # yi = np.append(yi, (initialArray >= int(threshold)).nonzero()[1])
    # print(len(xi))
    # goalArray = initialArray.copy()     # Create copy of initial image to turn into goal image
    # goalArray[xi,yi] = int(threshold)     # Create goal image by setting pixels above threshold equal to the threshold (flattening)
    # # goalArray[x,y] = int(threshold)
    # goalImg = Image.fromarray(goalArray)     # Turn goal array into image
    
    # displayt(goalImg, "goalImg")
    
    
    #####
    # Begin feedback loop, checking until every pixel value is within "range" away from the goal image
    # THIS PART CURRENTLY DOES NOT WORK. FEEDBACK LOOP IS IMPLEMENTED OUTSIDE THE FUNCTION. MAY CHANGE LATER.
    #####
    
    
    # trial = 0
    
    # diff = abs(255 - threshold)
    # while diff > range:
            
    #     try:
        
        
        
    #####
    # Take difference between initial image and goal image to find which pixels are brighter and which are dimmer compared to threshold
    #####
    
    
    image1 = np.int32(initialImg)     # Open initial image
    image2 = np.int32(goalImg)     # Open goal image
    # image3 = image1 - image2
    diffImgArray = cv2.subtract(image1, image2)     # Take difference between two images. Initial - goal. Positive numbers = too bright, negative = too dim. np.int32 to account for negative numbers -255 to +255
    # print(type(diffImgArray[0][0]))
    # diffImgArray = np.int32(diffImgArray)     
    # print("\ndiffImg\nMax: " + str(np.amax(diffImgArray)), "\nMin: " + str(np.amin(diffImgArray)))
    diffImg = Image.fromarray(diffImgArray)
    # displayt(diffImg, "diffImg")
    
    # aboveImgMax = aboveImg.copy()
    aboveImgArray = diffImgArray.copy()
    belowImgArray = diffImgArray.copy()
    xa, ya = (aboveImgArray > 0).nonzero()     # Find coordinates of pixels which are above and below the threshold
    xb, yb, = (belowImgArray < 0).nonzero()
    aboveImgArray[xb, yb] = 0     # Using the diffImg array, take all pixels that are NOT above the threshold and set to zero. Remaining pixels are above the threshold, creating aboveImg
    belowImgArray[xa, ya] = 0     # Opposite for belowImg
    belowImgArray = np.abs(belowImgArray)     # Turn belowImg positive, to subtract from grating later
    # print("\nAbove\nMax: " + str(np.amax(aboveImgArray)) + "\nMin: " + str(np.amin(aboveImgArray)))
    # print("\nBelow\nMax: " + str(np.amax(belowImgArray)) + "\nMin: " + str(np.amin(belowImgArray)))
    aboveImgArray = np.abs(np.int8(aboveImgArray))     # Turn into 0-255 brightness values
    belowImgArray = np.abs(np.int8(belowImgArray))
    
    aboveImg = Image.fromarray(aboveImgArray, "L")
    belowImg = Image.fromarray(belowImgArray, "L")
    # displayt(aboveImg, "aboveImg")
    # displayt(belowImg, "belowImg")
    
    #####
    # Take all pixels above and below threshold and blur the image using innerBlur value. This emits a certain amount of noise inherent to the input beam, so that these high frequency oscillations do not cause issues when calculating and appling the grating. Essentially just want to find the "outline" of the aboveImg and belowImg to be used to multiply by the grating.
    #####
    
    aboveImgGray = ImageOps.grayscale(aboveImg.copy())
    aboveImgBlurred = aboveImgGray.filter(ImageFilter.GaussianBlur(radius = innerBlur))
    aboveBlurredArray = asarray(aboveImgBlurred, dtype=np.int32)
    # displayt(aboveImgBlurred, "aboveImgBlurred")
    
    belowImgGray = ImageOps.grayscale(belowImg.copy())
    belowImgBlurred = belowImgGray.filter(ImageFilter.GaussianBlur(radius = innerBlur))
    belowBlurredArray = asarray(belowImgBlurred, dtype=np.int32)
    # displayt(belowImgBlurred, "belowImgBlurred")
    
    #####
    # Take all pixels above and below threshold and set to 255 (max). This is just to find the "edges" of aboveImg (the boundary between 255 and 0), which will receive a Gaussian blur. This causes the final grating image to have soft, gaussian sloping edges instead of sharp cutoff edges, which cause visible phase issues in the resulting beam image.
    #####
    
    aboveImgMaxArray = aboveImgArray.copy()
    belowImgMaxArray = belowImgArray.copy()
    # aboveImgMaxArray = np.int32(aboveImgMaxArray)
    aboveImgMaxArray = np.uint8(aboveImgMaxArray)
    belowImgMaxArray = np.uint8(belowImgMaxArray)
    
    aboveImgMaxArray[xa, ya] = 255
    belowImgMaxArray[xb, yb] = 255
    
    aboveImgMax = Image.fromarray(aboveImgMaxArray, "L") 
    belowImgMax = Image.fromarray(belowImgMaxArray, "L")
    # displayt(aboveImgMax)
    # print("\nAboveMax\nMax: " + str(np.amax(aboveImgMaxArray)))
    # print("\nBelowMax\nMax: " + str(np.amax(belowImgMaxArray)))
    
    aboveImgMaxGray = ImageOps.grayscale(aboveImgMax.copy())
    belowImgMaxGray = ImageOps.grayscale(belowImgMax.copy())
    # display(aboveImgMaxGray)
    # aboveImgMaxMap = aboveImgMax.load()
    
    # displayt(aboveImgMax, "aboveImgMax")
    
    aboveMaxBlurred = aboveImgMaxGray.filter(ImageFilter.GaussianBlur(radius = blur))
    aboveMaxBlurredMap = aboveMaxBlurred.load()
    aboveMaxBlurredArray = asarray(aboveMaxBlurred, dtype=np.int32) # int32
    # displayt(aboveMaxBlurred, "aboveMaxBlurred")
    
    belowMaxBlurred = belowImgMaxGray.filter(ImageFilter.GaussianBlur(radius = blur))
    belowMaxBlurredMap = belowMaxBlurred.load()
    belowMaxBlurredArray = asarray(belowMaxBlurred, dtype=np.int32) # int32
    # displayt(belowMaxBlurred, "belowMaxBlurred")
    
    
    # print("\nAboveMaxBlurredArray\nMax: " + str(np.amax(aboveMaxBlurredArray)))
    # print("\nBelowBlurredArray\nMax: " + str(np.amax(belowBlurredArray)))
    
    #####
    # Initialize final grating array (multArray)
    #####
    
    if count == 0:
        aboveMultArray = np.zeros((1080,1920))
        belowMultArray = np.zeros((1080,1920))
        totalMultArray = np.zeros((1080,1920))

    
    aboveMultArray2 = aboveMultArray     # Save previous multArray as multArray2 to take average later
    aboveMultArray2Blurred = asarray(Image.fromarray(aboveMultArray2, "L").filter(ImageFilter.GaussianBlur(radius = blur)), dtype = np.int32)
    
    aboveMultArray = np.multiply(aboveMaxBlurredArray, blazedData)     # Final grating should take into account the "edges" or "boundaries" of the threshold area, and should have blurred edges. This multiplies the blurred edges by the previously created grating image.
    aboveMultArray = np.multiply(aboveMultArray, aboveBlurredArray)     # Final grating should also take into account the general shape of the threshold area. So pixels 50 above the threshold should receive less intense grating, while pixels 150 above the threshold should receive more intense grating. This takes the shape (values) into account
    
    # aboveMultArray = np.multiply(aboveBlurredArray, blazedData)     # This one does not have to be used. Added for testing
    
    ################## PREVIOUS TESTING. SAVED AND COMMENTED OUT FOR REFERENCE
    # belowMultArray2 = belowMultArray     # Save previous multArray as multArray2 to take average later     ##### BELOWMULTARRAY DOES NOT INITIALLY EXIST AND NEITHER DOES ABOVEMULTARRAY: FIX WHEN RECURSION    # UPDATE: FIXED (I BELIEVE)
    # belowMultArray2Blurred = asarray(Image.fromarray(belowMultArray2, "L").filter(ImageFilter.GaussianBlur(radius = blur)), dtype = np.int32)
    
    # belowMultArray = np.multiply(belowMaxBlurredArray, blazedData)
    # belowMultArray = np.multiply(belowMultArray, belowBlurredArray)
    ##################
    
    # BelowMult Test
    belowMultArray2 = belowMultArray
    belowMultArray = np.multiply(belowMaxBlurredArray, blazedData)
    # belowMultArray = np.multiply(belowMultArray, belowBlurredArray)
    belowMultArray = np.multiply(belowBlurredArray, blazedData)
    
    #####
    # Since multiple arrays were multiplied together, now must normalize the final grating array to the intended amplitude
    #####
    
    # print(np.amax(aboveMultArray))
    # aboveMultArray = (aboveMultArray/np.amax(aboveMultArray)*np.amax(aboveImgArray)*aboveImgArray).astype(np.int32)
    
    # print(np.amax(aboveMultArray))
    
    aboveMultArray = (aboveMultArray * np.amax(aboveBlurredArray) / (np.amax(aboveMultArray))).astype(np.int32) # Normalize multiplied grating to the max of the subtracted image
    belowMultArray = (belowMultArray * np.amax(belowBlurredArray) / (np.amax(belowMultArray))).astype(np.int32)
    # aboveMultArray = (aboveMultArray * 200 / (np.amax(aboveMultArray))).astype(np.uint8)
    # print(np.amax(aboveMultArray2))
    
    # totalMultArray = (aboveMultArray - belowMultArray).astype(np.int32)
    # totalMultArray = aboveMultArray.astype(np.int32)
    # totalMultArray2 = totalMultArray.copy()
    totalMultArray2 = totalMultArray.astype(np.int32)     # Copy final grating array (totalMultArray) to take average later
    # print(np.amax(totalMultArray2))
    # if np.amax(totalMultArray) != 0:     # FOR SECOND TRIAL AND BEYOND
    #     # aboveMultArray = (aboveMultArray + 0.7*(aboveMultArray2 + aboveMultArray) / 2).astype(np.uint8)
    #     # aboveMultArray = (aboveMultArray + (aboveMultArray2 + aboveMultArray) / 2).astype(np.uint8)
    #     # aboveMultArray = (aboveMultArray + (aboveMultArray + aboveMultArray) / 2).astype(np.uint8)     # THIS IS FOR THE TEST 2 FOLDER
    #     # aboveMultArray = (aboveMultArray2 + aboveMultArray).astype(np.uint8)     # THIS IS FOR THE TEST 3 FOLDER
    #     # aveMax = 1.1 * (np.amax(aboveMultArray2) + ((np.amax(aboveMultArray2) + np.amax(aboveMultArray))/2))
    #     # print("aveMax: " + str(aveMax))
    #     # aboveMultArray = (aboveMultArray * aveMax / np.amax(aboveMultArray)).astype(np.uint8)     # THIS IS FOR THE TEST 4 FOLDER
    #     # TEST 5 = TEST 4 BUT IN EXTENDED MODE
    #     # aboveMultArray = (aboveMultArray2 + ((aboveMultArray + aboveMultArray) / 2)).astype(np.int32)     # TEST 6, EXTENDED MODE AGAIN
    #     # belowMultArray = (belowMultArray2 + ((belowMultArray + belowMultArray) / 2)).astype(np.int32)
        
    #     # totalMultArray2 = totalMultArray.astype(np.int32)
    #     totalMultArray = (totalMultArray2 + aboveMultArray - belowMultArray).astype(np.int32)
    # else:
    #     totalMultArray = (aboveMultArray - belowMultArray).astype(np.int32)
    
    #####
    # Find difference between threshold and max of result image and turn into multiplication of above and below. Used to add and subtract by smaller increments as image gets closer to goal
    # THIS IS A MORE CONSERVATIVE APPLICATION OF THE FEEDBACK. HOWEVER, ADJUSTMENTS GET SLOWER AND SLOWER CLOSER TO THE GOAL. TESTING HAS SHOWN THIS IS NOT ENTIRELY NECESSARY, SO NOT CURRENTLY BEING USED. APPLY DIFFMULT AGAIN IF NEW TESTING SHOWS THAT MORE FEEDBACK TRIALS LEADS TO INSANE NOISE AND POSITIVE FEEDBACK LOOP ISSUES
    #####
    
    # diffMult = np.abs((np.amax(goalArray) - np.amax(initialArray)).astype(np.uint8))
    # print("MAXES: " + str(np.amax(goalArray)) + str(np.amax(initialArray)))
    # print("DIFFMULT: " + str(diffMult))
    # display(initialImg)
    
    # print(np.amax(initialArray), np.amax(goalArray), np.amax(initialArray) - np.amax(goalArray))
    coords = np.stack((xi, yi), axis=1)
    initialVals = initialArray[[xi],[yi]]
    # print(initialVals[0])
    initialAvg = np.mean(initialVals[0])
    # print(initialAvg)
    diff = np.abs(initialAvg - threshold)
    diffMult = diff/100*2
    # print("AVE: " + str(initialAvg))
    # print("Diff: " + str(diff/100))
    # print(np.amax(initialVals[0]))
    # print(len(initialArray[[xi],[yi]][0]))
    # print(coords.shape)
    # print("DIFF: " + str(diff))

    # print(np.mean(aboveImgArray))
    
    #####
    # "diff" is calculated as absolute difference between the average values of the input beam's threshold area and the threshold value. Average is used to exclude any single-pixel bright specks. This does not currently stop the algorithm, it is just to print a notice once the flattening is sufficient. However, could be used to end the algorithm entirely
    #####
    
    if diff <= 5.0:
        print("ERROR LESS THAN 5. FLATTENING COMPLETE.")
        # return
    
    #####
    
    # totalMultArray = (totalMultArray2 + diffMult * aboveMultArray - diffMult * belowMultArray).astype(np.int32)
    # totalMultArray = (totalMultArray2 + 0.5 * aboveMultArray - 0.5 * belowMultArray).astype(np.int32)     # Add and subtract 1/2 of the above and below arrays. More conservative application, but slower. Use if encounter positive feedback loop issues.
    totalMultArray = (totalMultArray2 + aboveMultArray - belowMultArray).astype(np.int32)     # Simply add the calculated array for pixels above threshold and subtract array for pixels below threshold. Should work in most cases.
    
    totalMultArray[totalMultArray < 0] = 0     # Sometimes, subtracting belowMultArray leads to negative grating values (overcorrection). This does not work with SLM, so change all negative numbers to zero

    yshiftArray = np.ones(shape = totalMultArray.shape)

    #####
    # WAVEFRONT CORRECTION TEST
    #####
    
    if count ==9:
        # """
        # wfCorrectionArray = wavefront()
        # totalMultArray = totalMultArray + wfCorrectionArray
        # if count == 0:
        # totalMultArray[xi,yi] = totalMultArray[xi,yi] + yshift
             # Initialize yshift array
        # print(yshiftArray[0][0])
        yshiftArray = yshiftArray * 15
        # print(yshiftArray[0][0])
        # yshiftArray = yshiftArray
        # print(yshiftArray[0][0])
        
        # yshiftArray[xi,yi] = totalMultArray[xi,yi]     # Shift grating arary proportional to the local value of the grating array. Creates yshift the same shape as the grating
        yshiftArray[xi,yi] = 15 - totalMultArray[xi,yi] * 0.1     # Shift entire grating upward, and antiproportional to shape of grating. With some tweaking, this creates a final grating which has a flat top (all values match at top) and the yshift mirrors that
        # yshiftArray[xi,yi] = 50     # Constant yshift ONLY IN THE THRESHOLD AREA. Gaussian blur below ensures smooth transition back to zero outside the threshold area.
        # yshiftArray[xi,yi] = 70 - (totalMultArray[xi,yi] **2) / 100     # Squaring totalMultArray accounts LESS for the shape of totalMultArray. Just testing other ways to make different yshift shapes.

        
        yshiftArray = gaussian_filter(yshiftArray, sigma = 15)     # Smooth transition from yshift to zero. Testing shows ideal sigma value of 15.
        totalMultArray = totalMultArray + yshiftArray     # Directly add yshift to previous grating
        # totalMultArray = totalMultArray     # This should be active and the above line should be commented out to NOT include y shifts
        
        # """ 
        
    
    ######
    
    
    
    
    
    
    
    # if np.amax(totalMultArray) >= 190:     # TEST 13
    #     totalMultArray = (totalMultArray * 190 / np.amax(totalMultArray)).astype(np.int32)
    
    # print(type(totalMultArray[0][0]))
    
    # print("MULTMIN: " + str(np.amin(totalMultArray)))
    # totalMultArray[totalMultArray < yshift] = yshift
    totalMultArray = totalMultArray.astype(np.uint8)
    # print("\nAboveMultArray\nMax: " + str(np.amax(aboveMultArray)), "\nMin: " + str(np.amin(aboveMultArray)))
    # print("\nBelowMultArray\nMax: " + str(np.amax(belowMultArray)), "\nMin: " + str(np.amin(belowMultArray)))
    
    
    # multArray = multArray * blazedData
    # multArray = np.multiply(lenspaperArray, blazedData)
    # multArray = lenspaperBlurredArray * blazedData
    # multArray = np.multiply(lenspaperBlurred)
    # print(type(aboveMultArray[0][0]))
    
    
    # multArray = (multArray/np.amax(multArray)*np.amax(lenspaperArray)*lenspaperArray).astype(np.int32)
    
    
    # multArray = (multArray/np.amax(multArray)*np.amax(lenspaperArray)).astype(np.int32)
    # multArray = multArray.astype(np.int32)
    # aboveMultArray = aboveMultArray.astype(np.int32)
    # multArray = np.divide(multArray, 1)
    # print(type(multArray[0][0]))
    # print(np.amax(lenspaperArray))
    # print(np.amax(multArray))
    # print(type(aboveMultArray[0][0]))
    # print(aboveMultArray.shape)
    aboveMultImg = Image.fromarray(aboveMultArray, "L") # mode = L
    aboveMultMap = aboveMultImg.load()
    # display(multImg)
    
    totalMultImg = Image.fromarray(totalMultArray, "L") # mode = L
    # displayt(totalMultImg, "totalMult")
    # totalMultArray2 = totalMultArray.copy()
    # totalMultImg2 = Image.fromarray(totalMultArray2)
    # totalMultMap2 = totalMultImg2.load()
    
    if count == 0:
        for i in np.arange(width):
            initialImg.putpixel((i, int(height/2-centerShift)), int(255))
        initialImg.show()
    
    
    
    
    
    
    # displayt(totalMultImg, "SLM Grating")
    # maxStrip = []
    # blurredStrip = []
    # multStrip = []
    # ogStrip = []
    # for i in np.arange(width):
    #     # maxStrip = np.append(maxStrip, lenspaperMaxMap[i,height/2])
    #     ogStrip = np.append(ogStrip, lenspaperMap[i,height/2])
    #     blurredStrip = np.append(blurredStrip, lenspaperBlurredMap[i,height/2])
    #     multStrip = np.append(multStrip, multMap[i,height/2])
    # # plt.plot(np.arange(width), maxStrip, label = "Max")
    
    # # plt.plot(np.arange(width), blurredStrip, label = "Blurred")
    # # plt.plot(np.arange(width), multStrip, label = "Mult")
    # # plt.plot(np.arange(width), ogStrip, label = "Original")
    # # plt.legend()
    # # plt.xlim(700,1200)
    # # plt.show()
    
    # aboveMultImg.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/feedbackAlgorithm/081523/test6/4.png")
    # totalMultImg.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/feedbackAlgorithm/test" + str(testno) + "/" + str(count+1) + "TEST_15AMP_SIMGA20.png")
    # displayt(aboveImg, 'aboveImg')
    # displayt(aboveMultImg, 'aboveMultImg')

        
    
    #####
    # Make lineout plots of images to easily visualize values and shapes. Used for diagnostics and testing of algorithm
    #####
    
    if plot:
        aboveStrip = []
        belowStrip = []
        aboveMaxStrip = []
        belowMaxStrip = []
        aboveMaxBlurredStrip = []
        belowMaxBlurredStrip = []
        aboveMultStrip = []
        belowMultStrip = []
        diffImgStrip = []
        initialStrip = []
        goalStrip = []
        aboveBlurredStrip = []
        belowBlurredStrip = []
        aveTestStrip = []
        totalMultStrip = []
        yshiftStrip = []
        goalBlurredStrip = []
        

        
        for i in np.arange(width):
            aboveStrip = np.append(aboveStrip, aboveImgArray[int(height/2-centerShift), i])
            belowStrip = np.append(belowStrip, belowImgArray[int(height/2-centerShift), i])
            aboveMaxStrip = np.append(aboveMaxStrip, aboveImgMaxArray[int(height/2-centerShift), i])
            belowMaxStrip = np.append(belowMaxStrip, belowImgMaxArray[int(height/2-centerShift), i])
            aboveMaxBlurredStrip = np.append(aboveMaxBlurredStrip, aboveMaxBlurredArray[int(height/2-centerShift), i])
            belowMaxBlurredStrip = np.append(belowMaxBlurredStrip, belowMaxBlurredArray[int(height/2-centerShift), i])
            aboveMultStrip = np.append(aboveMultStrip, aboveMultArray[int(height/2-centerShift), i])
            diffImgStrip = np.append(diffImgStrip, diffImgArray[int(height/2-centerShift), i])
            initialStrip = np.append(initialStrip, initialArray[int(height/2-centerShift), i])
            goalStrip = np.append(goalStrip, goalArray[int(height/2-centerShift), i])
            aboveBlurredStrip = np.append(aboveBlurredStrip, aboveBlurredArray[int(height/2-centerShift), i])
            belowMultStrip = np.append(belowMultStrip, belowMultArray[int(height/2-centerShift), i])
            belowBlurredStrip = np.append(belowBlurredStrip, belowBlurredArray[int(height/2-centerShift), i])
            totalMultStrip = np.append(totalMultStrip, totalMultArray[int(height/2-centerShift), i])
            yshiftStrip = np.append(yshiftStrip, yshiftArray[int(height/2-centerShift), i])
            goalBlurredStrip = np.append(goalBlurredStrip, goalArrayBlurred[int(height/2-centerShift), i])
            # aveTestStrip = np.append(aveTestStrip, array3[int(height/2+30), i])
        # """
        plt.plot(np.arange(width), totalMultStrip, label = "SLM Grating", color = "C2")
        plt.plot(np.arange(width), initialStrip, label = "Initial")
        plt.plot(np.arange(width), goalStrip, label = "Goal")
        # plt.plot(np.arange(width), aboveStrip, label = "Above")
        # plt.plot(np.arange(width), aveTestStrip, label = "Average")
        # plt.plot(np.arange(width), belowStrip, label = "Below")
        # plt.plot(np.arange(width), aboveMaxStrip, label = "AboveMax")
        # plt.plot(np.arange(width), belowMaxStrip, label = "BelowMax")
        # plt.plot(np.arange(width), aboveMaxBlurredStrip, label = "AboveMaxBlurred")
        # plt.plot(np.arange(width), belowMaxBlurredStrip, label = "BelowMaxBlurred")
        # plt.plot(np.arange(width), belowBlurredStrip, label = "BelowBlurred")
        # plt.plot(np.arange(width), aboveMultStrip, label = "AboveMult")
        # plt.plot(np.arange(width), belowMultStrip, label = "BelowMult")
        # plt.plot(np.arange(width), totalMultStrip, label = "TotalMult", color = "yellow")
        # plt.plot(np.arange(width), diffImgStrip, label = "DiffImg", color = "yellow")
        # plt.plot(np.arange(width), aboveBlurredStrip, label = "AboveBlurred")
        # plt.plot(np.arange(width), yshiftStrip, label = "YShift", color = "red")
        # plt.plot(np.arange(width), goalBlurredStrip, label = "GoalBlurred")

        
        plt.legend()
        plt.xlim(550,1325)
        plt.ylim(0,260)
        plt.title("Test " + str(testno) + ", Trial " + str(count) + ", AveDiff = " + str(np.round(diff,2)) + ", 15AMP_SIGMA20")
        # plt.savefig("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/feedbackAlgorithm/test" + str(testno) + "/plot" + str(count) + "TEST_15AMP_SIGMA20.png")
        plt.show()
        # """
        
        
        # displayt(totalMultMap2, "TotalMult2")
        

    


    # print("OOPS")

    return totalMultImg, totalMultArray, diff, threshold
    
    #################


def runFeedback(testno = None, initArray = None, maxIter = 5):
    # while i <= 11:
    for i in np.arange(maxIter):

        try:
            gratingImg, gratingArray, diff = feedback(
                initialArray = initArray,
                count = i
            )

            initArray = gratingArray
            resultArray = gratingArray

            trialCompleted = True

            print("Completed round " + str(i))

        except:
            pass

        # if i == 0:
        #     feedback(
        #         # initial = "feedbackAlgorithm/test" + str(testno) + "/initial", 
        #         # testno = testno, 
        #         initialArray = initArray,
        #         count = i,
        #         plot = True
        #         )
        # else:
        #     try:
        #         # file = None
        #         # while file == None:
                    
        #         feedback(initial = "feedbackAlgorithm/test" + str(testno) + "/" + str(i) + "Result", testno = testno, count = i,
        #                     plot = True
        #                  )
        #     except:
        #         # count = i - 1
        #         # time.sleep(5)
        #         # continue
        #         pass

# runFeedback(51)


#####

# When you run this version of the feedback algorithm, you should:

# 1. Calibrate the image (matches CCD image to SLM image)
#   1.1 Display "crosshair4" on SLM
#   1.2 Save image (usually as "crosshairImg")
#   1.3 Run calibration function until properly aligned
#   1.4 Transfer numbers to zoom_at and feedback functions

# 2. Save initial beam input image as "initial.png"
#   2.1 This would also be a good time to save wavefront data if applicable

# 3. Once image shows up in GDrive, run "runFeedback" with trial number as input
#   3.1 If you plan to put the result onto the SLM, instead of running the function for testing, make sure to uncomment the two lines that save the output image and output lineout graph. Otherwise, leave commented out to prevent unwanted images from being saved in folder

# 4. Once output image shows up on GDrive, display on SLM.
#   4.1 Naming convention: Algorithm will save the first output image as "1.png". Save the resulting beam image as "1Result.png" so algorithm will recognize it
#   4.2 Also another good time to save wavefront data if applicable

# 5. Repeat to your heart's desire!

# 6. MAKE SURE to note down the trial number and what you changed / any notes for that trial below. Will be helpful to look back later

#####




# calibration()












#####
# TRIAL NUMBERS AND NOTES
#####


# Test 11 is with polarizer in (because I'm dumb) and image more centered
# Observation from test 11: "Above" and "below" add to previous results, which creates a compounding error issue. Resulting images flip between bright and dark spots every trial

# Test 12: Get rid of compounding for above and below, and only keep compounding for total mult
# Observation: Still flipping. 

# Test 13: Normalizing grating to 190 if max is above 190.

# Test 14: Keep 190 normalization, multiply above and below by 1/2 before adding to previous grating

# Test 15: Using diffMult instead of 1/2

# Test 16: Multiplied sensitivity by 2 to go faster
# Observation: This test dipped below the threshold and came back up. Very slow to iterate close to 150.

# Test 17: Blur radius of 10

# Test 18: Blur radius back to 5. 20lpmm instead of 10lpmm

# Test 19: Blur radius 15, 20lpmm

# Test 20: Blur radius 3, 20lpmm. Multipliers back to 1/2 instead of using diffMult

# Test 21: Blur radius 3, 190_rectangle_vertical_lines_1px grating. Multipliers 1/2

# Test 22: Blur radius 5

# Test 23: Blur radius 10

# Test 24: Outer blur 2000, inner blur 5

# Test 25: Outer blur 5, inner blur 5, 190 grating, mult 1/2, STANDARD MODE

# Test 26: Same, unsaturated initial image

# Test 27: Inner blur 0

# Test 28: Inner blur 1

# Test 29: Inner blur 3

# Test 30: Same. Threshold buffer 10 instead of 5

# Test 31: Threshold 50

# Test 32: Threshold 150. Y shift 100. BEAMSPLITTER IN

# Test 33: Threshold 150. Y shift 0.

# Test 34: Removed lens tissue. Playing around with y shift for wavefront correction.

# Test 35: Fixing gaussian beam. 

# Test 36: Apply full rectangular grating
# Observation: Full rectangular grating does not result in as much noise as regular tests. So quickly varying grating causes noise, not inherent to grating

# Test 37: Threshold 200

# Test 38: Inner blur 2

# Test 39: Threshold 175. Inner blur 15 (ok)

# Test 40: Inner blur 10 (ok)
 
# Test 41: Inner blur 5 (ok)

# Test 42: Inner blur 2 (terrible)

# Test 43: Inner blur 1 (terrible)

# Test 44: Inner blur 0 (terrible)

# Test 45: Inner blur 50 (ok, slow)

# Test 46: Inner blur 30 (ok, slow)

# Test 47: Inner blur 15. Multiply by 1 instead of 0.5 and 0.5 (very good. Use 15, mult 1)

# Test 48: Wavefront sensor data acquisition. Same settings as 47

# Test 49: Same as 48

# Test 50: Again

# Test 51: Just some test gratings to fix wavefront. Now using MasterControl to take data instead of native software. Created "SLM_TEST_MC.py" to take MC datatype, while "SLM_PW_TEST.py" takes regular CCD datatype. Will use MC going forward?

# Test 52: Take WF data with 1px grating across entire SLM, and with 15 yshift, and compare with beam correction both with and without clear SLM subtraction

















































































































#####
# CREATE NEW IMAGE TO ADD TO GRATING WHICH WILL ATTEMPT TO FIX WAVEFRONT
#####

def wavefront():
    wfCorrection = Image.new('P', size = totalMultImg.size)
    wfCorrection = ImageOps.grayscale(wfCorrection)
    wfCorrectionMap = wfCorrection.load()
    
    for i in np.arange(width):
        for j in np.arange(height):
            distance = np.sqrt((i-width/2)**2 + (j-height/2)**2)
            # hVal = -(( 200/(width**2) ) * ( distance**2 - distance*width ))
            hVal = (400/(width**2)) * (distance**2 - (width**2)/4)+50
            wfCorrectionMap[i,j] = int(hVal)
    
    
    wfCorrection.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/feedbackAlgorithm/parabola.png")
    
    wfCorrection = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/feedbackAlgorithm/parabola.png")
    
    # Parabola intercept form: y = a (x - int1) (x - int2)
    # (x,y) = vertex
    # x = width/2
    # y = -100
    # int1 = 0
    # int2 = width
    # a = 200/(width**2)
    
    # y = [ 200/(width**2) ] [ x**2 - x(width) ] + 100
    
    # wfCorrectionArray = Image.fromarray(wfCorrection)
    
    wfCorrectionArray = asarray(wfCorrection).astype(np.uint8)

    
    wfStrip = []
    # for i in np.arange(width):
    #     # wfCorrectionMap[i, int(height/2)] = int(255)
    #     wfStrip = np.append(wfStrip, wfCorrectionArray[int(height/2), i])
    
    # plt.plot(np.arange(width), wfStrip)
    # plt.show()
    
    # display(wfCorrection)
    
    return wfCorrectionArray

# wavefront()

