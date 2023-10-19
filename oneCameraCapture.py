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
from slmsuite.holography.algorithms import Hologram
from slmsuite.holography import toolbox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

class cameraCapture(tk.Frame):

    def __init__(self, page_instance, window2_instance):
        self.img0 = []
        self.windowName = 'SLM CCD'
        self.page = page_instance
        self.target = np.zeros(self.page.SLM_dim)
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
            self.camera.TriggerSource.SetValue("Line1")
            self.camera.AcquisitionMode.SetValue("Continuous")

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
        filename = './Tests/Diode/' + filename + '.png'
        try:
            self.page.CCD_fig.savefig(filename)  # Save the captured image to a file
            print(f"Image saved as {filename}")
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
        self.camera.Close()
    
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
    
    def nloops(self):
        self.loop_df = pd.read_csv('./settings/loopVals.csv', usecols=['Threshold', 'Tolerance'])
        self.loop_window = tk.Toplevel(self.page.window)
        self.loop_window.title("Loop Configuration")
        small_scale = 0.3
        window_height = int((self.page.monitor_dim[0] - self.page.taskbar_height) * small_scale - 45)  # 45 is the height of the window title
        window_hgap = int((self.page.monitor_dim[0] - self.page.taskbar_height) * (1 - small_scale) / 2)
        window_width = int(self.page.monitor_dim[1] * small_scale)
        window_wgap = int(self.page.monitor_dim[1] * (1 - small_scale) / 2)
        self.loop_window.geometry(f"{window_width}x{window_height}+{window_wgap}+{window_hgap}")
        self.loop_window.columnconfigure(0, weight=1)
        self.loop_window.columnconfigure(1, weight=1)
        self.loop_window.rowconfigure(0, weight=1)
        self.loop_window.rowconfigure(1, weight=1)
        self.loop_window.rowconfigure(2, weight=1)
        self.loop_window.grid_propagate(False)

        self.threshold_label = tk.Label(self.loop_window, text='Threshold(0-1)', font=('Arial, 14')).grid(row=0, column=0, sticky='nesw')
        self.tolerance_label = tk.Label(self.loop_window, text='Tolerance(0-1)', font=('Arial, 14')).grid(row=0, column=1, sticky='nesw')
        self.threshold_entry = tk.Entry(self.loop_window, font=('Arial, 18'), justify=tk.CENTER)
        self.threshold_entry.insert(0, str(self.loop_df.Threshold[0]))
        self.threshold_entry.grid(row=1, column=0, sticky='nesw')
        self.tolerance_entry = tk.Entry(self.loop_window, font=('Arial, 18'), justify=tk.CENTER)
        self.tolerance_entry.insert(0, str(self.loop_df.Tolerance[0]))
        self.tolerance_entry.grid(row=1, column=1, sticky='nesw')
        self.uniform_button = tk.Button(self.loop_window, text='Uniform', font=('Arial, 14'), command=self.uniform)
        self.uniform_button.grid(row=2, column=0, sticky='nesw')
        self.gaussian_button = tk.Button(self.loop_window, text='Gaussian', font=('Arial, 14'), command=self.gaussian)
        self.gaussian_button.grid(row=2, column=1, sticky='nesw')

    def uniform(self):
        self.page.nloop_pressed = True
        self.page.gauss = False
        self.page.uniform_index = float(self.threshold_entry.get())
        self.loop_df = pd.DataFrame({'Threshold': [self.threshold_entry.get()],
                                    'Tolerance': [self.tolerance_entry.get()]})
        self.loop_df.to_csv('./settings/loopVals.csv', index=False)
        self.loop_window.destroy()

    def gaussian(self):
        self.page.nloop_pressed = True
        self.page.gauss = True
        self.page.gauss_index = float(self.tolerance_entry.get())
        self.loop_df = pd.DataFrame({'Threshold': [self.threshold_entry.get()],
                                     'Tolerance': [self.tolerance_entry.get()]})
        self.loop_df.to_csv('./settings/loopVals.csv', index=False)
        self.loop_window.destroy()

    
    def save_SLM(self):
        filename = self.page.save_SLM_entry.get()
        filename = './Tests/Diode/' + filename + '.png'
        try:
            im = Image.fromarray(self.page.SLM_array)
            im.save(filename)  # Save the captured image to a file
            print(f"Image saved as {filename}")
            self.page.save_SLM_button.config(background="SystemButtonFace")
        except Exception as error:
            print(error)
            self.page.save_SLM_button.config(background="red")

    def calibrate(self):
        warp_transform = calibration(self.SLMdisp, self.getFrame())
        self.page.cal_transform = warp_transform

    def save_CCD(self):
        filename = self.page.save_CCD_entry.get()
        filename = './Tests/Diode/' + filename + '.png'
        try:
            im = Image.fromarray(self.img0)
            im.save(filename)  # Save the captured image to a file
            print(f"Image saved as {filename}")
            self.page.save_CCD_button.config(background="SystemButtonFace")
        except Exception as error:
            print(error)
            self.page.save_CCD_button.config(background="red")

    def size_adjust(self, arr, target_shape):
        arr_h, arr_w = arr.shape
        tar_h, tar_w = target_shape[0], target_shape[1]
        if arr_h <= tar_h:
            arr = toolbox.pad(arr, (tar_h, arr_w))
        else:
            arr = arr[int((arr_h - tar_h) / 2):int((arr_h + tar_h) / 2), :]
        arr_h = arr.shape[0]
        if arr_w <= tar_w:
            arr = toolbox.pad(arr, (arr_h, tar_w))
        else:
            arr = arr[:, int((arr_w - tar_w) / 2):int((arr_w + tar_w) / 2)]

        return arr

    def cgh(self):
        self.cgh_df = pd.read_csv('./settings/cghVals.csv', usecols=['sigma', 'A', 'filepath', 'iterations'])
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
        self.cgh_window.grid_propagate(False)

        # self.form = np.zeros((self.page.SLM_dim))
        # self.form = toolbox.pad(self.form, 2 ** (np.log2(self.form.shape) + 1).astype(int))

        self.button_frame = tk.Frame(self.cgh_window)
        self.button_frame.grid(row=0, column=0, rowspan=5, sticky='nesw')
        n_button_col = 2
        for i in range(n_button_col):
            self.button_frame.columnconfigure(i, weight=1)
        n_button_row = 6
        for i in range(n_button_row):
            self.button_frame.rowconfigure(i, weight=1)
        self.button_frame.grid_propagate(0)
        self.title_label = tk.Label(self.button_frame, text='Target Type', font=('Arial, 10')).grid(row=0, column=0, columnspan=2, sticky='nesw')
        self.sigma_label = tk.Label(self.button_frame, text=u'\u03C3(0, 1)', font=('Arial, 10')).grid(row=1, column=0, sticky='nesw')
        self.A_label = tk.Label(self.button_frame, text='A(0, 1)', font=('Arial, 10')).grid(row=1, column=1, sticky='nesw')
        self.sigma_entry = tk.Entry(self.button_frame, font=('Arial, 18'), justify=tk.CENTER)
        self.sigma_entry.grid(row=2, column=0, sticky='nesw')
        self.sigma_entry.insert(0, str(self.cgh_df.sigma[0]))
        self.A_entry = tk.Entry(self.button_frame, font=('Arial, 18'), justify=tk.CENTER)
        self.A_entry.grid(row=2, column=1, sticky='nesw')
        self.A_entry.insert(0, str(self.cgh_df.A[0]))
        self.round_button = tk.Button(self.button_frame, text='Round', font=('Arial, 10'), command=self.round_super)
        self.round_button.grid(row=3, column=0, sticky='nesw')
        self.square_button = tk.Button(self.button_frame, text='Square', font=('Arial, 10'), command=self.square_super)
        self.square_button.grid(row=3, column=1, sticky='nesw')
        self.browse_entry = tk.Entry(self.button_frame, font=('Arial, 18'), justify=tk.CENTER)
        self.browse_entry.insert(0, str(self.cgh_df.filepath[0]))
        self.browse_entry.grid(row=4, column=0, sticky='nesw')
        self.browse_button = tk.Button(self.button_frame, text='Browse', font=('Arial, 10'), command=self.cgh_browse)
        self.browse_button.grid(row=4, column=1, sticky='nesw')
        self.iteration_entry = tk.Entry(self.button_frame, font=('Arial, 18'), justify=tk.CENTER)
        self.iteration_entry.insert(0, str(self.cgh_df.iterations[0]))
        self.iteration_entry.grid(row=5, column=0, sticky='nesw')
        self.iteration_label = tk.Label(self.button_frame, text='Iterations', font=('Arial, 10')).grid(row=5, column=1, sticky='nesw')

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

        self.calculate_button = tk.Button(self.cgh_window, text='Calculate', font=('Arial, 10'), command=self.calculate)
        self.calculate_button.grid(row=3, column=2, sticky='nesw')
        self.apply_button = tk.Button(self.cgh_window, text='Apply', font=('Arial, 10'), command=self.apply)
        self.apply_button.grid(row=3, column=4, sticky='nesw')

    def round_super(self):
        sigma = float(self.sigma_entry.get())
        A = float(self.A_entry.get())
        kernel_size = self.CCD_cal.shape
        x, y = np.meshgrid(np.linspace(-1, 1, kernel_size[1]), np.linspace(-1, 1, kernel_size[0]))
        gauss = np.exp(-((x ** 2 / (2.0 * sigma ** 2)) + (y ** 2 / (2.0 * sigma ** 2))) ** 5) * A
        self.target = gauss
        self.Target_ax.clear()
        self.target_extent = [-int(gauss.shape[1] / 2), int(gauss.shape[1] / 2),
                           -int(gauss.shape[0] / 2), int(gauss.shape[0] / 2)]
        self.Target_ax.imshow(gauss*255, cmap='gray', vmin=0, vmax=255, extent=self.target_extent)
        self.Target_canvas.draw()

    def square_super(self):
        sigma = float(self.sigma_entry.get())
        A = float(self.A_entry.get())
        # kernel_size = self.CCD_cal.shape
        kernel_size = (1400, 1600)
        x, y = np.meshgrid(np.linspace(-1, 1, kernel_size[1]), np.linspace(-1, 1, kernel_size[0]))
        gauss = np.exp(-((x ** 2 / (2.0 * sigma ** 2)) ** 5 + (y ** 2 / (2.0 * sigma ** 2)) ** 5)) * A
        self.target = gauss
        self.Target_ax.clear()
        self.target_extent = [-int(gauss.shape[1] / 2), int(gauss.shape[1] / 2),
                              -int(gauss.shape[0] / 2), int(gauss.shape[0] / 2)]
        self.Target_ax.imshow(gauss*255, cmap='gray', vmin=0, vmax=255, extent=self.target_extent)
        self.Target_canvas.draw()

    def cgh_browse(self):
        # filename = C:\Users\10903\OneDrive\Python\SLM_GIT\star.png
        filename = self.browse_entry.get()
        target_image = Image.open(filename).convert('L')
        target = np.array(target_image)
        target = toolbox.pad(target, self.page.SLM_dim)
        self.target = target
        self.Target_ax.clear()
        self.target_extent = [-int(target.shape[1] / 2), int(target.shape[1] / 2),
                              -int(target.shape[0] / 2), int(target.shape[0] / 2)]
        self.Target_ax.imshow(target, cmap='gray', vmin=0, vmax=255, extent=self.target_extent)
        self.Target_canvas.draw()

    def calculate(self):
        phase = np.zeros(self.page.SLM_dim)
        phase = toolbox.pad(phase, 2**(np.log2(phase.shape)+1).astype(int))
        source = Image.open('./Tests/Diode/Raw_Beam.png').convert('L')
        source = np.array(source)
        source = self.size_adjust(source, phase.shape)
        target = self.size_adjust(self.target, phase.shape)
        holo = Hologram(target=target, amp=source, phase=phase, slm_shape=target.shape)
        holo.optimize(method="WGS-Kim", maxiter=int(self.iteration_entry.get())+1)
        phase_mask = holo.extract_phase()
        self.phase_mask = phase_mask / 2 / np.pi * 255
        self.CGH_Preview_ax.imshow(self.phase_mask, cmap='gray', vmin=0, vmax=255)
        self.CGH_Preview_canvas.draw()

    def apply(self):
        self.SLMdisp = self.phase_mask
        self.cgh_df = pd.DataFrame({'sigma': [self.sigma_entry.get()],
                               'A': [self.A_entry.get()],
                               'filepath': [self.browse_entry.get()],
                               'iterations': [self.iteration_entry.get()]})
        self.cgh_df.to_csv('./settings/cghVals.csv', index=False)
        self.cgh_window.destroy()
    

if __name__ == "__main__":
    testWidget = cameraCapture()
    while testWidget.camera.IsGrabbing():
        #input("Press Enter to continue...")
        testWidget.getFrame()