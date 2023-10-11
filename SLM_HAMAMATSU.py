import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from scipy import signal
from PIL import Image, ImageOps, ImageFont, ImageDraw, ImageFilter
from numpy import asarray
import cv2
from scipy.ndimage import gaussian_filter
from autoscaling import *
import pandas as pd
# from IPython.display import display

def calibration(SLM_data, CCD_data):
    warp_transform = clickCorners(SLM_data, CCD_data)
    return warp_transform


def center(imageArray):
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = np.uint8(imageArray)
    ret,thresh = cv2.threshold(gray_image,50,255,0)
    M = cv2.moments(thresh)

    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    newImage = Image.fromarray(imageArray)
    # display(newImage)
    
    return cX, cY


#####

# Feedback algorithm takes initial beam image, calculates pixels above threshold, applies phase grating to those pixels.

# Initial: PNG filepath of initial beam image ("input") stored in SLM folder of GDrive. Should not include ".png". 
# Example: initial = "feedbackAlgorithm/test51/initial"

# testno: Test number, with all images stored in separate numbered folder. Just used for testing. Will not be part of final implementation

# count: Index used for feedback loop.

# threshold: Pixel intensity value (0-255) to flatten beam to. All pixels above this threshold create the "hotspot area"

# blur: The radius of Gaussian blurring to apply to the outer edges of the hotspot area. Required to prevent sudden phase shift (grating-to-zero) edges, which cause unwanted discontinuities in the output beam. Testing has shown blur = 5 to be optimal.

# innerBlur: The radius of Gaussian blurring to apply to the inner hotspot area. Without this value, grating would gain problematic and unwanted noise. Testing has shown innerBlur = 15 to be optimal, but can vary between ~5-25.

# range: Theoretically used to calculate the max absolute difference between input image and goal image to check how close the input beam is to being "flat".

# maxIter: Number of max iterations of the function to try and flatten the beam before exiting. Currently not being used.

# yshift: Adding constant vertical shift to the applied grating. For testing purposes

# plot: When set to True, will plot whichever lineouts are uncommented. To visualize certain steps in the process for testing and debugging.

#####




