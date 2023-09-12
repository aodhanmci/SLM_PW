import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from tkinter import PhotoImage
import oneCameraCapture
from PIL import Image, ImageTk
import numpy as np
from tkinter import PhotoImage
import cv2
import PIL

small_button_height = 20
small_button_width = 50

large_button_height = 30
large_button_width = 90

button_gap = 0

window_width = 1500
window_height = 600

scale_percent = 40 # percent of original size
width_scale = int(window_width * scale_percent / 100)
height_scale = int(window_height * scale_percent / 100)
dim = (width_scale, height_scale)
print(dim)
second_row_button_height = window_height-2*large_button_height-button_gap
first_row_button_height = window_height-large_button_height

upper_row_dict = {"y":first_row_button_height, "height":large_button_height, "width":large_button_width}
lower_row_dict = {"y":second_row_button_height, "height":large_button_height, "width":large_button_width}

class Page(tk.Frame):

    def __init__(self, parent, window):
        
        tk.Frame.__init__(self, parent)
        self.window = window
        self.window.title = "SLM CCD"

        window.geometry(f"{window_width}x{window_height}")

        # Create a label for the SLM image
        self.vid = oneCameraCapture.cameraCapture(self)
        self.slm_image_label = tk.Label(window, text="SLM")
        self.slm_image_label.place(x=0.25*window_width, y=20)
        self.slm_image_window = tk.Canvas(window, width = 100, height=100)
        self.slm_image_window.pack()
        # slm_image_window.create_image(0, 0, image = np.ones((100, 100)))

        # Create a label for the CCD image
        self.ccd_image_label = tk.Label(window, text="CCD")
        self.ccd_image_label.place(x=0.75*window_width, y=20)

        # Create buttons
        self.start_button = tk.Button(window, text="Start")
        self.start_button.place(x=0, **upper_row_dict)
        self.stop_button = tk.Button(window, text="Stop")
        self.stop_button.place(x=large_button_width, **upper_row_dict)
        self.exit_button = tk.Button(window, text="Exit")
        self.exit_button.place(x=2*large_button_width, **upper_row_dict)

        self.upload_single_button = tk.Button(window, text="Upload Single")
        self.upload_single_button.place(x=0, **lower_row_dict)
        self.one_loop_button = tk.Button(window, text="1 loop")
        self.one_loop_button.place(x=large_button_width, **lower_row_dict)
        self.five_loop_button = tk.Button(window, text="5 loop")
        self.five_loop_button.place(x=2*large_button_width, **lower_row_dict)
        self.clear_button = tk.Button(window, text="Clear")
        self.clear_button.place(x=3*large_button_width, **lower_row_dict)
        self.calibrate_button = tk.Button(window, text="Calibrate")
        self.calibrate_button.place(x=4*large_button_width, **lower_row_dict)

        # Create labels and entry widgets for exposure, gain, and save file
        self.exposure_button = tk.Button(window, text="Set Exposure", command=self.vid.exposure_change)
        self.exposure_button.place(x=window_width-3*large_button_width, **upper_row_dict)
        self.gain_button = tk.Button(window, text="Set Gain", command=self.vid.gain_change)
        self.gain_button.place(x=window_width-2*large_button_width, **upper_row_dict)
        self.save_button = tk.Button(window, text="Save File", command=self.vid.save_image)
        self.save_button.place(x=window_width-large_button_width, **upper_row_dict)

        self.exposure_entry = tk.Entry(window)
        self.exposure_entry.place(x=window_width-3*large_button_width, **lower_row_dict)
        self.gain_entry = tk.Entry(window)
        self.gain_entry.place(x=window_width-2*large_button_width, **lower_row_dict)
        self.save_entry = tk.Entry(window)
        self.save_entry.place(x=window_width-1*large_button_width, **lower_row_dict)
        #Open camera source
        
        #Create a canvas that will fit the camera source
        self.SLM_image_widget = tk.Label(window, width=width_scale, height=height_scale)
        self.SLM_image_widget.place(x=1*window_width/4, y=window_height/2, anchor=tk.CENTER)

        self.ccd_image_widget = tk.Label(window, width=width_scale, height=height_scale)
        self.ccd_image_widget.place(x=3*window_width/4, y=window_height/2, anchor=tk.CENTER)

        self.delay=10
        self.update()



    def update(self):
        #Get a frame from cameraCapture

        # Example arrays (you can replace these with your actual image data)
        image_array1 = np.random.randint(0, 256, size=(width_scale, height_scale), dtype=np.uint8).T
        image_array2 = np.random.randint(0, 10, size=(width_scale, height_scale), dtype=np.uint8).T
        # Convert NumPy arrays to Pillow Images
        image1 = Image.fromarray(image_array1)
        image2 = Image.fromarray(image_array2)

        photo1 = PIL.ImageTk.PhotoImage(image=image1)
        self.SLM_image_widget.photo = photo1
        self.SLM_image_widget.config(image=photo1)

        photo2 = PIL.ImageTk.PhotoImage(image=image2)
        self.ccd_image_widget.photo = photo2
        self.ccd_image_widget.config(image=photo2)

        # ccd_data = self.vid.getFrame() #This is an array
        # ccd_data = cv2.resize(ccd_data, dsize=(width_scale, height_scale), interpolation=cv2.INTER_CUBIC)
        # self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(ccd_data))
        # self.ccd_image_widget.config(image=self.photo)
        # self.ccd_image_widget.photo = self.photo

        self.window.after(self.delay, self.update)





if __name__ == "__main__":
    root = tk.Tk()
    testWidget = Page(root, root) 
    root.mainloop()