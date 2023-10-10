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
import video_display  # remember to change this back
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

        self.SLMdisp = Image.fromarray(np.zeros((self.page.SLM_dim[0], self.page.SLM_dim[1])))
        self.browseImg = Image.open("./settings/PreSets/HAMAMATSU/HAMAMATSU_black.png")
        # self.SLMdisp = Image.open('10lpmm_190amp.png')

    def getFrame(self):
        self.img = np.array(Image.open("C:/Users/10903/OneDrive/Python/CGH_test/2D_Gaussian.png").convert('L'))
        return self.img

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
        global browseImg
        try:
            f_types = [('hurry up and pick one', '*.png')]
            filename = filedialog.askopenfilename(filetypes=f_types)
            self.browseImg = Image.open(filename)
            browseImg = self.browseImg
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
            self.page.display_button.config(background='red')

    def clearSLM(self):
        self.SLMdisp = Image.fromarray(np.zeros((self.page.SLM_dim[0], self.page.SLM_dim[1])))

    def stopGUI(self):
        # self.camera.StopGrabbing()
        # print("Stopped")
        pass

    def exitGUI(self):
        print("GOODBYE")
        df = pd.DataFrame({'exposure': [self.page.exposure_entry.get()],
                           'gain': [self.page.gain_entry.get()],
                           'loop': [self.page.loop_entry.get()]})
        df.to_csv('prevVals.csv', index=False)
        self.page.window.destroy()
        self.camera.Close

    def crosshair(self):
        self.SLMdisp = Image.open("./calibration/HAMAMATSU/crosshairNums.png")

    def testFunc(self):
        self.camera.StartGrabbing()

    def runThrough(self):
        # for pol in np.arange(0,360,10):
        #     for gray in np.arange(0, 260, 10):
        gray = 160
        # self.SLMdisp = Image.open("./HMPolTests/HAMAMATSU_"+str(gray)+".png")
        self.SLMdisp = Image.open("./calibration/HAMAMATSU/HAMAMATSU_2px_crosshair.png")
        print("Image displayed.")

        # self.page.update()
        # input("Press enter to continue....")
        # cv2.imwrite(f'./HMPolTests/testImg.png', self.img0)  # Save the captured image to a file
        # print(f"Image saved as testImg.png")

    def oneloop(self):
        self.page.loop_pressed = True

    def nloops(self):
        self.page.nloop_pressed = True

    def save_SLM(self):
        filename = self.page.save_SLM_entry.get()
        try:
            cv2.imwrite(f'{filename}.png', asarray(self.SLMdisp))  # Save the captured image to a file
            print(f"Image saved as {filename}.png")
            self.page.save_SLM_button.config(background="SystemButtonFace")
        except Exception as error:
            print(error)
            self.page.save_SLM_button.config(background="red")

    def calibrate(self):
        warp_transform = calibration(self.SLMdisp, self.getFrame())
        self.page.cal_transform = warp_transform

    def saveLineout(self):
        filename = self.page.save_lineout_entry.get()
        try:
            self.page.fig.savefig(filename)
            print(f"Image saved as {filename}.png")
            self.page.save_SLM_button.config(background="SystemButtonFace")
        except Exception as error:
            print(error)
            self.page.save_SLM_button.config(background="red")


if __name__ == "__main__":
    testWidget = cameraCapture()
    while testWidget.camera.IsGrabbing():
        # input("Press Enter to continue...")
        testWidget.getFrame()
