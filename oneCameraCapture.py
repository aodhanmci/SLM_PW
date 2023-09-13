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

class cameraCapture(tk.Frame):

    def __init__(self, page_instance):
        self.img0 = []
        self.windowName = 'SLM CCD'
        self.page = page_instance
        # self.SLMdilp = Image.open('10lpmm_190amp.png')
        self.SLMdisp = Image.fromarray(np.zeros((1080,1920)))
        try:
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
            running=False
            # Print the model name of the camera.
            print("Using device ", self.camera.GetDeviceInfo().GetModelName())

            # self.camera.PixelFormat = "Mono8"
       
            self.camera.Open()  #Need to open camera before can use camera.ExposureTime
            # self.camera.PixelFormat = "Mono8"
            self.camera.ExposureTimeRaw = 1000

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

        except genicam.GenericException as e:
            # Error handling
            print("An exception occurred.", e.GetDescription())
            exitCode = 1

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
            print(f"Image saved as {filename}")
        except Exception as error:
            print(error)
            self.page.gain_entry.config(background="red")
    
    def browse(self):
        global img
        f_types = [('PNG files', '*.png')]
        filename = filedialog.askopenfilename(filetypes=f_types)
        # self.browseImg = ImageTk.PhotoImage(file=filename)
        self.browseImg = Image.open(filename)
        # img_width = img.width()
        # img_height = img.height()
        self.browseImgArray = np.asarray(self.browseImg)
        # print(self.browseImgArray)
        # self.browseImgArray = self.browseImgArray.astype(np.uint8)
        # return self.browseResultArray

    def displayToSLM(self):
        # try:
        testImg = Image.open("test.png")
        # print(type(testImg))
        # testImg = cv2.resize(testImg, dsize = (self.page.SLMdim[0], self.page.SLMdim[1]))
        # testImg.show()
        # testLabel = tk.Label(self.window, testImg)
        # self.SLMdisp = Image.fromarray(np.uint8(self.browseImgArray), "L")
        # print(type(Image.fromarray(self.browseImgArray)))
        self.SLMdisp = Image.fromarray(self.browseImgArray)
        # print(type(self.SLMdisp))
        # print(self.SLMdisp.mode)
        # self.SLMdisp = testImg
        # print(type(self.SLMdisp))
        # print(self.SLMdisp.mode)
        # print("DONE")
        # except Exception as error:
        #     print(error)
        # Image.fromarray(self.browseResultArray).show()

    def clearSLM(self):
        self.SLMdisp = Image.fromarray(np.zeros((1080,1920)))


if __name__ == "__main__":
    testWidget = cameraCapture()
    while testWidget.camera.IsGrabbing():
        #input("Press Enter to continue...")
        testWidget.getFrame()

        #If window has been closed using the X button, close program
        # getWindowProperty() returns -1 as soon as the window is closed
        if cv2.getWindowProperty(testWidget.windowName, 0) < 0:
            cv2.destroyAllWindows()
            break
        if testWidget.k == 27: #If press ESC key
            print('ESC')
            cv2.destroyAllWindows()
            break