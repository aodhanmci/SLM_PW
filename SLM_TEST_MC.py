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


def algorithm():
    # setup the grid
    # x=np.linspace(-2000, 2000, 4000)
    # y=xh
    x = np.arange(1920)
    y = np.arange(1080)
    width = 1920
    height = 1080
    
    [MeshX, MeshY]=np.meshgrid(x,y) 
    [sy,sx]=np.shape(MeshX)
    mid=int(np.fix(sx/2))
    
    sigma1=400 # just the standard deviation for the gaussian profile i.e create a gaussian near field
    # Efield_amplitude=np.exp(-(MeshX**2+MeshY**2)/sigma1**2) # amplitude of the electric field. i.e. real component
    
    initialImgPath = "/superGaussian300"
    initial_img = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM" + str(initialImgPath) + ".png")
    W, H = initial_img.size
    initial_img = ImageOps.grayscale(initial_img)
    initial_imgMap = initial_img.load()
    Efield_amplitude = asarray(initial_img)
    
    
    
    E_initial_phase = np.zeros_like(Efield_amplitude) # assuming the initial beam has zero phase everywhere
    E_initial = Efield_amplitude + 1j*E_initial_phase # full description of the electric field with real and imaginary (amplitude and phase)
    
    I_initial=np.abs(E_initial)**2 # intensity
    input_total = np.sum(I_initial)
    
    # print(I_initial.shape)
    
    # PhaseMapX = signal.sawtooth(2 * np.pi * 100 * MeshX/np.max(MeshX)) # sawtooth pattern
    # PhaseMapX = ((np.sin(((2*3np.pi/0.05))*MeshX))) # sinusoidal grating
    # PhaseMapX=MeshX/np.max(np.max(MeshX)) # linear ramp
    # PhaseMapX = np.zeros_like(MeshX) # zero phase
    
    # Custom phasemap
    
    phase_map = Efield_amplitude.copy()
    
    blazed = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/blazed/5lpmm_200amp.png")
    blazedMap = blazed.load()
    
    blazedData = asarray(blazed) # Numpy array of blazed pattern to overlay on initial beam image input
    
    limit = 200
    
    xa, ya = (phase_map > limit).nonzero() # Coordinates of pixels greater than limit, to apply blazed grating
    xn, yn = (phase_map <= limit).nonzero() # Coordinates of pixels less than limit, to set to zero
    
    phase_map[xa,ya] = blazedData[xa,ya] # Overlay blazed image where necessary
    phase_map[xn, yn] = 0 # Set rest of image to black
    
    
    PhaseMapX = phase_map
    
    
    am = np.pi # amplitude
    E_initial= E_initial*np.exp(PhaseMapX*am*1j) # mutiply the 2 phases together
    E_fourier=np.fft.fft2(E_initial) #  fourier transform is like looking at the far field
    E_fourier=np.fft.fftshift(E_fourier)
    I_fourier=(np.abs(E_fourier))**2
    
    
    
    ###############
    # spatial filter
    ###############
    radius=10
    xcenter=width/2
    # xcenter=width/2 + 490
    ycenter=height/2
    SignMask=np.sign(1-np.sign((MeshX-xcenter)**2+(MeshY-ycenter)**2-radius**2))
    th=np.linspace(0, 2*np.pi, 90) 
    xunit=radius*np.cos(th)+xcenter
    yunit=radius*np.sin(th)+ycenter
    E_fourier_after_filter=E_fourier*SignMask
    ################
    
    
    E_final=np.fft.ifft2(E_fourier_after_filter)
    I_final=np.abs(E_final)**2
    I_fourier_after_filter=(np.abs(E_fourier_after_filter))**2
    
    # display(I_initial)
    
    output_total = np.sum(I_final)
    
    maxmax=np.max(np.max(I_fourier))
    minmin=np.min(np.min(I_fourier))
    
    
    fig, ax = plt.subplots(2, 4, figsize=(26, 8))
    
    ax[0, 0].imshow(I_initial, vmin = 0, vmax = 65025, extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto')
    # ax[0, 0].imshow(I_initial)
    # ax[0, 0].set_xlim(-500, 500)
    # ax[0, 0].set_ylim(-500, 500)
    ax[0, 0].set_xlabel('x')
    ax[0, 0].set_ylabel('y')
    ax[0, 0].set_title('2D Intensity Profile (I_initial)', fontsize = 25)
    print("I_initial min: " + str(np.amin(I_initial)))
    print("I_initial max: " + str(np.amax(I_initial)))
    
    ax[1, 0].plot(x, I_initial[int(height/2), :])
    ax[1, 0].set_ylim(0, 65025)
    
    ax[0, 1].imshow((np.angle(E_initial)), vmin = -np.pi, vmax = np.pi, extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto')
    ax[0, 1].set_title('2D Phase Structure SLM (E_initial)', fontsize = 25)
    # ax[0, 1].set_xlim(-500, 500)
    # ax[0, 1].set_ylim(-500, 500)
    print("E_initial min: " + str(np.amin(np.angle(E_initial))))
    print("E_initial max: " + str(np.amax(np.angle(E_initial))))
    
    
    ax[1, 1].plot(x, (np.angle(E_initial[int(height/2), :])))
    # ax[1, 1].set_xlim(800, 1000)
    # ax[1, 1].set_ylim(-4, 4)
    ax[1, 1].set_title('Phase Lineout [radians]', fontsize = 25)
    
    
    ax[0, 2].imshow(I_fourier, vmin = 0, vmax = 1000000000000, extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto')
    ax[0, 2].plot(xunit, yunit,  c='k')
    ax[0, 2].set_title('fourier no filter (I_fourier)', fontsize = 25)
    # ax[0, 2].set_xlim(width/2-900, width/2+900)
    ax[0, 2].set_ylim(height/2-100, height/2+100)
    print("I_fourier min: " + str(np.amin(I_fourier)))
    print("I_fourier max: " + str(np.amax(I_fourier)))
    
    ax[1, 2].plot(x, I_fourier[int(height/2), :])
    # ax[1, 2].set_xlim(width/2-10, width/2+10)
    
    # ax[1, 2].set_ylim(0, 1000000000000000)
    
    # ax[0, 3].imshow(I_fourier_after_filter, vmin=minmin, vmax=maxmax, extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto')
    # ax[0, 3].set_title('fourier filtered (I_fourier_after_filter)')
    # ax[0, 3].set_xlim(xcenter - 200, xcenter + 200)
    # ax[0, 3].set_ylim(ycenter - 50, ycenter + 50)
    
    ax[0, 3].imshow(I_final, vmin = 0, vmax = 65025, extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto')
    # print(np.max(np.max(I_final)))
    ax[0, 3].set_title('Intensity after filtering (I_final)', fontsize = 25)
    # ax[2, 1].set_xlim(-500, 500)
    # ax[2, 1].set_ylim(-500, 500)
    print("I_final min: " + str(np.amin(I_final)))
    print("I_final max: " + str(np.amax(I_final)))
    
    ax[1, 3].plot(x, I_final[int(height/2), :])
    ax[1, 3].plot(x, I_initial[int(height/2), :])
    ax[1, 3].set_ylim(0, 65025)
    
    
    
    fig.tight_layout()
    plt.show()
    print(f'Energy throughput={np.round(output_total/input_total,2)*100}%')
    
    # plt.close()
    # # plt.plot(I_initial[540, :])
    # # plt.plot(I_final[540, :])
    # plt.plot(E_initial[540, :])
    # plt.show()
    # finalImg = Image.fromarray(I_initial, "L")
    # display(finalImg)
    # print(I_final[700][int(height/2)])
    # print(np.amax(I_final))
    # plt.plot(x, I_final)
    # np.shape(I_final)
    
    
    
    # finalImg = np.array(I_initial, dtype=np.int32) # WORKS
    # finalImg = Image.fromarray(finalImg, "I") # WORKS
    
    # print(type(E_final[0][0]))
    # finalImg = np.array(I_final)
    # print(type(E_initial[0][0]))
    # print(type(np.imag(E_final[0][0]))) # np float 64
    
    # finalImg = np.array(np.abs(np.real(E_initial)), dtype=np.int8) # WORKS
    # finalImg = Image.fromarray(finalImg, "L") # WORKS
    
    
    # print(np.amax(np.real(E_initial)))
    
    finalImg = np.array(np.abs(np.real(E_final)), dtype=np.int8) # WORKS
    finalImg = Image.fromarray(finalImg, "L") # WORKS
    
    
    finalImg = finalImg.copy()
    finalMap = finalImg.load()
    
    # finalImg.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/feedbackAlgorithm/output1.png")
    
    
    # display(finalImg)
    # strip = []
    # for i in np.arange(width):
    #     # finalMap[i,height/2] = 255
    #     strip = np.append(strip, finalMap[i,height/2])
    
    # display(finalImg)
    
    # plt.plot(np.arange(width), strip)
    # plt.title("I_initial")
    # plt.show()
    
    
    # USE E_FINAL AS THE NEXT INITIAL BEAM; INCLUDES BOTH AMPLITUDE AND PHASE (WHICH IS ZERO)
    
    

"""


# algorithm()

initialImgPath = "/superGaussian300"
initial_img = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM" + str(initialImgPath) + ".png")
initial_img_map = initial_img.load()
initial_img_array = asarray(initial_img, dtype = np.int32)

output_img = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/feedbackAlgorithm/output1.png")
output_img_map = output_img.load()
output_img_array = asarray(output_img, dtype = np.int32)
# print("Output size: " + str(output_img.size))

target_img = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/feedbackAlgorithm/targetImage.png")
target_img_map = target_img.load()
target_img_array = asarray(target_img, dtype = np.int32)

# ox, oy = (output_img_array - target_img_array).nonzero()

final_img_array = np.subtract(target_img_array, output_img_array)
# print(type(final_img_array[0][0])) # np.int16
final_img_array = final_img_array.astype(np.float32)
# print(np.amin(final_img_array))

final_img = Image.fromarray(final_img_array, "F")
# final_img = ImageOps.grayscale(final_img)
# final_img = Image.fromarray(final_img_array)
final_img_map = final_img.load()
# display(final_img)



width, height = final_img.size

final_strip = []
initial_strip = []
output_strip = []
target_strip = []
for i in np.arange(width):
    final_strip = np.append(final_strip, final_img_map[i,height/2])
    initial_strip = np.append(initial_strip, initial_img_map[i,height/2])
    output_strip = np.append(output_strip, output_img_map[i,height/2])
    target_strip = np.append(target_strip, target_img_map[i,height/2])

# plt.plot(np.arange(width), final_strip, label = "Final")
# plt.plot(np.arange(width), initial_strip, label = "Initial")
# plt.plot(np.arange(width), output_strip, label = "Output")
# plt.plot(np.arange(width), target_strip, label = "Target")
# plt.legend()
# plt.show()
# """



# print(np.amin(final_img_array))





###########################
# MAKING UNIQUE BLAZE IMAGE
###########################


# """
# width, height = initial_img.size
# n = 5
# m = n*12.5
# y_shift = 1
# amplitude2 = 255



# blaze2 = Image.new('P', size = (width, height))
# blaze2 = ImageOps.grayscale(blaze2)
# x = np.linspace(0, 1, width)
# y = np.linspace(0, 1, height)
# [MeshX, MeshY]=np.meshgrid(x,y) 
# # xi = np.linspace()
# # yi = np.arange(30, 60)
# xi = x[0:int(width/2)]
# yi = y[0:int(height/2)]
# [MeshXi, MeshYi] = np.meshgrid(xi,yi)
# # signal = ((signal.sawtooth(2 * np.pi * m * MeshX)+y_shift)/2)*10
# # signal = ((signal.sawtooth(2 * np.pi * m * MeshX)+y_shift)/2)*10
# signal = ((signal.sawtooth(2 * np.pi * m * MeshX)+y_shift)/2)*255
# # print(np.amax(signal))

# # print(type(signal[0][0])) $ Float 64
# signal = signal.astype(np.int8)
# testImg = Image.fromarray(signal, "L")
# test_img_map = testImg.load()
# # display(testImg)
# test_strip = []
# mult_strip = []
# test_strip2 = []

# # mult = np.multiply(signal, final_img_array)
# # mult = np.abs(signal * final_img_array / 100)
# mult = signal
# # signal2 = signal
# # signal2 = signal2 * 0.8
# # signal = np.abs(signal * 1)
# # mult = np.abs(signal)
# # print(signal[0][17])
# # mult_img = Image.fromarray(mult, "L")
# mult_img = Image.fromarray(signal, "L")
# # display(mult_img)
# # print(np.amax(mult))
# mult_img_map = mult_img.load()
# # print(signal[0][5])

# for i in np.arange(width/2):
#     test_strip = np.append(test_strip, test_img_map[i,height/2])
#     # test_strip = np.append(test_strip, test_img_map[height/2,i])
#     # mult_strip = np.append(mult_strip, mult_img_map[i,height/2])
#     # test_strip2 = np.append(test_strip2, signal[int(height/2)][i])


# plt.plot(np.arange(width/2), test_strip, label = "Signal")
# # plt.plot(np.arange(width), mult_strip, label = "Mult")
# # plt.plot(np.arange(width), final_strip, label = "Final Strip")
# # plt.plot(np.arange(width), test_strip2, marker = "o", linestyle = " ", label = "Signal Array")
# # plt.plot(np.arange(width)[5], signal[0][5], marker = "o", linestyle = " ", color = "yellow", label = "Special Boi")
# plt.legend()
# plt.xlim(0, 50)
# plt.ylim(0, 255)
# plt.show()



def calibration():
    # lenspaper = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/lensPaper/crosshair4Img3.png")
    # lenspaper = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/feedbackAlgorithm/test51/crosshairImg.png")
    lenspaper = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/feedbackAlgorithm/testResult.png")
    # display(lenspaper)
    lenspaper = ImageOps.flip(ImageOps.mirror(lenspaper))
    # display(lenspaper)
    
    crosshair4 = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/lensPaper/crosshair4.png")
    width, height = crosshair4.size
    # display(crosshair4)
    # lenspaper = lenspaper.resize([int(width*2), int(height)])
    
    def zoom_at(img, x, y, zoom):
        global w, h
        w, h = img.size
        # print(w,h)
        zoom2 = zoom * 2
        img = img.crop((x - w / zoom2, y - h / zoom2, 
                        x + w / (zoom2*0.86), y + h / (zoom2*1.06)))
        return img.resize((width, height), Image.Resampling.LANCZOS)
    
    lenspaper = zoom_at(lenspaper, width/2 - 151, height/2 + 15, 1)
    lenspaper = lenspaper.rotate(1.2)
    
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
    
    
    
    
# """

lenspaper = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/lensPaper/12.3mA_donut.png")
# print(lenspaper.size)
# lenspaper = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/lensPaper/hd.png")
# print(lenspaper.size)

# display(lenspaper)
lenspaper = ImageOps.flip(ImageOps.mirror(lenspaper))
# display(lenspaper)

crosshair4 = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/lensPaper/crosshair4.png")
width, height = crosshair4.size
# display(crosshair4)
# lenspaper = lenspaper.resize([int(width*2), int(height)])

def zoom_at(img, x, y, zoom):
    global w, h
    w, h = img.size
    # print(w,h)
    zoom2 = zoom * 2
    img = img.crop((x - w / zoom2, y - h / zoom2, 
                    x + w / (zoom2*0.86), y + h / (zoom2*1.06)))
    return img.resize((width, height), Image.Resampling.LANCZOS)

lenspaper = zoom_at(lenspaper, width/2 - 539, height/2 + 295, 1.61)
lenspaper = lenspaper.rotate(1.2)

# display(lenspaper)
# print(lenspaper.size)
# print(crosshair4.size)
# display(crosshair4)

lenspaperMap = lenspaper.load()
lenspaperArray = asarray(lenspaper)

finalArray = lenspaperArray.copy()

lenspaperMaxArray = lenspaperArray.copy()

# blazed = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/blazed/10lpmm_255amp.png")
# blazed = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/testImages/blazed/20lpmm_190amp.png")
blazed = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/feedbackAlgorithm/190_rectangle_vertical_lines_1px.png")
# blazedMap = blazed.load()
# display(blazed)
blazedData = asarray(blazed)


limit = 200

xa, ya = (lenspaperArray > limit).nonzero() # Coordinates of pixels greater than limit, to apply blazed grating
xn, yn = (lenspaperArray <= limit).nonzero() # Coordinates of pixels less than limit, to set to zero


lenspaperMaxArray[xa,ya] = 255
lenspaperMaxArray[xn,yn] = 0

lenspaperMax = Image.fromarray(lenspaperMaxArray)
# display(lenspaperMax)
lenspaperMaxMap = lenspaperMax.load()

lenspaperBlurred = lenspaperMax.filter(ImageFilter.GaussianBlur(radius = 5))
lenspaperBlurredMap = lenspaperBlurred.load()
lenspaperBlurredArray = asarray(lenspaperBlurred, dtype=np.int32) # int32
# display(lenspaperBlurred)
# print(type(lenspaperBlurredArray[0][0]))

multArray = np.multiply(lenspaperBlurredArray, blazedData)
multArray = np.multiply(multArray, lenspaperArray)
# multArray = multArray * blazedData
# multArray = np.multiply(lenspaperArray, blazedData)
# multArray = lenspaperBlurredArray * blazedData
# multArray = np.multiply(lenspaperBlurred)
# print(type(multArray[0][0]))
multArray = (multArray/np.amax(multArray)*np.amax(lenspaperArray)*lenspaperArray).astype(np.int32)
# multArray = (multArray/np.amax(multArray)*np.amax(lenspaperArray)).astype(np.int32)
# multArray = multArray.astype(np.int32)
# multArray = multArray.astype(np.int32)
# multArray = np.divide(multArray, 1)
# print(type(multArray[0][0]))
# print(np.amax(lenspaperArray))
# print(np.amax(multArray))
multImg = Image.fromarray(multArray, "I") # mode = I
multMap = multImg.load()
# display(multImg)
maxStrip = []
blurredStrip = []
multStrip = []
ogStrip = []
for i in np.arange(width):
    # maxStrip = np.append(maxStrip, lenspaperMaxMap[i,height/2])
    ogStrip = np.append(ogStrip, lenspaperMap[i,height/2])
    blurredStrip = np.append(blurredStrip, lenspaperBlurredMap[i,height/2])
    multStrip = np.append(multStrip, multMap[i,height/2])
# plt.plot(np.arange(width), maxStrip, label = "Max")

# plt.plot(np.arange(width), blurredStrip, label = "Blurred")
# plt.plot(np.arange(width), multStrip, label = "Mult")
# plt.plot(np.arange(width), ogStrip, label = "Original")
# plt.legend()
# plt.xlim(700,1200)
# plt.show()

# print(np.amin(multArray/255))



# finalArray[xa,ya] = blazedData[xa,ya] # Overlay blazed image where necessary
# finalArray[xn, yn] = 0 # Set rest of image to black



# finalImg = Image.fromarray(finalArray)
multImg = Image.fromarray(multArray)
# multImg = multImg.resize((1900,1200), Image.Resampling.LANCZOS)
# display(multImg)
# finalImg.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/lensPaper/donut_11.5mA_200_mask_50.png")
# multImg.save("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/lensPaper/12.3mA_donut_mult_200lim_5rad.png")

# display(multImg)

# display(finalImg)










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


















def displayt(image, text):
    # print(image)
    image2 = image.copy()
    draw = ImageDraw.Draw(image2)
    mf = ImageFont.truetype('/Users/anthonylu/Documents/LBNL/SLM/Roboto-Medium.ttf', 30)
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




def feedback(testno, count, initial = None, initialArray = None, threshold = 175, blur = 5, innerBlur = 15, range = 5, maxIter = 100, yshift = 4, plot = False):
    global aboveMultArray, belowMultArray, totalMultArray, totalMultImg, xi, yi, goalImg, goalArray, stacked, stacked2, x, y
    
    #####
    # Open the initial beam image from the "SLM" folder in GDrive. Function input should be a PNG filepath with no extension
    # For implementation: input is in the form of a numpy 2D array (initialArray)
    #####
    
    if initial != None:
        initialImg = Image.open("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/" + str(initial) + ".png")
    
    if initialArray != None:
        initialImg = Image.fromarray(initialArray)
    
    # display(initialImg)
    
    #####
    # A smaller version of the calibration function. Not the final implementation. Aligns CCD image to SLM screen, rescales, resizes
    #####
    
    # width, height = initialImg.size
    
    initialImg = ImageOps.flip(ImageOps.mirror(initialImg))     # With current setup, beam gets rotated 180° between the SLM and the CCD. Must align CCD image to match SLM screen before calculating grating
    
    initialImg = zoom_at(initialImg, width/2 - 151, height/2 + 15, 1)     # Not final implementation of zoom function
    initialImg = initialImg.rotate(1.2)     # Image is rotated 2°
    # initialImg = initialImg.convert("L")
    initialImgArray = asarray(initialImg)
    initialImgArray = cv2.normalize(initialImgArray, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8U)
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
    displayt(goalImg, "GoalImg")
    displayt(goalImgBlurred, "GoalBlurred")
    
    
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



    #####
    # WAVEFRONT CORRECTION TEST
    #####
    
    
    # """
    # wfCorrectionArray = wavefront()
    # totalMultArray = totalMultArray + wfCorrectionArray
    # if count == 0:
    # totalMultArray[xi,yi] = totalMultArray[xi,yi] + yshift
    yshiftArray = np.ones(shape = totalMultArray.shape)     # Initialize yshift array
    # print(yshiftArray[0][0])
    yshiftArray = yshiftArray * 70
    # print(yshiftArray[0][0])
    # yshiftArray = yshiftArray
    # print(yshiftArray[0][0])
    
    # yshiftArray[xi,yi] = totalMultArray[xi,yi]     # Shift grating arary proportional to the local value of the grating array. Creates yshift the same shape as the grating
    yshiftArray[xi,yi] = 70 - totalMultArray[xi,yi] * 2     # Shift entire grating upward, and antiproportional to shape of grating. With some tweaking, this creates a final grating which has a flat top (all values match at top) and the yshift mirrors that
    # yshiftArray[xi,yi] = 50     # Constant yshift ONLY IN THE THRESHOLD AREA. Gaussian blur below ensures smooth transition back to zero outside the threshold area.
    # yshiftArray[xi,yi] = 70 - (totalMultArray[xi,yi] **2) / 100     # Squaring totalMultArray accounts LESS for the shape of totalMultArray. Just testing other ways to make different yshift shapes.

    
    yshiftArray = gaussian_filter(yshiftArray, sigma = 15)     # Smooth transition from yshift to zero. Testing shows ideal sigma value of 15.
    totalMultArray = totalMultArray + yshiftArray     # Directly add yshift to previous grating
    # totalMultArray = totalMultArray
    
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
    print(aboveMultArray.shape)
    aboveMultImg = Image.fromarray(aboveMultArray, "L") # mode = L
    aboveMultMap = aboveMultImg.load()
    # display(multImg)
    
    totalMultImg = Image.fromarray(totalMultArray, "L") # mode = L
    # displayt(totalMultImg, "totalMult")
    # totalMultArray2 = totalMultArray.copy()
    # totalMultImg2 = Image.fromarray(totalMultArray2)
    # totalMultMap2 = totalMultImg2.load()
    
    # for i in np.arange(width):
    #     initialImg.putpixel((i, int(height/2-15)), int(255))
    # initialImg.show()
    
    
    
    
    
    
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
            aboveStrip = np.append(aboveStrip, aboveImgArray[int(height/2-15), i])
            belowStrip = np.append(belowStrip, belowImgArray[int(height/2-15), i])
            aboveMaxStrip = np.append(aboveMaxStrip, aboveImgMaxArray[int(height/2-15), i])
            belowMaxStrip = np.append(belowMaxStrip, belowImgMaxArray[int(height/2-15), i])
            aboveMaxBlurredStrip = np.append(aboveMaxBlurredStrip, aboveMaxBlurredArray[int(height/2-15), i])
            belowMaxBlurredStrip = np.append(belowMaxBlurredStrip, belowMaxBlurredArray[int(height/2-15), i])
            aboveMultStrip = np.append(aboveMultStrip, aboveMultArray[int(height/2-15), i])
            diffImgStrip = np.append(diffImgStrip, diffImgArray[int(height/2-15), i])
            initialStrip = np.append(initialStrip, initialArray[int(height/2-15), i])
            goalStrip = np.append(goalStrip, goalArray[int(height/2-15), i])
            aboveBlurredStrip = np.append(aboveBlurredStrip, aboveBlurredArray[int(height/2-15), i])
            belowMultStrip = np.append(belowMultStrip, belowMultArray[int(height/2-15), i])
            belowBlurredStrip = np.append(belowBlurredStrip, belowBlurredArray[int(height/2-15), i])
            totalMultStrip = np.append(totalMultStrip, totalMultArray[int(height/2-15), i])
            yshiftStrip = np.append(yshiftStrip, yshiftArray[int(height/2-15), i])
            goalBlurredStrip = np.append(goalBlurredStrip, goalArrayBlurred[int(height/2), i])
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
        plt.plot(np.arange(width), yshiftStrip, label = "YShift", color = "red")
        plt.plot(np.arange(width), goalBlurredStrip, label = "GoalBlurred")

        
        plt.legend()
        plt.xlim(750,1125)
        plt.ylim(0,260)
        plt.title("Test " + str(testno) + ", Trial " + str(count) + ", AveDiff = " + str(np.round(diff,2)) + ", 15AMP_SIGMA20")
        # plt.savefig("/Users/anthonylu/Library/CloudStorage/GoogleDrive-AnthonyLu@lbl.gov/.shortcut-targets-by-id/1VJBVeRRN_5zVF1Gqm0fEKW9dfVeRScci/SLM/feedbackAlgorithm/test" + str(testno) + "/plot" + str(count) + "TEST_15AMP_SIGMA20.png")
        plt.show()
        # """
        
        
        # displayt(totalMultMap2, "TotalMult2")
        

    


    # print("OOPS")

    return totalMultImg, diff
    
    #################


def runFeedback(testno):
    # while i <= 11:
    for i in np.arange(15):
        if i == 0:
            feedback(initial = "feedbackAlgorithm/test" + str(testno) + "/initial", testno = testno, count = i,
                        plot = True
                     )
        else:
            try:
                # file = None
                # while file == None:
                    
                feedback(initial = "feedbackAlgorithm/test" + str(testno) + "/" + str(i) + "Result", testno = testno, count = i,
                            plot = True
                         )
            except:
                # count = i - 1
                # time.sleep(5)
                # continue
                pass

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




calibration()












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















