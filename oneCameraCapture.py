import os

os.environ["PYLON_CAMEMU"] = "3"

from pypylon import genicam
from pypylon import pylon
import sys
import time
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, PhotoImage, filedialog
from tkinter.filedialog import askopenfile
import video_display
from PIL import Image, ImageTk
import pandas as pd
from SLM_HAMAMATSU import *
import os

class cameraCapture(tk.Frame):

    def __init__(self, page_instance, window2_instance):
        self.img0 = []
        self.windowName = 'SLM CCD'
        self.page = page_instance
        self.window2 = window2_instance
        # self.SLMdisp = Image.open('10lpmm_190amp.png')

        self.SLMdisp = Image.fromarray(np.zeros((1080,1920)))
        try:
            df = pd.read_csv('prevVals.csv', usecols=['exposure','gain'])
            # Create an instant camera object with the camera device found first.
            # maxCamerasToUse = 2
            # get transport layer and all attached devices
            tlf = pylon.TlFactory.GetInstance()
            devices = tlf.EnumerateDevices()
            NUM_CAMERAS = len(devices)
            os.environ["PYLON_CAMEMU"] = f"{NUM_CAMERAS}"
            exitCode = 0
            if NUM_CAMERAS == 0:
                raise pylon.RuntimeException("No camera connected")
            else:
                print(f'{NUM_CAMERAS} cameras detected:\n')
                
                for counter, device in enumerate(devices):
                    print(f'{counter}) {device.GetFriendlyName()}') # return readable name
                    print(f'{counter}) {device.GetFullName()}\n') # return unique code
            self.camera = pylon.InstantCamera(tlf.CreateDevice(devices[0]))
            # running=False
            # Print the model name of the camera.
            print("Using device ", self.camera.GetDeviceInfo().GetModelName())

            # self.camera.PixelFormat = "Mono8"
            self.camera.Open()  #Need to open camera before can use camera.ExposureTime
            # self.camera.PixelFormat = "Mono8"
            self.camera.ExposureTimeRaw = int(df.exposure[0])
            self.camera.GainRaw = int(df.gain[0])

            # Print the model name of the camera.
            # print("Using device ", self.camera.GetDeviceInfo().GetModelName())
            # print("Exposure time ", self.camera.ExposureTime.GetValue())

            # According to their default configuration, the cameras are
            # set up for free-running continuous acquisition.
            #Grabbing continuously (video) with minimal delay
            self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 

            # converting to opencv bgr format
            self.converter = pylon.ImageFormatConverter()
            self.converter.OutputPixelFormat = pylon.PixelType_Mono8
            self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        # except genicam.GenericException as e:
        #     # Error handling
        #     print("An exception occurred.", e.GetDescription())
        #     exitCode = 1

        except Exception as error:
            print(error)
            pass

    def getFrame(self):
        try:
            self.grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if self.grabResult.GrabSucceeded():
                image = self.converter.Convert(self.grabResult) # Access the openCV image data
                self.img0 = image.GetArray()

            else:
                print("Error: ", self.grabResult.ErrorCode)
    
            self.grabResult.Release()
            #time.sleep(0.01)

            return self.img0
            
        except genicam.GenericException as e:
            # Error handling
            print("An exception occurred.", e.GetDescription())
            exitCode = 1

    def exposure_change(self):
        try:
            self.camera.ExposureTimeRaw = int(self.page.exposure_entry.get())
            self.page.exposure_entry.config(background="white")
        except Exception as error:
            print(error)
            self.page.exposure_entry.config(background="red")

    def gain_change(self):
        try:
            self.camera.GainRaw = int(self.page.gain_entry.get())
            self.page.gain_entry.config(background="white")
        except Exception as error:
            print(error)
            self.page.gain_entry.config(background="red")

    def save_image(self):
        filename = self.page.save_entry.get()
        try:
            cv2.imwrite(f'{filename}.png', self.img0)  # Save the captured image to a file
            print(f"Image saved as {filename}.png")
            self.page.save_button.config(background="SystemButtonFace")
        except Exception as error:
            print(error)
            self.page.save_button.config(background="red")
    
    def browse(self):
        global img
        try:
            f_types = [('hurry up and pick one', '*.png')]
            filename = filedialog.askopenfilename(filetypes=f_types)
            self.browseImg = Image.open(filename)
            # img_width = img.width()
            # img_height = img.height()
            self.browseImgArray = np.asarray(self.browseImg)
            self.page.browse_button.config(background='SystemButtonFace')
        except Exception as error:
            self.page.browse_button.config(background='red')
            print(error)

    def displayToSLM(self):
        try:
            self.SLMdisp = Image.fromarray(self.browseImgArray)
            self.page.display_button.config(background='SystemButtonFace')
        except AttributeError as error:
            print("NO IMAGE SELECTED")
            # print(error)
            self.page.display_button.config(background='red')
        except Exception as error:
            print(error)

    def clearSLM(self):
        self.SLMdisp = Image.fromarray(np.zeros((1080,1920)))

    def stopGUI(self):
        # self.camera.StopGrabbing()
        # print("Stopped")
        pass

    def exitGUI(self):
        print("GOODBYE")
        df = pd.DataFrame({'exposure': [self.page.exposure_entry.get()],
                           'gain': [self.page.gain_entry.get()]})
        df.to_csv('prevVals.csv', index=False)
        self.page.window.destroy()
        self.camera.Close
    
    def testFunc(self):
        # print(self.page.gain_entry.get())
        # df = pd.DataFrame({'exposure': [self.page.exposure_entry.get()],
        #                    'gain': [self.page.gain_entry.get()]})
        # df.to_csv('prevVals.csv', index=False)
        pass

    def nloops(self):
        print("BEGINNING")
        numLoops = 5
        for i in np.arange(numLoops):
            print("BLOOP")
            if  i == 0:
                gratingImg, gratingArray, diff, threshold, allTest = feedback(
                    count = i,
                    plot = True,
                    initialArray = self.img0
                )
            else:
                gratingImg, gratingArray, diff, threshold, allTest = feedback(
                    count = i,
                    plot = True,
                    threshold = threshold,
                    initialArray = self.img0
                )
            self.SLMdisp = Image.fromarray(gratingArray)
            self.page.update()
            time.sleep(1)
            print("ELOOP")
    
    def runThrough(self):
        # for pol in np.arange(0,360,10):
        #     for gray in np.arange(0, 260, 10):
        gray=160
        # self.SLMdisp = Image.open("./HMPolTests/HAMAMATSU_"+str(gray)+".png")
        self.SLMdisp = Image.open("./calibration/HAMAMATSU/HAMAMATSU_2px_crosshair.png")
        print("Image displayed.")
        
        # self.page.update()
        # input("Press enter to continue....")
        # cv2.imwrite(f'./HMPolTests/testImg.png', self.img0)  # Save the captured image to a file
        # print(f"Image saved as testImg.png")

if __name__ == "__main__":
    testWidget = cameraCapture()
    while testWidget.camera.IsGrabbing():
        #input("Press Enter to continue...")
        testWidget.getFrame()