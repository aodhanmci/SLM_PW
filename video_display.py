import tkinter as tk
from tkinter import ttk, PhotoImage, filedialog
from tkinter.filedialog import askopenfile
from tkinter.constants import *
import oneCameraCapture
from PIL import Image, ImageTk, ImageOps
import numpy as np
import cv2
import PIL
from SLM_HAMAMATSU import *
import screeninfo
from screeninfo import get_monitors
import pandas as pd
import os
import imageio.v3 as iio
import laserbeamsize as lbs
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import time

# THIS IS A TEST!!!

class Page(tk.Frame):

    def __init__(self, parent, window):
        global onClose, scale_percent

        # self.grid()

        tk.Frame.__init__(self, parent)

        self.window = window
        window.title("SLM & CCD Control")
        # window.geometry(f"{window_width}x{window_height}")
        
        self.vid = oneCameraCapture.cameraCapture(self, self)

        # Detect SLM monitor
        global mainDim, SLMdim

        mainDisplayNum = 0
        mainDisplay = screeninfo.get_monitors()[mainDisplayNum]
        mainDim = (int(mainDisplay.width), int(mainDisplay.height))

        self.SLMdisplayNum = 1
        self.SLMdisplay = screeninfo.get_monitors()[self.SLMdisplayNum]
        self.SLMdim = (int(self.SLMdisplay.width), int(self.SLMdisplay.height))
        SLMdim = self.SLMdim

        # Define dimensions for object placement
        SLMwidth = SLMdim[0]
        SLMheight = SLMdim[1]

        CCDwidth = self.vid.getFrame().shape[1] # 1920
        CCDheight = self.vid.getFrame().shape[0] # 1200

        scale_percent = 30 # percent of original size

        gap = min(SLMwidth, CCDwidth)*scale_percent/600

        window_width = int(SLMwidth*scale_percent/100 + CCDwidth*scale_percent/100 + 3*gap)
        window_height = int(max(SLMheight, CCDheight)*scale_percent/50 + 3*gap)

        window.geometry(f"{window_width}x{window_height}+{int(mainDim[0]/2-window_width/2)}+{int(mainDim[1]/2-window_height/2-gap/2)}")

        small_button_height = 20
        small_button_width = 50
        # just leaving this here
        large_button_height = 30
        large_button_width = 60

        button_gap = 0

        width_scale = int(window_width * scale_percent / 100)
        height_scale = int(window_height * scale_percent / 100)
        first_row_button_height = window_height-2*large_button_height-2*button_gap
        second_row_button_height = window_height-large_button_height-button_gap

        upper_row_dict = {"y":first_row_button_height, "height":large_button_height, "width":large_button_width}
        lower_row_dict = {"y":second_row_button_height, "height":large_button_height, "width":large_button_width}

        df = pd.read_csv('./settings/prevVals.csv', usecols=['exposure','gain','loop'])

        # Create a label for the SLM image
        self.slm_image_label = tk.Label(window, text="SLM")
        self.slm_image_label.place(
            x = SLMwidth*scale_percent/200 + gap,
            y= gap/2,
            anchor=tk.CENTER
            )

        # Create a label for the CCD image
        self.ccd_image_label = tk.Label(window, text="CCD")
        self.ccd_image_label.place(
            x = window_width - CCDwidth*scale_percent/200 - gap,
            y= gap/2, 
            anchor=tk.CENTER
            )
        
        self.slm_preview_label = tk.Label(window, text="SLM Preview")
        self.slm_preview_label.place(
            x = SLMwidth*scale_percent/200 + gap,
            y= 3*gap/2 + max(SLMheight, CCDheight)*scale_percent/100, 
            anchor=tk.CENTER
            )
        
        self.lineout_label = tk.Label(window, text="Center Lineout")
        self.lineout_label.place(
            x = window_width - CCDwidth*scale_percent/200 - gap,
            y= 3*gap/2 + max(SLMheight, CCDheight)*scale_percent/100, 
            anchor=tk.CENTER
            )

        # Create buttons
        self.start_button = tk.Button(window, text="Start", command=self.vid.testFunc)
        self.start_button.place(x=0, **upper_row_dict)
        self.stop_button = tk.Button(window, text="Stop", command=self.vid.stopGUI)
        self.stop_button.place(x=large_button_width, **upper_row_dict)
        self.exit_button = tk.Button(window, text="Exit", command=self.vid.exitGUI)
        self.exit_button.place(x=2*large_button_width, **upper_row_dict)
        self.save_SLM_entry = tk.Entry(window)
        self.save_SLM_entry.place(x=3*large_button_width, **upper_row_dict)
        self.loop_entry = tk.Entry(window)
        self.loop_entry.insert(0, str(df.loop[0]))
        self.loop_entry.place(x=5*large_button_width, **upper_row_dict)

        self.browse_button = tk.Button(window, text="Browse", command=self.vid.browse)
        self.browse_button.place(x=0, **lower_row_dict)
        self.display_button = tk.Button(window, text="Display to SLM", command=self.vid.displayToSLM)
        self.display_button.place(x=1*large_button_width, **lower_row_dict)
        self.clear_button = tk.Button(window, text="Clear", command=self.vid.clearSLM)
        self.clear_button.place(x=2*large_button_width, **lower_row_dict)
        self.save_SLM_button = tk.Button(window, text="Save SLM", command=self.vid.save_SLM)
        self.save_SLM_button.place(x=3*large_button_width, **lower_row_dict)
        self.one_loop_button = tk.Button(window, text="1 loop", command=self.vid.oneloop)
        self.one_loop_button.place(x=4*large_button_width, **lower_row_dict)
        self.five_loop_button = tk.Button(window, text="n loop", command=self.vid.nloops)
        self.five_loop_button.place(x=5*large_button_width, **lower_row_dict)
        self.crosshair_button = tk.Button(window, text="Crosshair", command=self.vid.crosshair)
        self.crosshair_button.place(x=6*large_button_width, **lower_row_dict)
        self.calibrate_button = tk.Button(window, text="Calibrate", command=self.vid.calibrate)
        self.calibrate_button.place(x=7*large_button_width, **lower_row_dict)
        self.circle_button = tk.Button(window, text="Circle", command=lambda: circleDetection())
        self.circle_button.place(x=8*large_button_width, **lower_row_dict)
        self.lineout_button = tk.Button(window, text="Lineout", command=lambda: lineout())
        self.lineout_button.place(x=9*large_button_width, **lower_row_dict)
        self.trigger_button = tk.Button(window, text="Trigger", command=lambda: trigger())
        self.trigger_button.place(x=10*large_button_width, **lower_row_dict)

        # Create labels and entry widgets for exposure, gain, and save file
        self.exposure_button = tk.Button(window, text="Set Exposure", command=self.vid.exposure_change)
        self.exposure_button.place(x=window_width-4*large_button_width, **lower_row_dict)
        self.gain_button = tk.Button(window, text="Set Gain", command=self.vid.gain_change)
        self.gain_button.place(x=window_width-3*large_button_width, **lower_row_dict)
        self.save_button = tk.Button(window, text="Save CCD", command=self.vid.save_image)
        self.save_button.place(x=window_width-2*large_button_width, **lower_row_dict)
        self.save_lineout_button = tk.Button(window, text="Save Lineout", command=self.vid.saveLineout)
        self.save_lineout_button.place(x=window_width-large_button_width, **lower_row_dict)

        self.exposure_entry = tk.Entry(window)
        self.exposure_entry.insert(0, str(df.exposure[0]))
        self.exposure_entry.place(x=window_width-4*large_button_width, **upper_row_dict)
        self.gain_entry = tk.Entry(window)
        self.gain_entry.insert(0, str(df.gain[0]))
        self.gain_entry.place(x=window_width-3*large_button_width, **upper_row_dict)
        self.save_entry = tk.Entry(window)
        self.save_entry.place(x=window_width-2*large_button_width, **upper_row_dict)
        self.save_lineout_entry = tk.Entry(window)
        self.save_lineout_entry.place(x=window_width-large_button_width, **upper_row_dict)
        # load in the last saved image transformation object
        try:
            with open('./settings/calibration/warp_transform.pckl', 'rb') as warp_trans_file:
                self.cal_transform = pickle.load(warp_trans_file)
        except FileNotFoundError:
            print('No image transform file found. Pls calibrate.')
            self.cal_transform = 0

        #Create a canvas that will display what is on the SLM
        self.SLM_image_widget = tk.Label(window, 
                                         width=int(SLMwidth*scale_percent/100),
                                         height=int(SLMheight*scale_percent/100),
                                         anchor=tk.CENTER
                                         )
        self.SLM_image_widget.place(
                                    x = int(SLMwidth*scale_percent/200 + gap),
                                    y = int(max(SLMheight, CCDheight)*scale_percent/200 + gap),
                                    anchor=tk.CENTER
                                    )

        #Create a canvas that will show the CCD image
        self.ccd_image_widget = tk.Label(window, 
                                         width=int(CCDwidth*scale_percent/100), 
                                         height=int(CCDheight*scale_percent/100),
                                         anchor=tk.CENTER
                                         )
        self.ccd_image_widget.place(
                                    x = int(window_width - CCDwidth*scale_percent/200 - gap),
                                    y = int(max(SLMheight, CCDheight)*scale_percent/200 + gap),
                                    anchor=tk.CENTER
                                    )

        #Create a canvas that will preview the SLM image
        self.SLM_preview_widget = tk.Label(window, 
                                         width=int(SLMwidth*scale_percent/100),
                                         height=int(SLMheight*scale_percent/100),
                                         anchor=tk.CENTER
                                         )
        self.SLM_preview_widget.place(
                                    x = int(SLMwidth*scale_percent/200 + gap),
                                    y = int(max(SLMheight, CCDheight)*scale_percent*1.5/100 + 2*gap),
                                    anchor=tk.CENTER
                                    )


        global SLMimage, SLMpreview
        self.SLMimage = np.zeros((SLMdim[0], SLMdim[1]))
        self.SLMimage[0][0] = None
        SLMimage = self.SLMimage
        self.SLMpreview = SLMimage
        SLMpreview = SLMimage

        fig, ax = plt.subplots(figsize=(4.5,3.5))

        canvas = FigureCanvasTkAgg(fig, root)
        canvas.draw()
        canvas.get_tk_widget().place(
                                    x = int(window_width - CCDwidth*scale_percent/200 - gap),
                                    y = int(max(SLMheight, CCDheight)*scale_percent*1.5/100 + 2*gap),
                                    anchor=tk.CENTER
        )

        self.ax = ax
        self.canvas = canvas
        self.fig = fig

        self.circle_toggle = False
        self.lineout_toggle = False
        # self.trigger_toggle = False
        self.clearCanvas = True
        self.loop_pressed = False
        self.nloop_pressed = False
        self.count = 0
        self.timer = 0


        def circleDetection():
            if self.circle_toggle:
                self.circle_toggle = False
                self.circle_button.config(background="SystemButtonFace")
            else:
                self.circle_toggle = True
                self.circle_button.config(background="white")

        def lineout():
            if self.lineout_toggle:
                self.lineout_toggle = False
                self.lineout_button.config(background="SystemButtonFace")
            else:
                self.lineout_toggle = True
                self.lineout_button.config(background="white")

        def trigger():
            if self.vid.camera.TriggerMode.GetValue() == "On":
                try:
                    self.vid.camera.StopGrabbing()
                    self.vid.camera.TriggerMode.SetValue("Off")
                    self.vid.camera.StartGrabbing()
                    self.trigger_button.config(background="SystemButtonFace")
                    # print("TRIGGER OFF")
                except Exception as error:
                    print(error)
            else:
                try:
                    self.vid.camera.StopGrabbing()
                    self.vid.camera.TriggerMode.SetValue("On")
                    self.vid.camera.StartGrabbing()
                    self.trigger_button.config(background="white")
                    # print("TRIGGER ON")
                except Exception as error:
                    self.vid.camera.StopGrabbing()
                    self.vid.camera.TriggerMode.SetValue("Off")
                    self.vid.camera.StartGrabbing()
                    self.trigger_button.config(background="SystemButtonFace")
                    # print("TRIGGER OFF")
                    print(error)

        self.delay=3
        print("HELLO")
        self.update()
        
        onClose = self.vid.exitGUI






    def update(self):
        global SLMgrating, check, threshold, calibrate, circleDetection, saveLineout, goalArray, beginningIntensity, trigger
        SLMimage = self.SLMimage
        time1 = time.time()
        # Example arrays (you can replace these with your actual image data)
        # SLMgrating = np.random.randint(0, 256, size=(int(self.SLMdim[0]*scale_percent/100), int(self.SLMdim[1]*scale_percent/100)), dtype=np.uint8).T
        # image_array2 = np.random.randint(0, 10, size=(width_scale, height_scale), dtype=np.uint8).T
        # Convert NumPy arrays to Pillow Images
        # image1 = Image.fromarray(image_array1)
        # SLMimage = Image.fromarray(image_array2)

        # SLMgrating = np.asarray(Image.open("./calibration/crosshair4.png"))
        # SLMgrating = np.asarray(self.vid.SLMdisp)

        if self.nloop_pressed == True or self.loop_pressed == True:
            currentBeam = self.vid.getFrame()
            if self.count == 0 and self.timer == 0:
                beginningIntensity = np.sum(currentBeam[currentBeam > 1])
                # print("BEGINNING TOTAL: " + str(beginningIntensity))
            if self.loop_pressed == True:
                maxLoops = 0
            else:
                maxLoops = int(self.loop_entry.get())
            if self.timer != 5:
                # time.sleep(0.1)
                self.timer += 1
            if self.timer == 5:
                if self.count == 0:
                    gratingImg, gratingArray, goalArray, diff, threshold, allTest = feedback(
                        count = self.count,
                        # plot = True,
                        initialArray = self.vid.getFrame(),
                        image_transform=self.cal_transform,
                        SLM_height = self.SLMdim[1],
                        SLM_width = self.SLMdim[0]
                        )
                else:
                    gratingImg, gratingArray, goalArray, diff, threshold, allTest = feedback(
                        count = self.count,
                        # plot = True,
                        threshold = threshold,
                        initialArray = self.vid.getFrame(),
                        image_transform=self.cal_transform,
                        SLM_height=self.SLMdim[1],
                        SLM_width=self.SLMdim[0]
                    )

                SLMgrating = gratingArray


                if self.count == maxLoops:
                    self.count = 0
                    self.nloop_pressed = False
                    self.loop_pressed = False
                    self.vid.SLMdisp = Image.fromarray(gratingArray)
                    goalArray = None
                else:
                    self.count += 1
                self.timer = 0
                print("THROUGHPUT: " + str(np.round(np.sum(currentBeam[currentBeam > 1]/beginningIntensity*100),2)) + "%")
        else:
            SLMgrating = np.asarray(self.vid.SLMdisp)

        if len(SLMgrating.shape) == 3:
            SLMgrating = SLMgrating[:,:,0]

        SLMbrowse = np.asarray(self.vid.browseImg)

        if SLMimage[0][0] != None:
            check = np.array_equal(SLMimage, SLMgrating)
            if check != True:
                self.SLMimage = SLMgrating

                self.SLMgrating = cv2.resize(SLMgrating, dsize=(int(self.SLMdim[0]*scale_percent/100), int(self.SLMdim[1]*scale_percent/100)))
                self.SLMgrating = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.SLMgrating))
                self.SLM_image_widget.photo = self.SLMgrating
                self.SLM_image_widget.config(image=self.SLMgrating)
        
        if SLMpreview[0][0] != None:
            check2 = np.array_equal(SLMpreview, SLMbrowse)
            if check2 != True:
                self.SLMbrowse = cv2.resize(SLMbrowse, dsize=(int(self.SLMdim[0]*scale_percent/100), int(self.SLMdim[1]*scale_percent/100)))
                self.SLMbrowse = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.SLMbrowse))
                self.SLM_preview_widget.photo = self.SLMbrowse
                self.SLM_preview_widget.config(image=self.SLMbrowse)


        self.ccd_data = self.vid.getFrame() #This is an array
        self.ccd_data = cv2.resize(self.ccd_data, dsize=(int(self.vid.getFrame().shape[1]*scale_percent/100), int(self.vid.getFrame().shape[0]*scale_percent/100)), interpolation=cv2.INTER_CUBIC)


        image = self.ccd_data
        cx, cy, dx, dy, phi = lbs.beam_size(image)
        detected_circle = np.uint16((cx,cy,(dx/3+dy/3)/2,phi))

        # Live lineout plotting

        if self.lineout_toggle:
            self.clearCanvas = False
            try:
                y = self.ccd_data[int(cy),:]
                x = np.arange(len(y))


                self.ax.clear()
                self.ax.plot(x,y, color = "dimgrey")
                try:
                    goalArray = cv2.resize(goalArray, dsize=(int(self.vid.getFrame().shape[1]*scale_percent/100), int(self.vid.getFrame().shape[0]*scale_percent/100)), interpolation=cv2.INTER_CUBIC)
                    yGoal = goalArray[int(cy),:]
                    self.ax.plot(x,yGoal, color="black")
                except Exception as error:
                    # print(error)
                    pass
                self.ax.set_ylim([0,260])
                self.ax.set_xlabel("Position (x)")
                self.ax.set_ylabel("Pixel Intensity (0-255)")
                self.ax.set_title("Center Horizontal Lineout of CCD")
                self.canvas.draw()
            except Exception as error:
                print(error)
        else:
            if self.clearCanvas == False:
                self.ax.clear()
                self.canvas.draw()
                self.clearCanvas = True

        # Circle detection

        if self.circle_toggle:
            try:
                cv2.circle(image, (detected_circle[0],detected_circle[1]), detected_circle[2], 255, 1)
                cv2.circle(image, (detected_circle[0],detected_circle[1]), 1, 255, 2)
            except Exception as error:
                print(error)

        # if self.trigger_toggle:
        #     try:
        #         self.vid.camera.StopGrabbing()
        #         self.vid.camera.TriggerMode.SetValue("On")
        #         self.vid.camera.StartGrabbing()
        # else:
        #     try:
        #         self.vid.camera.StopGrabbing()
        #         self.vid.camera.TriggerMode.SetValue("Off")
        #         self.vid.camera.StartGrabbing()
        #     except Exception as error:
        #         print(error)

        # def trigger():
        #     if self.vid.camera.TriggerMode.GetValue == "On":
        #         self.vid.camera.StopGrabbing()
        #         self.vid.camera.TriggerMode.SetValue("Off")
        #         self.vid.camera.StartGrabbing()
        #         self.trigger_button.config(background="SystemButtonFace")
        #     else:
        #         self.vid.camera.StopGrabbing()
        #         self.vid.camera.TriggerMode.SetValue("On")
        #         self.vid.camera.StartGrabbing()
        #         self.trigger_button.config(background="white")

        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.ccd_data))
        self.ccd_image_widget.config(image=self.photo)
        self.ccd_image_widget.photo = self.photo

        self.window.after(self.delay, self.update)
        time2 = time.time()
        # print(time2-time1)