def feedback(image_transform, SLM_height, SLM_width, count = 0, initial = None, initialArray = None, threshold = 75, plot = False, innerBlur = 15, blur = 15, rangeVal=5, testno=0):
    global aboveMultArray, belowMultArray, totalMultArray, totalMultImg, xi, yi, goalImg, goalArray, stacked, stacked2, x, y
    
    # Open calVals.csv, which houses the 5 values for SLM-CCD calibration. Use these values to rescale/reposition "initialImg" to match SLM
    # df = pd.read_csv('./calibration/calVals.csv', usecols=['xZoom', 'yZoom', 'xShift', 'yShift', 'angle'])

    #####
    # Open the initial beam image from the "SLM" folder in GDrive. Function input should be a PNG filepath with no extension
    # For implementation: input is in the form of a numpy 2D array (initialArray)
    #####
    
    if initial != None:
        # initialImg = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/" + str(initial) + ".png")
        print("There has been a catastrophic disaster.")

    if np.any(initialArray != None):
        initialImg = Image.fromarray(initialArray)
        # print(np.amax(initialArray))
    
    blazed = Image.open('./settings/PreSets/HAMAMATSU/HAMAMATSU_2px.png')
    blazedData = asarray(blazed)
    initialImgArray = asarray(initialImg)
    initialArray = cv2.warpPerspective(initialImgArray, image_transform, (np.shape(blazedData)[1], np.shape(blazedData)[0]), flags=cv2.INTER_LINEAR)
         # Turn initial image into 2D array of pixel intensity values
    # print(np.shape(initialArray))

    #####
    # Initial testing to use peak-to-valley to find "threshold image" instead of manually inputting a threshold
    #####
    
    cX, cY = center(initialArray)
    
    
    if count == 0:
        threshold = np.mean(sorted(initialArray.flatten(), reverse=True)[50]) * 0.75
    else:
        threshold = threshold
    
    
    #####
    # Creating "goal" or "target" image (turn every pixel above the threshold to the threshold). What the final beam should look like.
    # For every additional trial (count != 0), any pixels above the threshold which were not previously above the threshold ("unique") are added to the goal image and included in the current grating calculation
    #####
    
    if count == 0:
        xi, yi = (initialArray >= int(threshold-5)).nonzero()
        stacked = np.stack((xi, yi), axis=-1)     # Must stack array in order to properly append new pixel coordinates to the array
    else:
        x, y = (initialArray >= int(threshold-10)).nonzero()
        stacked2 = np.stack((x, y), axis = -1)
        unique = np.unique(np.concatenate((stacked, stacked2)),axis=0)
        unstacked = np.stack(unique, axis=1)
        xi, yi = unstacked[0], unstacked[1]
        
    goalArray = initialArray.copy()
    goalArray[xi,yi] = int(threshold)
    goalArray = gaussian_filter(goalArray, sigma = 10)
    goalImg = Image.fromarray(goalArray)
    goalMap = goalImg.load()
    
    
    goalArrayBlurred = gaussian_filter(goalArray, sigma = 10)
    goalImgBlurred = Image.fromarray(goalArrayBlurred)


    #####
    # Take difference between initial image and goal image to find which pixels are brighter and which are dimmer compared to threshold
    #####
    
    
    image1 = np.int32(initialArray)     # Open initial image
    image2 = np.int32(goalImg)     # Open goal image
    diffImgArray = cv2.subtract(image1, image2)     # Take difference between two images. Initial - goal. Positive numbers = too bright, negative = too dim. np.int32 to account for negative numbers -255 to +255
    diffImg = Image.fromarray(diffImgArray)
    
    aboveImgArray = diffImgArray.copy()
    belowImgArray = diffImgArray.copy()
    xa, ya = (aboveImgArray > 0).nonzero()     # Find coordinates of pixels which are above and below the threshold
    xb, yb, = (belowImgArray < 0).nonzero()
    aboveImgArray[xb, yb] = 0     # Using the diffImg array, take all pixels that are NOT above the threshold and set to zero. Remaining pixels are above the threshold, creating aboveImg
    belowImgArray[xa, ya] = 0     # Opposite for belowImg
    belowImgArray = np.abs(belowImgArray)     # Turn belowImg positive, to subtract from grating later
    aboveImgArray = np.abs(np.int8(aboveImgArray))     # Turn into 0-255 brightness values
    belowImgArray = np.abs(np.int8(belowImgArray))
    
    aboveImg = Image.fromarray(aboveImgArray, "L")
    belowImg = Image.fromarray(belowImgArray, "L")
    
    
    #####
    # Take all pixels above and below threshold and blur the image using innerBlur value. This emits a certain amount of noise inherent to the input beam, so that these high frequency oscillations do not cause issues when calculating and appling the grating. Essentially just want to find the "outline" of the aboveImg and belowImg to be used to multiply by the grating.
    #####
    
    aboveImgGray = ImageOps.grayscale(aboveImg.copy())
    aboveImgBlurred = aboveImgGray.filter(ImageFilter.GaussianBlur(radius = innerBlur))
    aboveBlurredArray = asarray(aboveImgBlurred, dtype=np.int32)
    
    belowImgGray = ImageOps.grayscale(belowImg.copy())
    belowImgBlurred = belowImgGray.filter(ImageFilter.GaussianBlur(radius = innerBlur))
    belowBlurredArray = asarray(belowImgBlurred, dtype=np.int32)
    
    #####
    # Take all pixels above and below threshold and set to 255 (max). This is just to find the "edges" of aboveImg (the boundary between 255 and 0), which will receive a Gaussian blur. This causes the final grating image to have soft, gaussian sloping edges instead of sharp cutoff edges, which cause visible phase issues in the resulting beam image.
    #####
    
    aboveImgMaxArray = aboveImgArray.copy()
    belowImgMaxArray = belowImgArray.copy()
    aboveImgMaxArray = np.uint8(aboveImgMaxArray)
    belowImgMaxArray = np.uint8(belowImgMaxArray)
    
    aboveImgMaxArray[xa, ya] = 255
    belowImgMaxArray[xb, yb] = 255
    
    aboveImgMax = Image.fromarray(aboveImgMaxArray, "L") 
    belowImgMax = Image.fromarray(belowImgMaxArray, "L")
    
    aboveImgMaxGray = ImageOps.grayscale(aboveImgMax.copy())
    belowImgMaxGray = ImageOps.grayscale(belowImgMax.copy())
        
    aboveMaxBlurred = aboveImgMaxGray.filter(ImageFilter.GaussianBlur(radius = blur))
    aboveMaxBlurredArray = asarray(aboveMaxBlurred, dtype=np.int32) # int32
    
    belowMaxBlurred = belowImgMaxGray.filter(ImageFilter.GaussianBlur(radius = blur))
    belowMaxBlurredArray = asarray(belowMaxBlurred, dtype=np.int32) # int32
    
    
    #####
    # Initialize final grating array (multArray)
    #####
    
    
    if count == 0:
        aboveMultArray = np.zeros(initialArray.shape)
        belowMultArray = np.zeros(initialArray.shape)
        totalMultArray = np.zeros(initialArray.shape)

    
    aboveMultArray2 = aboveMultArray     # Save previous multArray as multArray2 to take average later
    aboveMultArray2Blurred = asarray(Image.fromarray(aboveMultArray2, "L").filter(ImageFilter.GaussianBlur(radius = blur)), dtype = np.int32)
    
    aboveMultArray = np.multiply(aboveMaxBlurredArray, blazedData)     # Final grating should take into account the "edges" or "boundaries" of the threshold area, and should have blurred edges. This multiplies the blurred edges by the previously created grating image.
    aboveMultArray = np.multiply(aboveMultArray, aboveBlurredArray)     # Final grating should also take into account the general shape of the threshold area. So pixels 50 above the threshold should receive less intense grating, while pixels 150 above the threshold should receive more intense grating. This takes the shape (values) into account
    
    # aboveMultArray = np.multiply(aboveBlurredArray, blazedData)     # This one does not have to be used. Added for testing. The above two lines would be replaced with this line.
    
    
    belowMultArray2 = belowMultArray
    belowMultArray = np.multiply(belowMaxBlurredArray, blazedData)
    # belowMultArray = np.multiply(belowMultArray, belowBlurredArray)
    belowMultArray = np.multiply(belowBlurredArray, blazedData)
    
    #####
    # Since multiple arrays were multiplied together, now must normalize the final grating array to the intended amplitude
    #####
    
    if np.amax(aboveMultArray) != 0:
        aboveMultArray = (aboveMultArray * np.amax(aboveBlurredArray) / (np.amax(aboveMultArray))).astype(np.int32) # Normalize multiplied grating to the max of the subtracted image
    if np.amax(belowMultArray) != 0:
        belowMultArray = (belowMultArray * np.amax(belowBlurredArray) / (np.amax(belowMultArray))).astype(np.int32)

    totalMultArray2 = totalMultArray.astype(np.int32)     # Copy final grating array (totalMultArray) to take average later

    
    #####
    # Find difference between threshold and max of result image and turn into multiplication of above and below. Used to add and subtract by smaller increments as image gets closer to goal
    #####
    

    coords = np.stack((xi, yi), axis=1)
    initialVals = initialArray[[xi],[yi]]
    initialMax = np.amax(initialVals)
    initialMin = np.amin(initialVals)
    initialAvg = np.mean(initialVals[0])
    diff = np.abs(initialAvg - threshold)
    pv = np.abs(initialMax - initialMin)
    diffMult = diff/100*2
    maxDiff = np.abs(initialMax - threshold)
    minDiff = np.abs(initialMin - threshold)

    
    #####
    # "diff" is calculated as absolute difference between the average values of the input beam's threshold area and the threshold value. Average is used to exclude any single-pixel bright specks. This does not currently stop the algorithm, it is just to print a notice once the flattening is sufficient. However, could be used to end the algorithm entirely
    #####
    
    diffTest = False
    pvTest = False
    rangeTest = False
    allTest = False
    
    print("DIFF: " + str(diff))
    print("PV: " + str(pv))
    print("MAXDIFF: " + str(maxDiff))

    if diff <= 5.0:
        print("ERROR LESS THAN 5")
        diffTest = True
    
    if pv <= 10:
        print("PEAK-TO-VALLEY LESS THAN 10")
        pvTest = True
    
    if maxDiff <= rangeVal and minDiff <= rangeVal:
        print("MAX AND MIN RANGE WITHIN 5")
        rangeTest = True
    
    if diffTest == True and pvTest == True and rangeTest == True:
        print("ALL CHECKS NOMINAL. FLATTENING COMPLETE.")
        allTest = True
    
    #####
    
    # totalMultArray = (totalMultArray2 + diffMult * aboveMultArray - diffMult * belowMultArray).astype(np.int32)
    # totalMultArray = (totalMultArray2 + 0.5 * aboveMultArray - 0.5 * belowMultArray).astype(np.int32)     # Add and subtract 1/2 of the above and below arrays. More conservative application, but slower. Use if encounter positive feedback loop issues.
    totalMultArray = (totalMultArray2 + aboveMultArray/2 - belowMultArray/2).astype(np.int32)     # Simply add the calculated array for pixels above threshold and subtract array for pixels below threshold. Should work in most cases.
    
    totalMultArray[totalMultArray < 0] = 0     # Sometimes, subtracting belowMultArray leads to negative grating values (overcorrection). This does not work with SLM, so change all negative numbers to zero



    #####
    # WAVEFRONT CORRECTION TEST
    #####
    
    
    # totalMultArray[xi,yi] = totalMultArray[xi,yi] + yshift
    yshiftArray = np.ones(shape = totalMultArray.shape)     # Initialize yshift array
    # print(yshiftArray[0][0])
    # yshiftArray = yshiftArray * 70
    # print(yshiftArray[0][0])
    # yshiftArray = yshiftArray
    # print(yshiftArray[0][0])
    
    # yshiftArray[xi,yi] = totalMultArray[xi,yi]     # Shift grating arary proportional to the local value of the grating array. Creates yshift the same shape as the grating
    # yshiftArray[xi,yi] = 70 - totalMultArray[xi,yi] * 2     # Shift entire grating upward, and antiproportional to shape of grating. With some tweaking, this creates a final grating which has a flat top (all values match at top) and the yshift mirrors that
    # yshiftArray[xi,yi] = 50     # Constant yshift ONLY IN THE THRESHOLD AREA. Gaussian blur below ensures smooth transition back to zero outside the threshold area.
    # yshiftArray[xi,yi] = 70 - (totalMultArray[xi,yi] **2) / 100     # Squaring totalMultArray accounts LESS for the shape of totalMultArray. Just testing other ways to make different yshift shapes.

    
    yshiftArray = gaussian_filter(yshiftArray, sigma = 15)     # Smooth transition from yshift to zero. Testing shows ideal sigma value of 15.
    # totalMultArray = totalMultArray + yshiftArray     # Directly add yshift to previous grating
    totalMultArray = totalMultArray
    
    
    
    ######
    
    totalMultArray = totalMultArray.astype(np.uint8)

    aboveMultImg = Image.fromarray(aboveMultArray, "L") # mode = L
    
    totalMultImg = Image.fromarray(totalMultArray, "L") # mode = L
    if count == 0:
        for i in np.arange(SLM_width):
            initialImg.putpixel((i, cY), int(255))
        # initialImg.show()
    
    # pd.DataFrame(xi).to_csv('xi.csv')
    # pd.DataFrame(yi).to_csv('yi.csv')
    
    # totalMultImg.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/feedbackAlgorithm/test" + str(testno) + "/" + str(count+1) + "TEST_15AMP_SIMGA20.png")
      
    
    #####
    # Make lineout plots of images to easily visualize values and shapes. Used for diagnostics and testing of algorithm
    #####
    
    if plot:
        
        plt.plot(np.arange(SLM_width), totalMultArray[cY,:], label = "SLM Grating", color = "C2")
        plt.plot(np.arange(SLM_width), initialArray[cY,:], label = "Initial")
        plt.plot(np.arange(SLM_width), goalArray[cY,:], label = "Goal")

        
        plt.legend()
        plt.xlim(cX-400,cX+400)
        plt.ylim(0,260)
        plt.title("Test " + str(testno) + ", Trial " + str(count) + ", AveDiff = " + str(np.round(diff,2)))
        # plt.savefig("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/feedbackAlgorithm/test" + str(testno) + "/plot" + str(count) + "TEST_15AMP_SIGMA20.png")
        plt.show()



    return totalMultImg, totalMultArray, goalArray, diff, threshold, allTest
    
    #################
