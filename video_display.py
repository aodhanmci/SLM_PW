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

small_button_height = 20
small_button_width = 50

large_button_height = 30
large_button_width = 90

button_gap = 0

window_width = 1500
window_height = 1000

scale_percent = 40 # percent of original size
width_scale = int(window_width * scale_percent / 100)
height_scale = int(window_height * scale_percent / 100)
# dim = (width_scale, height_scale)
first_row_button_height = window_height-2*large_button_height-2*button_gap
second_row_button_height = window_height-large_button_height-button_gap

upper_row_dict = {"y":first_row_button_height, "height":large_button_height, "width":large_button_width}
lower_row_dict = {"y":second_row_button_height, "height":large_button_height, "width":large_button_width}

class Page(tk.Frame):

    def __init__(self, parent, window):
        global onClose

        # self.grid()

        tk.Frame.__init__(self, parent)

        self.window = window
        window.title("SLM & CCD Control")
        window.geometry(f"{window_width}x{window_height}")

        df = pd.read_csv('prevVals.csv', usecols=['exposure','gain'])
        
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

        # Move SLM monitor to second screen
        # cv2.namedWindow('SLM', cv2.WINDOW_NORMAL)
        # cv2.moveWindow('SLM', self.SLMdisplay.x - 1, self.SLMdisplay.y - 1)
        # cv2.setWindowProperty('SLM', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        # print(self.SLMdim)     # width = 1280, height = 1024

        # Define dimensions for object placement
        SLMwidth = SLMdim[0]
        SLMheight = SLMdim[1]

        CCDwidth = self.vid.getFrame().shape[1] # 1920
        CCDheight = self.vid.getFrame().shape[0] # 1200

        gap = (window_width - SLMwidth*scale_percent/100 - CCDwidth*scale_percent/100) / 3


        # Create a label for the SLM image
        self.slm_image_label = tk.Label(window, text="SLM")
        self.slm_image_label.place(
            # x=0.25*window_width, 
            x = SLMwidth*scale_percent/200 + gap,
            y= gap/2,
            anchor=tk.CENTER
            )

        # UNNEEDED?
        # self.slm_image_window = tk.Canvas(window, width = 100, height=100)
        # self.slm_image_window.config(background='red')
        # self.slm_image_window.pack()

        # slm_image_window.create_image(0, 0, image = np.ones((100, 100)))

        # Create a label for the CCD image
        self.ccd_image_label = tk.Label(window, text="CCD")
        self.ccd_image_label.place(
            # x=0.75*window_width, 
            x = window_width - CCDwidth*scale_percent/200 - gap,
            y= gap/2, 
            anchor=tk.CENTER
            )

        # Create buttons
        self.start_button = tk.Button(window, text="Start", command=self.vid.testFunc)
        self.start_button.place(x=0, **upper_row_dict)
        self.stop_button = tk.Button(window, text="Stop", command=self.vid.stopGUI)
        self.stop_button.place(x=large_button_width, **upper_row_dict)
        self.exit_button = tk.Button(window, text="Exit", command=self.vid.exitGUI)
        self.exit_button.place(x=2*large_button_width, **upper_row_dict)

        self.browse_button = tk.Button(window, text="Browse", command=self.vid.browse)
        self.browse_button.place(x=0, **lower_row_dict)
        self.display_button = tk.Button(window, text="Display to SLM", command=self.vid.displayToSLM)
        self.display_button.place(x=1*large_button_width, **lower_row_dict)
        self.one_loop_button = tk.Button(window, text="1 loop", command=self.vid.oneloop)
        self.one_loop_button.place(x=2*large_button_width, **lower_row_dict)
        self.five_loop_button = tk.Button(window, text="5 loop", command=self.vid.nloops)
        self.five_loop_button.place(x=3*large_button_width, **lower_row_dict)
        self.clear_button = tk.Button(window, text="Clear", command=self.vid.clearSLM)
        self.clear_button.place(x=4*large_button_width, **lower_row_dict)
        self.crosshair_button = tk.Button(window, text="Crosshair", command=self.vid.crosshair)
        self.crosshair_button.place(x=5*large_button_width, **lower_row_dict)
        self.calibrate_button = tk.Button(window, text="Calibrate", command=lambda: calibrate())
        self.calibrate_button.place(x=6*large_button_width, **lower_row_dict)

        # Create labels and entry widgets for exposure, gain, and save file
        self.exposure_button = tk.Button(window, text="Set Exposure", command=self.vid.exposure_change)
        self.exposure_button.place(x=window_width-3*large_button_width, **lower_row_dict)
        self.gain_button = tk.Button(window, text="Set Gain", command=self.vid.gain_change)
        self.gain_button.place(x=window_width-2*large_button_width, **lower_row_dict)
        self.save_button = tk.Button(window, text="Save File", command=self.vid.save_image)
        self.save_button.place(x=window_width-large_button_width, **lower_row_dict)

        self.exposure_entry = tk.Entry(window)
        self.exposure_entry.insert(0, str(df.exposure[0]))
        self.exposure_entry.place(x=window_width-3*large_button_width, **upper_row_dict)
        self.gain_entry = tk.Entry(window)
        self.gain_entry.insert(0, str(df.gain[0]))
        self.gain_entry.place(x=window_width-2*large_button_width, **upper_row_dict)
        self.save_entry = tk.Entry(window)
        self.save_entry.place(x=window_width-1*large_button_width, **upper_row_dict)
        


        #Create a canvas that will fit the camera source
        self.SLM_image_widget = tk.Label(window, 
                                         width=int(self.SLMdim[0]*scale_percent/100),
                                         height=int(self.SLMdim[1]*scale_percent/100),
                                         anchor=tk.CENTER
                                         )
        # self.SLM_image_widget.config(background='orange')
        self.SLM_image_widget.place(
                                    # x=1*window_width/3,
                                    x = int(SLMwidth*scale_percent/200 + gap),
                                    # y=window_height/2, 
                                    y = int(SLMheight*scale_percent/200 + gap),
                                    anchor=tk.CENTER
                                    )

        # self.ccd_image_widget = tk.Label(window, width=width_scale, height=height_scale)
        self.ccd_image_widget = tk.Label(window, 
                                         width=int(self.vid.getFrame().shape[1]*scale_percent/100), 
                                         height=int(self.vid.getFrame().shape[0]*scale_percent/100),
                                         anchor=tk.CENTER
                                         )
        self.ccd_image_widget.place(
                                    # x=2*window_width/3, 
                                    x = int(window_width - CCDwidth*scale_percent/200 - gap),
                                    # y=window_height/2, 
                                    y = int(SLMheight*scale_percent/200 + gap),
                                    anchor=tk.CENTER
                                    )

        # # Create a canvas for the SLM upload preview
        # self.preview_widget = tk.Label(window, 
        #                                  width=int(self.SLMdim[0]*scale_percent/500),
        #                                  height=int(self.SLMdim[1]*scale_percent/500),
        #                                  anchor=tk.CENTER
        #                                  )
        # self.preview_widget.config(background='red')
        # self.preview_widget.place(
        #                             # x=1*window_width/3,
        #                             x = int(SLMwidth*scale_percent/200 + gap),
        #                             # y=window_height/2, 
        #                             y = int(window_height - 2*large_button_height - SLMheight*scale_percent/200 - gap),
        #                             anchor=tk.CENTER
        #                             )


        global image2
        self.image2 = np.zeros((SLMdim[0], SLMdim[1]))
        self.image2[0][0] = None
        image2 = self.image2

        self.pressed = False
        self.count = 0
        self.timer = 0

        self.delay=10
        print("HELLO")
        self.update()
        
        onClose = self.vid.exitGUI






    def update(self):
        #Get a frame from cameraCapture
        global photo1, check, threshold, calibrate
        image2 = self.image2
        # Example arrays (you can replace these with your actual image data)
        # photo1 = np.random.randint(0, 256, size=(int(self.SLMdim[0]*scale_percent/100), int(self.SLMdim[1]*scale_percent/100)), dtype=np.uint8).T
        # image_array2 = np.random.randint(0, 10, size=(width_scale, height_scale), dtype=np.uint8).T
        # Convert NumPy arrays to Pillow Images
        # image1 = Image.fromarray(image_array1)
        # image2 = Image.fromarray(image_array2)

        # photo1 = np.asarray(Image.open("./calibration/crosshair4.png"))
        # photo1 = np.asarray(self.vid.SLMdisp)

        def calibrate():
            match = False
            while match == False:

                print("\nPlease enter the following calibration values. Type \"Done\" if done.")
                xZoom = input("Enter xZoom: ")
                if xZoom == "Done":
                    try:
                        df = pd.DataFrame({'xZoom': [prevxZoom],
                                            'yZoom': [yZoom],
                                            'xShift': [xShift],
                                            'yShift': [yShift],
                                            'angle': [angle]})
                        df.to_csv('calVals.csv', index=False)
                        print("DONE CALIBRATING!")
                    except:
                        print("Failed to save values. Ending calibration.")
                        pass
                    match = True
                else:
                    yZoom = input("Enter yZoom: ")
                    xShift = input("Enter xShift: ")
                    yShift = input("Enter yShift: ")
                    angle = input("Enter angle: ")
                    prevxZoom = xZoom

                    calImg = calibration(self.vid.getFrame(), float(xZoom), float(yZoom), float(xShift), float(yShift), float(angle))
                    calImg = Image.fromarray(calImg)
                    calImg.show()
                    Image.open("./calibration/HAMAMATSU/HAMAMATSU_2px_crosshair.png").show()



        maxLoops = 10
        if self.pressed == True:
            # print("1 LOOP BUTTON PRESSED")
            if self.timer != 10:
                # time.sleep(1)
                self.timer += 1
            if self.timer == 10:
                if self.count == 0:
                    gratingImg, gratingArray, diff, threshold, allTest = feedback(
                        count = self.count,
                        # plot = True,
                        initialArray = self.vid.getFrame()
                        )
                else:
                    gratingImg, gratingArray, diff, threshold, allTest = feedback(
                        count = self.count,
                        # plot = True,
                        threshold = threshold,
                        initialArray = self.vid.getFrame()
                    )

                photo1 = gratingArray

                if self.count == maxLoops:
                    self.count = 0
                    self.pressed = False
                    self.vid.SLMdisp = Image.fromarray(gratingArray)
                else:
                    self.count += 1
                self.timer = 0
        else:
            photo1 = np.asarray(self.vid.SLMdisp)
        # print(image2)

        if len(photo1.shape) == 3:
            photo1 = photo1[:,:,0]
        # print(image2.shape)
        # print(photo1.shape)

        if image2[0][0] != None:
            check = np.array_equal(image2, photo1)
            if check != True:
                self.image2 = photo1

                self.photo1 = cv2.resize(photo1, dsize=(int(self.SLMdim[0]*scale_percent/100), int(self.SLMdim[1]*scale_percent/100)))
                self.photo1 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.photo1))
                self.SLM_image_widget.photo = self.photo1
                self.SLM_image_widget.config(image=self.photo1)
                # print("CHANGED SLM PREVIEW")

        # photo2 = PIL.ImageTk.PhotoImage(image=image2)
        # self.ccd_image_widget.photo = photo2
        # self.ccd_image_widget.config(image=photo2)

        self.ccd_data = self.vid.getFrame() #This is an array
        self.ccd_data = cv2.resize(self.ccd_data, dsize=(int(self.vid.getFrame().shape[1]*scale_percent/100), int(self.vid.getFrame().shape[0]*scale_percent/100)), interpolation=cv2.INTER_CUBIC)
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.ccd_data))
        self.ccd_image_widget.config(image=self.photo)
        self.ccd_image_widget.photo = self.photo
        # print("CHANGED CCD")

        self.window.after(self.delay, self.update)


        # label = tk.Label(self.window2)
        # photo2 = PIL.ImageTk.PhotoImage(image=self.vid.SLMdisp)
        # label.photo = photo2
        # label.config(image=photo2)
        # self.window2.mainloop()