class window2(tk.Toplevel, Page):
    def __init__(self, parent):
        global SLMimage

        self.SLMdims = SLMdim

        # Get main display and SLM display dimensions to send window2 to SLM display
        mainWidth = mainDim[0] # 2560
        mainHeight = mainDim[1] # 1440
        SLMwidth = SLMdim[0] # 1280
        SLMheight = SLMdim[1] # 1024

        # print(mainWidth, mainHeight, SLMwidth, SLMheight)

        tk.Toplevel.__init__(self,parent)
        self.parent = parent
        self.title("SLM DISPLAY")
        self.geometry('%dx%d+%d+%d'%(SLMwidth, SLMheight, mainWidth, 0))
        self.overrideredirect(1) # Remove window borders
        self.another_widget = tk.Label(self, width = int(SLMdim[0]*3), height = int(SLMdim[1]*3))
        self.another_widget.place(x=SLMdim[0]/2, y=SLMdim[1]/2, anchor=tk.CENTER)

        self.delay=1
        self.update2()

    def update2(self):
        global SLMimage

        self.SLMdims = SLMdim

        # Only change image on SLM if the variable "SLMgrating" from oneCameraCapture (created from Upload to SLM button) is different from current display on SLM

        if SLMimage[0][0] != None:
            if check != True:
                SLMimage = SLMgrating
                SLMimage = ImageOps.fit(Image.fromarray(SLMimage), (int(self.SLMdims[0]), int(self.SLMdims[1])))
                SLMimage = np.asarray(SLMimage)
                self.SLMpreview = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(SLMimage))
                # self.SLMpreview = PIL.ImageTk.PhotoImage(image=SLMimage)
                # self.SLMpreview = SLMimage
                self.another_widget.photo = self.SLMpreview
                # self.another_widget.image = self.SLMpreview
                self.another_widget.config(image=self.SLMpreview)
                # self.another_widget.attributes("-fullscreen", True)
                # self.another_widget.pack(fill="both")

                # print("CHANGED SLM")

        self.after(self.delay, self.update2)



if __name__ == "__main__":
    root = tk.Tk()
    testWidget = Page(root, root) 

    window2 = window2(root)

    root.protocol("WM_DELETE_WINDOW", onClose)
    # root.bind('<Escape>', lambda x: onClose) # not working
    root.mainloop()

