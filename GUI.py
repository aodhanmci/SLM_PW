import tkinter as tk
from tkinter.constants import *
import Camera
from PIL import Image, ImageOps
import numpy as np
import cv2
import PIL
from SLM_HAMAMATSU import *
import screeninfo
import pandas as pd
import laserbeamsize as lbs
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
from tkinter import ttk, PhotoImage, filedialog
# THIS IS A TEST!!!

class Page(tk.Frame):

    def __init__(self, parent, window, camera, Monitors, SLM):

        tk.Frame.__init__(self, parent)

        self.window = window
        self.SLM = SLM
        window.title("SLM & CCD Control")
        # window.geometry(f"{window_width}x{window_height}")
        self.camera=camera
        self.Monitors = Monitors


        # CCDwidth = camera.getFrame().shape[1] # 1920
        # CCDheight = camera.getFrame().shape[0] # 1200
        CCDwidth=1920
        CCDheight=1200

        scale_percent = 30 # percent of original size
        self.scale_percent = scale_percent
        gap = min(self.Monitors.SLMwidth, CCDwidth)*scale_percent/600

        window_width = int(self.Monitors.SLMwidth*scale_percent/100 + CCDwidth*scale_percent/100 + 3*gap)
        window_height = int(max(self.Monitors.SLMheight, CCDheight)*scale_percent/50 + 3*gap)

        window.geometry(f"{window_width}x{window_height}+{int(self.Monitors.mainDim[0]/2-window_width/2)}+{int(self.Monitors.mainDim[1]/2-window_height/2-gap/2)}")

        # just leaving this here
        large_button_height = 30
        large_button_width = 60

        button_gap = 0

        first_row_button_height = window_height-2*large_button_height-2*button_gap
        second_row_button_height = window_height-large_button_height-button_gap

        upper_row_dict = {"y":first_row_button_height, "height":large_button_height, "width":large_button_width}
        lower_row_dict = {"y":second_row_button_height, "height":large_button_height, "width":large_button_width}

        df = pd.read_csv('./settings/prevVals.csv', usecols=['exposure','gain','loop'])
        self.ccd_data = None
        # Create a label for the SLM image
        self.slm_image_label = tk.Label(window, text="SLM")
        self.slm_image_label.place(
            x = self.Monitors.SLMwidth*scale_percent/200 + gap,
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
            x = self.Monitors.SLMwidth*scale_percent/200 + gap,
            y= 3*gap/2 + max(self.Monitors.SLMheight, CCDheight)*scale_percent/100, 
            anchor=tk.CENTER
            )
        
        self.lineout_label = tk.Label(window, text="Center Lineout")
        self.lineout_label.place(
            x = window_width - CCDwidth*scale_percent/200 - gap,
            y= 3*gap/2 + max(self.Monitors.SLMheight, CCDheight)*scale_percent/100, 
            anchor=tk.CENTER
            )


        # Create buttons
        self.start_button = tk.Button(window, text="Start", command=camera.testFunc)
        self.start_button.place(x=0, **upper_row_dict)
        self.stop_button = tk.Button(window, text="Stop", command=self.stopGUI)
        self.stop_button.place(x=large_button_width, **upper_row_dict)
        self.exit_button = tk.Button(window, text="Exit", command=self.exitGUI)
        self.exit_button.place(x=2*large_button_width, **upper_row_dict)
        self.save_SLM_entry = tk.Entry(window)
        self.save_SLM_entry.place(x=3*large_button_width, **upper_row_dict)
        self.loop_entry = tk.Entry(window)
        self.loop_entry.insert(0, str(df.loop[0]))
        self.loop_entry.place(x=5*large_button_width, **upper_row_dict)

        self.browse_button = tk.Button(window, text="Browse", command=self.SLM.browse)
        self.browse_button.place(x=0, **lower_row_dict)
        self.display_button = tk.Button(window, text="Display to SLM", command=SLM.displayToSLM)
        self.display_button.place(x=1*large_button_width, **lower_row_dict)
        self.clear_button = tk.Button(window, text="Clear", command=SLM.clearSLM)
        self.clear_button.place(x=2*large_button_width, **lower_row_dict)
        self.save_SLM_button = tk.Button(window, text="Save SLM", command=self.save_SLM)
        self.save_SLM_button.place(x=3*large_button_width, **lower_row_dict)
        self.one_loop_button = tk.Button(window, text="1 loop", command=self.oneloop)
        self.one_loop_button.place(x=4*large_button_width, **lower_row_dict)
        self.five_loop_button = tk.Button(window, text="n loop", command=self.nloops)
        self.five_loop_button.place(x=5*large_button_width, **lower_row_dict)
        self.crosshair_button = tk.Button(window, text="Crosshair", command=camera.crosshair)
        self.crosshair_button.place(x=6*large_button_width, **lower_row_dict)
        self.calibrate_button = tk.Button(window, text="Calibrate", command=camera.calibrate)
        self.calibrate_button.place(x=7*large_button_width, **lower_row_dict)
        self.circle_button = tk.Button(window, text="Circle", command=self.circleDetection)
        self.circle_button.place(x=8*large_button_width, **lower_row_dict)
        self.lineout_toggle=False
        self.lineout_button = tk.Button(window, text="Lineout", command= self.lineout)
        self.lineout_button.place(x=9*large_button_width, **lower_row_dict)
        self.trigger_button = tk.Button(window, text="Trigger", command=self.trigger)
        self.trigger_button.place(x=10*large_button_width, **lower_row_dict)
        self.wf_button = tk.Button(window, text="WF", command=self.wf)
        self.wf_button.place(x=11*large_button_width, **lower_row_dict)

        # Create labels and entry widgets for exposure, gain, and save file
        self.exposure_button = tk.Button(window, text="Set Exposure", command=self.exposure_change)
        self.exposure_button.place(x=window_width-4*large_button_width, **lower_row_dict)
        self.gain_button = tk.Button(window, text="Set Gain", command=self.gain_change)
        self.gain_button.place(x=window_width-3*large_button_width, **lower_row_dict)
        self.save_button = tk.Button(window, text="Save CCD", command=self.save_image)
        self.save_button.place(x=window_width-2*large_button_width, **lower_row_dict)
        self.save_lineout_button = tk.Button(window, text="Save Lineout", command=self.saveLineout)
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
                                         width=int(self.Monitors.SLMwidth*scale_percent/100),
                                         height=int(self.Monitors.SLMheight*scale_percent/100),
                                         anchor=tk.CENTER
                                         )
        self.SLM_image_widget.place(
                                    x = int(self.Monitors.SLMwidth*scale_percent/200 + gap),
                                    y = int(max(self.Monitors.SLMheight, CCDheight)*scale_percent/200 + gap),
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
                                    y = int(max(self.Monitors.SLMheight, CCDheight)*scale_percent/200 + gap),
                                    anchor=tk.CENTER
                                    )

        #Create a canvas that will preview the SLM image
        self.SLM_preview_widget = tk.Label(window, 
                                         width=int(self.Monitors.SLMwidth*scale_percent/100),
                                         height=int(self.Monitors.SLMheight*scale_percent/100),
                                         anchor=tk.CENTER
                                         )
        self.SLM_preview_widget.place(
                                    x = int(self.Monitors.SLMwidth*scale_percent/200 + gap),
                                    y = int(max(self.Monitors.SLMheight, CCDheight)*scale_percent*1.5/100 + 2*gap),
                                    anchor=tk.CENTER
                                    )


        fig, ax = plt.subplots(figsize=(4.5,3.5))

        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().place(
                                    x = int(window_width - CCDwidth*scale_percent/200 - gap),
                                    y = int(max(self.Monitors.SLMheight, CCDheight)*scale_percent*1.5/100 + 2*gap),
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
        self.clearSLM = False
        self.count = 0
        self.timer = 0

        self.delay=1
        print("HELLO")
        self.after(self.delay, self.update)
        ## end of initialisation ##

    def gain_change(self):
        try:
            self.camera.Set_Gain(int(self.gain_entry.get()))
            self.gain_entry.config(background="white")
        except Exception as error:
            print(error)
            self.gain_entry.config(background="red")

    def exposure_change(self):
        try:
            self.camera.Set_Exposure(int(self.exposure_entry.get()))
            self.exposure_entry.config(background="white")
        except Exception as error:
            print(error)
            self.exposure_entry.config(background="red")

    def oneloop(self):
        self.loop_pressed = True
    
    def nloops(self):
        self.nloop_pressed = True
    
    def save_SLM(self):
        filename = self.save_SLM_entry.get()
        try:
            cv2.imwrite(f'./data/{filename}.png', asarray(self.SLM.SLMdisp))  # Save the captured image to a file
            print(f"Image saved as /data/{filename}.png")
            self.save_SLM_button.config(background="SystemButtonFace")
        except Exception as error:
            print(error)
            self.save_SLM_button.config(background="red")

    def save_image(self):
        filename = self.save_entry.get()
        try:
            cv2.imwrite(f'{filename}.png', self.ccd_data)  # Save the captured image to a file
            print(f"Image saved as {filename}.png")
            self.save_button.config(background="SystemButtonFace")

        except Exception as error:
            print(error)
            self.save_button.config(background="red")
    
    def saveLineout(self):
        filename = self.save_lineout_entry.get()
        try:
            self.fig.savefig(f"./data/{filename}")
            print(f"Image saved as /data/{filename}.png")
            self.save_SLM_button.config(background="SystemButtonFace")
        except Exception as error:
            print(error)
            self.save_SLM_button.config(background="red")

    def circleDetection(self):
        if self.circle_toggle:
            self.circle_toggle = False
            self.circle_button.config(background="SystemButtonFace")
        else:
            self.circle_toggle = True
            self.circle_button.config(background="white")

    def lineout(self):
        if self.lineout_toggle:
            self.lineout_toggle = False
            self.lineout_button.config(background="SystemButtonFace")
        else:
            self.lineout_toggle = True
            self.lineout_button.config(background="white")


    def trigger(self):
        self.camera.Set_Trigger()
        

    def stopGUI(self):
        self.camera.StopGrabbing()
        print("Stopped")
        pass

    def exitGUI(self):
        print("GOODBYE")
        df = pd.DataFrame({'exposure': [self.exposure_entry.get()],
                           'gain': [self.gain_entry.get()],
                           'loop': [self.loop_entry.get()]})
        df.to_csv('./settings/prevVals.csv', index=False)
        self.window.destroy()
        self.camera.Close


    def wf(self):
            # gratingArray = Image.fromarray(gratingArray).show()

            # totalMultArray[xi,yi] = totalMultArray[xi,yi] + yshift
        # yshiftArray = np.ones(shape=gratingArray.shape)  # Initialize yshift array
            # print(yshiftArray[0][0])
            # yshiftArray = yshiftArray * 70
            # print(yshiftArray[0][0])
            # yshiftArray = yshiftArray
            # print(yshiftArray[0][0])

            # yshiftArray[xi,yi] = totalMultArray[xi,yi]     # Shift grating arary proportional to the local value of the grating array. Creates yshift the same shape as the grating
            # yshiftArray[xi,yi] = 70 - totalMultArray[xi,yi] * 2     # Shift entire grating upward, and antiproportional to shape of grating. With some tweaking, this creates a final grating which has a flat top (all values match at top) and the yshift mirrors that
            # yshiftArray[xi,yi] = 50     # Constant yshift ONLY IN THE THRESHOLD AREA. Gaussian blur below ensures smooth transition back to zero outside the threshold area.
            # yshiftArray[xi,yi] = 70 - (totalMultArray[xi,yi] **2) / 100     # Squaring totalMultArray accounts LESS for the shape of totalMultArray. Just testing other ways to make different yshift shapes.

        yshiftArray = gaussian_filter(yshiftArray,
                                          sigma=15)  # Smooth transition from yshift to zero. Testing shows ideal sigma value of 15.
            # totalMultArray = totalMultArray + yshiftArray     # Directly add yshift to previous grating
        totalMultArray = totalMultArray


    def update(self):
        # global SLMgrating, check, threshold, calibrate, circleDetection, saveLineout, goalArray, beginningIntensity, trigger, gratingArray
        SLMimage = self.SLM.SLMimage
        time1 = time.time()
        # Example arrays (you can replace these with your actual image data)
        # SLMgrating = np.random.randint(0, 256, size=(int(self.SLMdim[0]*scale_percent/100), int(self.SLMdim[1]*scale_percent/100)), dtype=np.uint8).T
        # image_array2 = np.random.randint(0, 10, size=(width_scale, height_scale), dtype=np.uint8).T
        # Convert NumPy arrays to Pillow Images
        # image1 = Image.fromarray(image_array1)
        # SLMimage = Image.fromarray(image_array2)

        # SLMgrating = np.asarray(Image.open("./calibration/crosshair4.png"))
        # SLMgrating = np.asarray(camera.SLMdisp)

        if self.nloop_pressed == True or self.loop_pressed == True:
            currentBeam = self.camera.getFrame()
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
                        initialArray = self.camera.getFrame(),
                        image_transform=self.cal_transform,
                        SLM_height = self.SLMdim[1],
                        SLM_width = self.SLMdim[0]
                    )
                if self.count == maxLoops:
                    gratingImg, gratingArray, goalArray, diff, threshold, allTest = feedback(
                        count = self.count,
                        lastloop = True,
                        # plot = True,
                        threshold = threshold,
                        initialArray = self.camera.getFrame(),
                        image_transform=self.cal_transform,
                        SLM_height=self.SLMdim[1],
                        SLM_width=self.SLMdim[0]
                    )
                else:
                    gratingImg, gratingArray, goalArray, diff, threshold, allTest = feedback(
                        count = self.count,
                        # plot = True,
                        threshold = threshold,
                        initialArray = self.camera.getFrame(),
                        image_transform=self.cal_transform,
                        SLM_height=self.SLMdim[1],
                        SLM_width=self.SLMdim[0]
                    )

                SLMgrating = gratingArray


                if self.count == maxLoops:
                    self.count = 0
                    self.nloop_pressed = False
                    self.loop_pressed = False
                    self.camera.SLMdisp = Image.fromarray(gratingArray)
                    goalArray = None
                else:
                    self.count += 1
                self.timer = 0
                print("THROUGHPUT: " + str(np.round(np.sum(currentBeam[currentBeam > 1]/beginningIntensity*100),2)) + "%")
        else:
            SLMgrating = np.asarray(self.SLM.SLMdisp)

        if len(SLMgrating.shape) == 3:
            SLMgrating = SLMgrating[:,:,0]

        SLMbrowse = np.asarray(self.SLM.browseImg)

        if SLMimage[0][0] != None:
            check = np.array_equal(SLMimage, SLMgrating)
            if check != True:
                self.SLM.SLMimage = SLMgrating

                self.SLMgrating = cv2.resize(SLMgrating, dsize=(int(self.Monitors.SLMdim[0]*self.scale_percent/100), int(self.Monitors.SLMdim[1]*self.scale_percent/100)))
                self.SLMgrating = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.SLMgrating))
                self.SLM_image_widget.photo = self.SLMgrating
                self.SLM_image_widget.config(image=self.SLMgrating)
        
        if self.SLM.SLMpreview[0][0] != None:
            check2 = np.array_equal(self.SLM.SLMpreview, SLMbrowse)
            if check2 != True:
                self.SLMbrowse = cv2.resize(SLMbrowse, dsize=(int(self.Monitors.SLMdim[0]*self.scale_percent/100), int(self.Monitors.SLMdim[1]*self.scale_percent/100)))
                self.SLMbrowse = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.SLMbrowse))
                self.SLM_preview_widget.photo = self.SLMbrowse
                self.SLM_preview_widget.config(image=self.SLMbrowse)

        with self.camera.lock:
            self.ccd_data = self.camera.getFrame()  # Access the shared frame in a thread-safe manner
        # self.ccd_data = self.camera.getFrame() #This is an array
        self.ccd_data = cv2.resize(self.ccd_data, dsize=(int(self.ccd_data.shape[1]*self.scale_percent/100), int(self.ccd_data.shape[0]*self.scale_percent/100)), interpolation=cv2.INTER_CUBIC)


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
                    if np.amax(self.SLM.SLMimage) != 0.0:
                        gratingArrayRescaled = cv2.resize(gratingArray, dsize=(int(self.ccd_data.shape[1]*self.scale_percent/100), int(self.ccd_data.shape[0]*self.scale_percent/100)), interpolation=cv2.INTER_CUBIC)
                        SLMrescaledwidth, SLMrescaledheight = gratingArrayRescaled.shape
                        ySLM = gratingArrayRescaled[int(SLMrescaledwidth/2),:]
                        # ySLM = gratingArray[int(self.SLMheight/2),:]
                        self.ax.plot(x,ySLM, color="red")
                    else:
                        # if self.clearCanvas != False:
                        self.clearCanvas = False

                except Exception as error:
                    # print(error)
                    pass

                try:
                    goalArray = cv2.resize(goalArray, dsize=(int(self.ccd_data.shape[1]*self.scale_percent/100), int(self.ccd_data.shape[0]*self.scale_percent/100)), interpolation=cv2.INTER_CUBIC)
                    yGoal = goalArray[int(cy),:]
                    self.ax.plot(x,yGoal, color="black")
                except Exception as error:
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
                # print("CLEAR")
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
        #         camera.camera.StopGrabbing()
        #         camera.camera.TriggerMode.SetValue("On")
        #         camera.camera.StartGrabbing()
        # else:
        #     try:
        #         camera.camera.StopGrabbing()
        #         camera.camera.TriggerMode.SetValue("Off")
        #         camera.camera.StartGrabbing()
        #     except Exception as error:
        #         print(error)

        # def trigger():
        #     if camera.camera.TriggerMode.GetValue == "On":
        #         camera.camera.StopGrabbing()
        #         camera.camera.TriggerMode.SetValue("Off")
        #         camera.camera.StartGrabbing()
        #         self.trigger_button.config(background="SystemButtonFace")
        #     else:
        #         camera.camera.StopGrabbing()
        #         camera.camera.TriggerMode.SetValue("On")
        #         camera.camera.StartGrabbing()
        #         self.trigger_button.config(background="white")

        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.ccd_data))
        self.ccd_image_widget.config(image=self.photo)
        self.ccd_image_widget.photo = self.photo

        self.window.after(self.delay, self.update)
        time2 = time.time()
        # print(time2-time1)






