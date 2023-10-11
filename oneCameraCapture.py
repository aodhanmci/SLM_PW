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
from slmsuite import holography as holo
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

class cameraCapture(tk.Frame):

    def __init__(self, page_instance, window2_instance):
        self.img0 = []
        self.windowName = 'SLM CCD'
        self.page = page_instance
        self.window2 = window2_instance
        # self.SLMdisp = Image.open('10lpmm_190amp.png')

        self.SLMdisp = Image.fromarray(np.zeros((self.page.SLM_dim[0], self.page.SLM_dim[1])))
        self.browseImg = Image.open("./settings/PreSets/HAMAMATSU/HAMAMATSU_black.png")
        try:
            df = pd.read_csv('./settings/prevVals.csv', usecols=['exposure', 'gain'])
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
                # print(f'{NUM_CAMERAS} cameras detected:\n')
                
                # for counter, device in enumerate(devices):
                #     print(f'{counter}) {device.GetFriendlyName()}') # return readable name
                #     print(f'{counter}) {device.GetFullName()}\n') # return unique code

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
            self.CCD_cal = cv2.warpPerspective(self.img0, self.page.cal_transform, (self.img0.shape[1], self.img0.shape[0]), flags=cv2.INTER_LINEAR)

            return self.img0
            
        # except genicam.GenericException as e:
        #     # Error handling
        #     print("An exception occurred.", e.GetDescription())
        #     exitCode = 1
        except Exception as error:
            print(error)

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
        df.to_csv('./settings/prevVals.csv', index=False)
        self.page.window.destroy()
        self.camera.Close
    
    def crosshair(self):
        self.SLMdisp = Image.open("./settings/calibration/HAMAMATSU/crosshairNums.png")
    
    def testFunc(self):
        self.camera.StartGrabbing()
    
    def runThrough(self):
        # for pol in np.arange(0,360,10):
        #     for gray in np.arange(0, 260, 10):
        gray=160
        # self.SLMdisp = Image.open("./HMPolTests/HAMAMATSU_"+str(gray)+".png")
        self.SLMdisp = Image.open("./settings/calibration/HAMAMATSU/HAMAMATSU_2px_crosshair.png")
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

    def cgh(self):
        self.cgh_window = tk.Toplevel(self.page.window)
        self.cgh_window.title("CGH Configuration")
        small_scale = 0.5
        window_height = int((self.page.monitor_dim[0] - self.page.taskbar_height) * small_scale - 45)  # 45 is the height of the window title
        window_hgap = int((self.page.monitor_dim[0] - self.page.taskbar_height) * (1 - small_scale) / 2)
        window_width = int(self.page.monitor_dim[1] * small_scale)
        window_wgap = int(self.page.monitor_dim[1] * (1 - small_scale) / 2)
        self.cgh_window.geometry(f"{window_width}x{window_height}+{window_wgap}+{window_hgap}")
        self.cgh_window.columnconfigure(0, weight=int(round(0.8 / self.page.gap_ratio)))
        self.cgh_window.columnconfigure(1, weight=1)
        self.cgh_window.columnconfigure(2, weight=int(1 / self.page.gap_ratio))
        self.cgh_window.columnconfigure(3, weight=1)
        self.cgh_window.columnconfigure(4, weight=int(1 / self.page.gap_ratio))
        self.cgh_window.columnconfigure(5, weight=1)
        self.cgh_window.rowconfigure(0, weight=1)
        self.cgh_window.rowconfigure(1, weight=int(0.8 / self.page.gap_ratio))
        self.cgh_window.rowconfigure(2, weight=1)
        self.cgh_window.rowconfigure(3, weight=int(0.2 / self.page.gap_ratio))
        self.cgh_window.rowconfigure(4, weight=1)
        self.cgh_window.grid_propagate(0)

        self.button_frame = tk.Frame(self.cgh_window)
        self.button_frame.grid(row=0, column=0, rowspan=5, sticky='nesw')
        n_button_col = 2
        for i in range(n_button_col):
            self.button_frame.columnconfigure(i, weight=1)
        n_button_row = 5
        for i in range(n_button_row):
            self.button_frame.rowconfigure(i, weight=1)
        self.button_frame.grid_propagate(0)
        self.title_label = tk.Label(self.button_frame, text='Target Type', font=('Arial, 10')).grid(row=0, column=0, columnspan=2, sticky='nesw')
        self.sigma_label = tk.Label(self.button_frame, text=u'\u03C3(0, 1)', font=('Arial, 10')).grid(row=1, column=0, sticky='nesw')
        self.A_label = tk.Label(self.button_frame, text='A(0, 1)', font=('Arial, 10')).grid(row=1, column=1, sticky='nesw')
        self.sigma_entry = tk.Entry(self.button_frame, font=('Arial, 18'), justify=tk.CENTER)
        self.sigma_entry.grid(row=2, column=0, sticky='nesw')
        self.A_entry = tk.Entry(self.button_frame, font=('Arial, 18'), justify=tk.CENTER)
        self.A_entry.grid(row=2, column=1, sticky='nesw')
        self.round_button = tk.Button(self.button_frame, text='Round', font=('Arial, 10'), command=self.round_super)
        self.round_button.grid(row=3, column=0, sticky='nesw')
        self.square_button = tk.Button(self.button_frame, text='Square', font=('Arial, 10'), command=self.square_super)
        self.square_button.grid(row=3, column=1, sticky='nesw')
        self.browse_button = tk.Button(self.button_frame, text='Browse', font=('Arial, 10'), command=self.cgh_browse)
        self.browse_button.grid(row=4, column=0, columnspan=2, sticky='nesw')

        for i in range(3):
            exec(f"gap{i} = tk.Label(self.cgh_window)")
            exec(f"gap{i}.grid(row=0, column=1 + 2 * {i}, rowspan=5, sticky='nesw')")
            exec(f"gap{i}.grid_propagate(0)")

        for j in range(2):
            exec(f"gap{j+3} = tk.Label(self.cgh_window)")
            exec(f"gap{j+3}.grid(row=2 + 2 * {j}, column=1, columnspan=5, sticky='nesw')")
            exec(f"gap{j+3}.grid_propagate(0)")

        names = ['Target', 'CGH_Preview']
        count_canvas = 0

        for i in names:
            exec(f"self.{i}_frame = tk.Frame(self.cgh_window, background='white')")
            exec(f"self.{i}_frame.grid(row=1, column=2 + 2 * count_canvas, sticky='nwse')")
            exec(f"self.{i}_frame.rowconfigure(0, weight=1)")
            exec(f"self.{i}_frame.columnconfigure(0, weight=1)")
            exec(f"self.{i}_fig = plt.figure()")
            exec(f"self.{i}_ax = self.{i}_fig.add_subplot(111)")
            exec(f"self.{i}_canvas = FigureCanvasTkAgg(self.{i}_fig, master=self.{i}_frame)")
            exec(f"self.{i}_canvas.get_tk_widget().grid()")
            exec(f"self.{i}_canvas.draw()")
            exec(f"self.{i}_label_title = tk.Label(self.cgh_window, text=i, font=('Arial, 10'))")
            exec(f"self.{i}_label_title.grid(row=0, column=2 + 2 * count_canvas, sticky='NS')")
            exec(f"self.{i}_frame.grid_propagate(0)")
            exec(f"self.{i}_label_title.grid_propagate(0)")
            count_canvas += 1

    def round_super(self):
        sigma = float(self.sigma_entry.get())
        A = float(self.A_entry.get())
        kernel_size = self.CCD_cal.shape
        x, y = np.meshgrid(np.linspace(-1, 1, kernel_size[1]), np.linspace(-1, 1, kernel_size[0]))
        gauss = np.exp(-((x ** 2 / (2.0 * sigma ** 2)) + (y ** 2 / (2.0 * sigma ** 2))) ** 5) * A
        self.Target_ax.clear()
        self.target_extent = [-int(gauss.shape[1] / 2), int(gauss.shape[1] / 2),
                           -int(gauss.shape[0] / 2), int(gauss.shape[0] / 2)]
        self.Target_ax.imshow(gauss*255, cmap='gray', vmin=0, vmax=255, extent=self.target_extent)
        self.Target_canvas.draw()

    def square_super(self):
        sigma = float(self.sigma_entry.get())
        A = float(self.A_entry.get())
        kernel_size = self.CCD_cal.shape
        x, y = np.meshgrid(np.linspace(-1, 1, kernel_size[1]), np.linspace(-1, 1, kernel_size[0]))
        gauss = np.exp(-((x ** 2 / (2.0 * sigma ** 2)) ** 5 + (y ** 2 / (2.0 * sigma ** 2)) ** 5)) * A
        self.Target_ax.clear()
        self.target_extent = [-int(gauss.shape[1] / 2), int(gauss.shape[1] / 2),
                              -int(gauss.shape[0] / 2), int(gauss.shape[0] / 2)]
        self.Target_ax.imshow(gauss*255, cmap='gray', vmin=0, vmax=255, extent=self.target_extent)
        self.Target_canvas.draw()

    def cgh_browse(self):
        try:
            f_types = [('hurry up and pick one', '*.png')]
            filename = filedialog.askopenfilename(filetypes=f_types)
            target_image = Image.open(filename).convert('L')
            target = np.array(self.target_image)
            self.Target_ax.clear()
            self.target_extent = [-int(target.shape[1] / 2), int(target.shape[1] / 2),
                                  -int(target.shape[0] / 2), int(target.shape[0] / 2)]
            self.Target_ax.imshow(target, cmap='gray', vmin=0, vmax=255, extent=self.target_extent)
            self.Target_canvas.draw()
            self.browse_button.config(background='SystemButtonFace')
        except Exception as error:
            self.browse_button.config(background='red')
            print(error)
    

if __name__ == "__main__":
    testWidget = cameraCapture()
    while testWidget.camera.IsGrabbing():
        #input("Press Enter to continue...")
        testWidget.getFrame()