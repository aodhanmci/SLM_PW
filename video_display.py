import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from tkinter import PhotoImage
import oneCameraCapture
from PIL import Image, ImageTk
import numpy as np
from tkinter import PhotoImage
small_button_height = 20
small_button_width = 50

large_button_height = 30
large_button_width = 90

button_gap = 0

window_width = 1200
window_height = 600

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
        slm_image_label = tk.Label(window, text="SLM")
        slm_image_label.place(x=0.25*window_width, y=20)
        slm_image_window = tk.Canvas(window, width = 100, height=100)
        slm_image_window.pack()
        # slm_image_window.create_image(0, 0, image = np.ones((100, 100)))

        # Create a label for the CCD image
        ccd_image_label = tk.Label(window, text="CCD")
        ccd_image_label.place(x=0.75*window_width, y=20)

        # Create buttons
        start_button = tk.Button(window, text="Start")
        start_button.place(x=0, **upper_row_dict)
        stop_button = tk.Button(window, text="Stop")
        stop_button.place(x=large_button_width, **upper_row_dict)
        exit_button = tk.Button(window, text="Exit")
        exit_button.place(x=2*large_button_width, **upper_row_dict)

        upload_single_button = tk.Button(window, text="Upload Single")
        upload_single_button.place(x=0, **lower_row_dict)
        one_loop_button = tk.Button(window, text="1 loop")
        one_loop_button.place(x=large_button_width, **lower_row_dict)
        five_loop_button = tk.Button(window, text="5 loop")
        five_loop_button.place(x=2*large_button_width, **lower_row_dict)
        clear_button = tk.Button(window, text="Clear")
        clear_button.place(x=3*large_button_width, **lower_row_dict)
        calibrate_button = tk.Button(window, text="Calibrate")
        calibrate_button.place(x=4*large_button_width, **lower_row_dict)

        # Create labels and entry widgets for exposure, gain, and save file
        exposure_button = tk.Button(window, text="Set Exposure")
        exposure_button.place(x=window_width-3*large_button_width, **upper_row_dict)
        gain_button = tk.Button(window, text="Set Gain")
        gain_button.place(x=window_width-2*large_button_width, **upper_row_dict)
        save_button = tk.Button(window, text="Save File")
        save_button.place(x=window_width-large_button_width, **upper_row_dict)

        exposure_entry = tk.Entry(window)
        exposure_entry.place(x=window_width-3*large_button_width, **lower_row_dict)
        gain_entry = tk.Entry(window)
        gain_entry.place(x=window_width-2*large_button_width, **lower_row_dict)
        save_entry = tk.Entry(window)
        save_entry.place(x=window_width-1*large_button_width, **lower_row_dict)
        #Open camera source
        # self.vid = oneCameraCapture.cameraCapture()
        image_size = 4/4*window_width
        #Create a canvas that will fit the camera source
        self.canvas_SLM = tk.Canvas(window, width=int(window_width/2),height=int(window_width/4))
        self.canvas_SLM.place(x=475, y=window_height/2, anchor=tk.CENTER)

        self.canvas_CCD = tk.Canvas(window, width=int(window_width/2),height=int(window_width/4))
        self.canvas_CCD.place(x=0.9*1200, y=window_height/2, anchor=tk.CENTER)

        self.delay=10
        self.update()
        #self.window.mainloop()


    def update(self):
        #Get a frame from cameraCapture
        # frame = self.vid.getFrame() #This is an array
        # Example arrays (you can replace these with your actual image data)
        image_array1 = np.random.randint(0, 256, size=(int(window_width), int(window_height)), dtype=np.uint8)
        image_array2 = np.random.randint(0, 16, size=(int(window_width), int(window_height)), dtype=np.uint8)

        # Convert NumPy arrays to Pillow Images
        image1 = Image.fromarray(image_array1)
        image2 = Image.fromarray(image_array2)

        # Convert Pillow Images to PhotoImage objects
        photo1 = ImageTk.PhotoImage(image=image1)
        photo2 = ImageTk.PhotoImage(image=image2)

        # self.canvas_SLM.config(width=image1.width, height=image1.height)
        self.canvas_SLM.create_image(0, 0, anchor=tk.CENTER, image=photo1)
        self.canvas_SLM.photo = photo1  # Store a reference to prevent garbage collection

        # self.canvas_CCD.config(width=image2.width, height=image2.height)
        self.canvas_CCD.create_image(0, 0, anchor=tk.CENTER, image=photo2)
        self.canvas_CCD.photo = photo2  # Store a reference to prevent garbage collection


    # def saveImage(self):
    #     # Get a frame from the video source
    #     frame = self.vid.getFrame()

    #     cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg",
    #                 cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))



if __name__ == "__main__":
    root = tk.Tk()
    testWidget = Page(root, root) 
    # testWidget.grid(row=0, column=0, sticky="W")
    root.mainloop()