class window2(tk.Toplevel, Page):
    def __init__(self, parent):
        global image2

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
        self.overrideredirect(1)
        # self.attributes("-fullscreen", True)
        self.another_widget = tk.Label(self, width = int(SLMdim[0]*3), height = int(SLMdim[1]*3))
        self.another_widget.place(x=SLMdim[0]/2, y=SLMdim[1]/2, anchor=tk.CENTER)

        # self.image2 = np.zeros((SLMdim[0], SLMdim[1]))
        # self.image2[0][0] = None
        # image2 = self.image2

        self.delay=1
        self.update2()

    def update2(self):
        global image2

        self.SLMdims = SLMdim

        # Only change image on SLM if the variable "photo1" from oneCameraCapture (created from Upload to SLM button) is different from current display on SLM

        if image2[0][0] != None:
            if check != True:
                image2 = photo1
                image2 = ImageOps.fit(Image.fromarray(image2), (int(self.SLMdims[0]), int(self.SLMdims[1])))
                image2 = np.asarray(image2)
                self.image3 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image2))
                # self.image3 = PIL.ImageTk.PhotoImage(image=image2)
                # self.image3 = image2
                self.another_widget.photo = self.image3
                # self.another_widget.image = self.image3
                self.another_widget.config(image=self.image3)
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

