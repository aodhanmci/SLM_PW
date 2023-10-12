import tkinter as tk
import matplotlib.pyplot as plt
import oneCameraCapture
import SLM_HAMAMATSU
import numpy as np
import screeninfo
import ctypes
import pandas as pd
from PIL import Image, ImageTk
import laserbeamsize as lbs
import time
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pickle

class Page(tk.Frame):

    def __init__(self, parent, window):
        global onClose, SLM_dim, monitor_dim

        tk.Frame.__init__(self, parent)

        self.window = window
        window.title("SLM & CCD Control")

        self.SLM_num = 1
        self.SLM_info = screeninfo.get_monitors()[self.SLM_num]
        self.SLM_dim = (int(self.SLM_info.height), int(self.SLM_info.width))

        self.vid = oneCameraCapture.cameraCapture(self, self)
        df = pd.read_csv('./settings/prevVals.csv', usecols=['exposure', 'gain', 'loop'])

        try:
            with open('./settings/calibration/warp_transform.pckl', 'rb') as warp_trans_file:
                self.cal_transform = pickle.load(warp_trans_file)
        except FileNotFoundError:
            print('No image transform file found. Pls calibrate.')
            self.cal_transform = 0

        # Get dimensions of user monitor, SLM, and CCD
        self.monitor_num = 0
        self.monitor_info = screeninfo.get_monitors()[self.monitor_num]
        self.monitor_dim = (int(self.monitor_info.height), int(self.monitor_info.width))
        self.monitor_scale = ctypes.windll.shcore.GetScaleFactorForDevice(self.monitor_num) / 100  # scaling of the primary monitor
        self.Preview_dim = self.SLM_dim
        self.CCD_dim = (int(self.vid.getFrame().shape[0]), int(self.vid.getFrame().shape[1]))
        SLM_dim = self.SLM_dim
        monitor_dim = self.monitor_dim

        # Auto set window geometry according to user computer dimensions
        self.window_scale = 0.9
        self.taskbar_height = 60*self.monitor_scale
        window_height = int((self.monitor_dim[0] - self.taskbar_height) * self.window_scale - 45)  # 45 is the height of the window title
        window_hgap = int((self.monitor_dim[0] - self.taskbar_height) * (1 - self.window_scale) / 2)  # 90 is the width of default windows taskbar
        window_width = int(self.monitor_dim[1] * self.window_scale)
        window_wgap = int(self.monitor_dim[1] * (1 - self.window_scale) / 2)
        window.geometry(f"{window_width}x{window_height}+{window_wgap}+{window_hgap}")

        # Configure general window layout
        self.gap_ratio = 0.06  # gap in the content section
        window.columnconfigure(0, weight=int(round(0.8/self.gap_ratio)))
        window.columnconfigure(1, weight=1)
        window.columnconfigure(2, weight=int(1/self.gap_ratio))
        window.columnconfigure(3, weight=1)
        window.columnconfigure(4, weight=int(1.5/self.gap_ratio))
        window.columnconfigure(5, weight=1)
        window.rowconfigure(0, weight=1)
        window.rowconfigure(1, weight=int(0.5/self.gap_ratio))
        window.rowconfigure(2, weight=1)
        window.rowconfigure(3, weight=int(0.5/self.gap_ratio))
        window.rowconfigure(4, weight=1)
        window.grid_propagate(0)

        # Buttons and Entry Frame
        self.button_frame = tk.Frame(window)
        self.button_frame.grid_propagate(0)
        self.button_frame.grid(row=0, column=0, rowspan=5, sticky="nesw")

        # Set the weight of the buttons
        n_button_col = 2
        for i in range(n_button_col):
            self.button_frame.columnconfigure(i, weight=1)
        n_button_row = 13
        for i in range(n_button_row):
            self.button_frame.rowconfigure(i, weight=1)

        # Create all the buttons
        self.start_button = tk.Button(self.button_frame, text="Start", font=('Arial, 16'), command=self.vid.testFunc)
        self.start_button.grid(row=0, column=0, sticky="nesw")
        self.browse_button = tk.Button(self.button_frame, text="Browse", font=('Arial, 16'), command=self.vid.browse)
        self.browse_button.grid(row=0, column=1, sticky="nesw")
        self.stop_button = tk.Button(self.button_frame, text="Stop", font=('Arial, 16'), command=self.vid.stopGUI)
        self.stop_button.grid(row=1, column=0, sticky="nesw")
        self.display_button = tk.Button(self.button_frame, text="Display to SLM", font=('Arial, 16'), command=self.vid.displayToSLM)
        self.display_button.grid(row=1, column=1, sticky="nesw")
        self.exit_button = tk.Button(self.button_frame, text="Exit", font=('Arial, 16'), command=self.vid.exitGUI)
        self.exit_button.grid(row=2, column=0, sticky="nesw")
        self.clear_button = tk.Button(self.button_frame, text="Clear", font=('Arial, 16'), command=self.vid.clearSLM)
        self.clear_button.grid(row=2, column=1, sticky="nesw")
        self.calibrate_button = tk.Button(self.button_frame, text="Calibrate", font=('Arial, 16'), command=self.vid.calibrate)
        self.calibrate_button.grid(row=3, column=0, sticky="nesw")
        self.crosshair_button = tk.Button(self.button_frame, text="Crosshair", font=('Arial, 16'), command=self.vid.crosshair)
        self.crosshair_button.grid(row=3, column=1, sticky="nesw")

        self.trigger_button = tk.Button(self.button_frame, text="Trigger", font=('Arial, 16'), command=lambda: trigger())
        self.trigger_button.grid(row=4, column=0, sticky='nesw')
        self.one_loop_button = tk.Button(self.button_frame, text="1 loop", font=('Arial, 16'), command=self.vid.oneloop)
        self.one_loop_button.grid(row=4, column=1, sticky="nesw")

        # Create all the entries and their buttons
        self.loop_entry = tk.Entry(self.button_frame, font=('Arial, 13'), justify=tk.CENTER)
        self.loop_entry.grid(row=5, column=0, sticky="nesw")
        self.loop_entry.insert(0, str(df.loop[0]))
        self.five_loop_button = tk.Button(self.button_frame, text="n loop", font=('Arial, 16'), command=self.vid.nloops).grid(row=5, column=1, sticky="nesw")

        self.exposure_entry = tk.Entry(self.button_frame, font=('Arial, 13'), justify=tk.CENTER)
        self.exposure_entry.grid(row=6, column=0, sticky="nesw")
        self.exposure_entry.insert(0, str(df.exposure[0]))
        self.exposure_button = tk.Button(self.button_frame, text="Set Exposure", font=('Arial, 16'), command=self.vid.exposure_change).grid(row=6, column=1, sticky="nesw")

        self.gain_entry = tk.Entry(self.button_frame, font=('Arial, 13'), justify=tk.CENTER)
        self.gain_entry.grid(row=7, column=0, sticky="nesw")
        self.gain_entry.insert(0, str(df.gain[0]))
        self.gain_button = tk.Button(self.button_frame, text="Set Gain", font=('Arial, 16'), command=self.vid.gain_change).grid(row=7, column=1, sticky="nesw")

        self.save_SLM_entry = (tk.Entry(self.button_frame, font=('Arial, 13'), justify=tk.CENTER))
        self.save_SLM_entry.grid(row=8, column=0, sticky="nesw")
        self.save_SLM_button = tk.Button(self.button_frame, text="Save SLM", font=('Arial, 16'), command=self.vid.save_SLM).grid(row=8, column=1, sticky="nesw")

        self.save_entry = tk.Entry(self.button_frame, font=('Arial, 13'), justify=tk.CENTER)  # save CCD entry
        self.save_entry.grid(row=9, column=0, sticky="nesw")
        self.save_button = tk.Button(self.button_frame, text="Save CCD", font=('Arial, 16'), command=self.vid.save_image).grid(row=9, column=1, sticky="nesw")

        self.save_lineout_entry = tk.Entry(self.button_frame, font=('Arial, 13'), justify=tk.CENTER)
        self.save_lineout_entry.grid(row=10, column=0, sticky="nesw")
        self.save_lineout_button = tk.Button(self.button_frame, text="Save Lineout", font=('Arial, 16'), command=self.vid.saveLineout).grid(row=10, column=1, sticky="nesw")

        self.lineout_iso_button = tk.Button(self.button_frame, text="Lineout ISO", font=('Arial, 16'), command=lambda: lineout_iso())
        self.lineout_iso_button.grid(row=11, column=0, sticky="nesw")
        self.lineout_xy_button = tk.Button(self.button_frame, text="Lineout XY", font=('Arial, 16'), command=lambda: lineout_xy())
        self.lineout_xy_button.grid(row=11, column=1, sticky="nesw")
        self.circle_button = tk.Button(self.button_frame, text="Circle", font=('Arial, 16'), command=lambda: circleDetection())
        self.circle_button.grid(row=12, column=0, sticky="nesw")
        self.cgh_button = tk.Button(self.button_frame, text="CGH", font=('Arial, 16'), command=self.vid.cgh)
        self.cgh_button.grid(row=12, column=1, sticky="nesw")


        # Make every canvas an individual frame, might slow the GUI
        names = ['SLM', 'Preview']
        count_canvas = 0

        for i in names:
            exec(f"self.{i}_frame = tk.Frame(window, background='white')")
            exec(f"self.{i}_frame.grid(row=1 + 2 * int(count_canvas), column=2, sticky='nwse')")
            exec(f"self.{i}_frame.rowconfigure(0, weight=1)")
            exec(f"self.{i}_frame.columnconfigure(0, weight=1)")
            exec(f"self.{i}_fig = plt.figure()")
            exec(f"self.{i}_ax = self.{i}_fig.add_subplot(111)")
            exec(f"self.{i}_canvas = FigureCanvasTkAgg(self.{i}_fig, master=self.{i}_frame)")
            exec(f"self.{i}_canvas.get_tk_widget().grid()")
            exec(f"self.{i}_canvas.draw()")
            exec(f"self.{i}_label_title = tk.Label(window, text=i, font=('Arial, 14'))")
            exec(f"self.{i}_label_title.grid(row=2 * int(count_canvas), column=2, sticky='NS')")
            exec(f"self.{i}_frame.grid_propagate(0)")
            exec(f"self.{i}_label_title.grid_propagate(0)")
            count_canvas += 1

        # Set up Gap holders
        for i in range(3):
            exec(f"gap{i} = tk.Label(window)")
            exec(f"gap{i}.grid(row=0, column=1 + 2 * {i}, rowspan=5, sticky='nesw')")
            exec(f"gap{i}.grid_propagate(0)")

        self.CCD_frame = tk.Frame(window, background='white')
        self.CCD_frame.grid(row=1, column=4, rowspan=3, sticky='nesw')
        self.CCD_frame.rowconfigure(0, weight=1)
        self.CCD_frame.columnconfigure(0, weight=1)
        self.CCD_frame.grid_propagate(0)
        self.CCD_label_title = tk.Label(window, text='CCD', font=('Arial, 14'))
        self.CCD_label_title.grid(row=0, column=4, sticky='NS')
        self.CCD_fig = plt.figure(figsize=(5, 5))
        self.CCD_main_ax = self.CCD_fig.add_subplot(111)
        self.CCD_canvas = FigureCanvasTkAgg(self.CCD_fig, master=self.CCD_frame)
        self.CCD_canvas.get_tk_widget().grid(sticky='nesw')
        self.CCD_divider = make_axes_locatable(self.CCD_main_ax)
        self.CCD_top_ax = self.CCD_divider.append_axes("top", 1.05, pad=0.1, sharex=self.CCD_main_ax)
        self.CCD_right_ax = self.CCD_divider.append_axes("right", 1.05, pad=0.1, sharey=self.CCD_main_ax)
        self.CCD_top_ax.xaxis.set_tick_params(labelbottom=False)
        self.CCD_right_ax.yaxis.set_tick_params(labelleft=False)
        self.CCD_main_ax.autoscale(enable=False)
        self.CCD_right_ax.autoscale(enable=False)
        self.CCD_top_ax.autoscale(enable=False)
        self.CCD_canvas.draw()

        self.circle_toggle = False
        self.lineout_iso_toggle = False
        self.lineout_xy_toggle = False
        self.clearCanvas = True
        self.loop_pressed = False
        self.nloop_pressed = False
        self.count = 0
        self.timer = 0

        # initialize canvas data
        self.SLM_array = np.zeros((self.SLM_dim[0], self.SLM_dim[1]))
        self.SLM_image = Image.fromarray(self.SLM_array)
        self.Preview_array = self.SLM_array
        self.Preview_image = self.SLM_image
        self.CCD_array = self.vid.getFrame()
        self.CCD_image = Image.fromarray(self.CCD_array)

        name2 = ['SLM', 'Preview']
        # Show data on canvas
        for i in name2:
            exec(f"self.{i}_extent = [-int(self.{i}_array.shape[1] / 2), int(self.{i}_array.shape[1] / 2), -int(self.{i}_array.shape[0] / 2), int(self.{i}_array.shape[0] / 2)]")
            exec(f"self.{i}_ax.imshow(self.{i}_array, cmap='gray', vmin=0, vmax=255, extent=self.{i}_extent)")

        self.CCD_extent = [-int(self.CCD_array.shape[1] / 2), int(self.CCD_array.shape[1] / 2), -int(self.CCD_array.shape[0] / 2), int(self.CCD_array.shape[0] / 2)]
        self.CCD_main_ax.imshow(self.CCD_array, cmap='gray', vmin=0, vmax=255, extent=self.CCD_extent)

        def circleDetection():
            if self.circle_toggle:
                self.circle_toggle = False
                self.circle_button.config(background="SystemButtonFace")
            else:
                self.circle_toggle = True
                self.circle_button.config(background="white")

        def lineout_iso():
            if self.lineout_iso_toggle:
                self.lineout_iso_toggle = False
                self.lineout_iso_button.config(background="SystemButtonFace")
            else:
                self.lineout_iso_toggle = True
                self.lineout_xy_toggle = False
                self.lineout_xy_button.config(background="SystemButtonFace")
                self.lineout_iso_button.config(background="white")
                self.CCD_top_ax.set_title('Major Axis')
                self.CCD_right_ax.set_title('Minor Axis')

        def lineout_xy():
            if self.lineout_xy_toggle:
                self.lineout_xy_toggle = False
                self.lineout_xy_button.config(background="SystemButtonFace")
            else:
                self.lineout_xy_toggle = True
                self.lineout_iso_toggle = False
                input_max = np.amax(self.CCD_array)
                center_y = np.where(self.CCD_array == input_max)[0]
                center_x = np.where(self.CCD_array == input_max)[1]
                self.center_x = center_x[int(len(center_x) / 2)]
                self.center_y = center_y[int(len(center_y) / 2)]
                self.lineout_iso_button.config(background="SystemButtonFace")
                self.lineout_xy_button.config(background="white")
                self.CCD_top_ax.set_title('X Cross-section')
                self.CCD_right_ax.set_title('Y Cross-section')

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

        self.delay = 5
        self.update()

        onClose = self.vid.exitGUI

    def update(self):
        global SLM_image, SLM_check

        tic = time.perf_counter()
        if self.nloop_pressed or self.loop_pressed:
            print("If is triggered")
            self.currentBeam = self.CCD_array
            if self.count == 0 and self.timer == 0:
                self.beginningIntensity = np.sum(self.currentBeam[self.currentBeam > 1])
            if self.loop_pressed:
                self.maxLoops = 0
            else:
                self.maxLoops = int(self.loop_entry.get())
            if self.timer != 5:
                self.timer += 1
            if self.timer == 5:
                if self.count == 0:  # Change this to accommodate 2d threshold
                    self.gratingImg, self.gratingArray, self.goalArray, self.diff, self.threshold, self.allTest = SLM_HAMAMATSU.feedback(
                        count=self.count,
                        initialArray=self.vid.getFrame(),
                        image_transform=self.cal_transform,
                        SLM_height=self.SLM_dim[0],
                        SLM_width=self.SLM_dim[1]
                        )
                else:
                    self.gratingImg, self.gratingArray, self.goalArray, self.diff, self.threshold, self.allTest = SLM_HAMAMATSU.feedback(
                        count=self.count,
                        threshold=self.threshold,
                        initialArray=self.vid.getFrame(),
                        image_transform=self.cal_transform,
                        SLM_height=self.SLM_dim[0],
                        SLM_width=self.SLM_dim[1]
                        )

                self.SLM_array = self.gratingArray

                if self.count == self.maxLoops:
                    self.count = 0
                    self.nloop_pressed = False
                    self.loop_pressed = False
                    self.vid.SLMdisp = Image.fromarray(self.gratingArray)
                    self.goalArray = None
                else:
                    self.count += 1
                self.timer = 0
                print("THROUGHPUT: " + str(np.round(np.sum(self.currentBeam[self.currentBeam > 1]/self.beginningIntensity*100),2)) + "%")
        else:
            self.SLM_array = np.asarray(self.vid.SLMdisp)

        if len(self.SLM_array.shape) == 3:
            self.SLM_array = self.SLM_array[:, :, 0]

        self.Preview_array = np.asarray(self.vid.browseImg)

        self.SLM_check = np.array_equal(self.SLM_array, np.asarray(self.SLM_image))
        SLM_check = self.SLM_check
        self.Preview_check = np.array_equal(self.Preview_array, np.asarray(self.Preview_image))

        if not self.SLM_check:
            self.SLM_image = Image.fromarray(self.SLM_array)
            SLM_image = self.SLM_image
            self.SLM_ax.clear()
            self.SLM_extent = [-int(self.SLM_array.shape[1] / 2), int(self.SLM_array.shape[1] / 2),
                               -int(self.SLM_array.shape[0] / 2), int(self.SLM_array.shape[0] / 2)]
            self.SLM_ax.imshow(self.SLM_array, cmap='gray', vmin=0, vmax=255, extent=self.SLM_extent)
            self.SLM_canvas.draw()

        if not self.Preview_check:
            self.Preview_image = Image.fromarray(self.Preview_array)
            self.Preview_ax.clear()
            self.Preview_extent = [-int(self.Preview_array.shape[1] / 2), int(self.Preview_array.shape[1] / 2),
                                   -int(self.Preview_array.shape[0] / 2), int(self.Preview_array.shape[0] / 2)]
            self.Preview_ax.imshow(self.Preview_array, cmap='gray', vmin=0, vmax=255, extent=self.Preview_extent)
            self.Preview_canvas.draw()

        self.CCD_original = self.vid.getFrame()
        self.CCD_array = self.vid.getFrame()
        self.CCD_image = Image.fromarray(self.CCD_array)
        self.CCD_main_ax.clear()
        if self.circle_toggle:
            try:
                self.cx, self.cy, self.dx, self.dy, self.phi = lbs.beam_size(self.CCD_array)
                self.axes_arrayx, self.axes_arrayy = lbs.axes_arrays(self.cx, self.cy, self.dx, self.dy, self.phi)
                self.ellipse_arrayx, self.ellipse_arrayy = lbs.ellipse_arrays(self.cx, self.cy, self.dx, self.dy, self.phi)
                self.CCD_main_ax.plot(self.axes_arrayx-self.CCD_array.shape[1]/2, self.axes_arrayy-self.CCD_array.shape[0]/2)
                self.CCD_main_ax.plot(self.ellipse_arrayx-self.CCD_array.shape[1]/2, self.ellipse_arrayy-self.CCD_array.shape[0]/2)
                self.CCD_main_ax.set_xlim([-self.CCD_array.shape[1] / 2, self.CCD_array.shape[1] / 2])
                self.CCD_main_ax.set_ylim([-self.CCD_array.shape[0] / 2, self.CCD_array.shape[0] / 2])
            except Exception as error:
                print(error)
        self.CCD_extent = [-int(self.CCD_array.shape[1] / 2), int(self.CCD_array.shape[1] / 2),
                           -int(self.CCD_array.shape[0] / 2), int(self.CCD_array.shape[0] / 2)]
        self.CCD_main_ax.imshow(self.CCD_array, cmap='gray', vmin=0, vmax=255, extent=self.CCD_extent)
        self.CCD_canvas.draw()

        if self.lineout_iso_toggle:
            try:
                self.cx, self.cy, self.dx, self.dy, self.phi = lbs.beam_size(self.CCD_array)
                self.CCD_array_major = lbs.major_axis_arrays(self.CCD_array, self.cx, self.cy, self.dx, self.dy,
                                                             self.phi)
                self.CCD_array_minor = lbs.minor_axis_arrays(self.CCD_array, self.cx, self.cy, self.dx, self.dy,
                                                             self.phi)
                self.CCD_top_ax.clear()
                self.CCD_right_ax.clear()
                self.CCD_right_ax.set_xlim([0, 255])
                self.CCD_right_ax.set_ylim([-int(self.CCD_array.shape[0] / 2), int(self.CCD_array.shape[0] / 2)])
                self.CCD_top_ax.set_ylim([0, 255])
                self.CCD_top_ax.set_xlim([-int(self.CCD_array.shape[1] / 2), int(self.CCD_array.shape[1] / 2)])
                self.CCD_top_ax.plot(self.CCD_array_major[3], self.CCD_array_major[2])
                self.CCD_right_ax.plot(self.CCD_array_minor[2], self.CCD_array_minor[3])
                self.CCD_canvas.draw()
            except Exception as error:
                print(error)

        if self.lineout_xy_toggle:
            try:
                self.CCD_top_ax.clear()
                self.CCD_right_ax.clear()
                self.CCD_main_ax.axvline(int(self.center_x-self.CCD_array.shape[1]/2), color='r')
                self.CCD_main_ax.axhline(int(self.center_y-self.CCD_array.shape[0]/2), color='g')
                self.CCD_right_ax.set_xlim([0, 255])
                self.CCD_top_ax.set_ylim([0, 255])
                self.CCD_top_ax.plot(np.linspace(self.CCD_extent[0], self.CCD_extent[1], self.CCD_array.shape[1]), self.CCD_array[self.center_y, :], 'g-')
                self.CCD_right_ax.plot(self.CCD_array[:, self.center_x], np.linspace(self.CCD_extent[2], self.CCD_extent[3], self.CCD_array.shape[0]), 'r-')
                self.CCD_canvas.draw()
            except Exception as error:
                print(error)

        toc = time.perf_counter()
        # print(toc-tic)
        self.window.after(self.delay, self.update)


class Window2(tk.Toplevel, Page):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.geometry('{}x{}+{}+{}'.format(SLM_dim[1], SLM_dim[0], monitor_dim[1], 0))
        self.overrideredirect(1)
        self.widget = tk.Label(self, width=SLM_dim[1], height=SLM_dim[0], background='black')
        self.widget.place(x=0, y=0, relx=0, rely=0)

        self.delay = 1
        self.update2()

    def update2(self):
        if not SLM_check:
            self.SLM_image = SLM_image
            imw, imh = self.SLM_image.size

            if imw > SLM_dim[1]:
                cropsizew = (int((imw-SLM_dim[1])/2), 0, SLM_dim[1] + int((imw-SLM_dim[1])/2), imh)
                self.SLM_image = self.SLM_image.crop(cropsizew)
            if imh > SLM_dim[0]:
                imw, imh = self.SLM_image.size
                cropsizew = (0, int((imh-SLM_dim[0])/2), imw, SLM_dim[0] + int((imh-SLM_dim[0])/2))
                self.SLM_image = self.SLM_image.crop(cropsizew)

            self.photo = ImageTk.PhotoImage(image=self.SLM_image)
            self.widget.config(image=self.photo)
            self.widget.photo = self.photo

        self.after(self.delay, self.update2)


if __name__ == "__main__":
    root = tk.Tk()
    testWidget = Page(root, root)
    window2 = Window2(root)

    root.protocol("WM_DELETE_WINDOW", onClose)
    root.mainloop()