import tkinter as tk
from tkinter import ttk, PhotoImage, filedialog
from tkinter.filedialog import askopenfile
from tkinter.constants import *
import oneCameraCapture
from PIL import Image, ImageTk
import numpy as np
import cv2
import PIL
import SLM_TEST_GUI
import screeninfo
from screeninfo import get_monitors

small_button_height = 20
small_button_width = 50

large_button_height = 30
large_button_width = 90

button_gap = 0

window_width = 1500
window_height = 600

scale_percent = 30 # percent of original size
width_scale = int(window_width * scale_percent / 100)
height_scale = int(window_height * scale_percent / 100)
dim = (width_scale, height_scale)
# print(dim)
first_row_button_height = window_height-2*large_button_height-2*button_gap
second_row_button_height = window_height-large_button_height-button_gap

upper_row_dict = {"y":first_row_button_height, "height":large_button_height, "width":large_button_width}
lower_row_dict = {"y":second_row_button_height, "height":large_button_height, "width":large_button_width}

class Page(tk.Frame):

    def __init__(self, parent, window):
        
        tk.Frame.__init__(self, parent)

        # super(Page, self).__init__()

        self.window = window
        window.title("SLM & CCD Control")
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
        self.stop_button = tk.Button(window, text="Stop", command=self.vid.stop)
        self.stop_button.place(x=large_button_width, **upper_row_dict)
        self.exit_button = tk.Button(window, text="Exit")
        self.exit_button.place(x=2*large_button_width, **upper_row_dict)

        self.browse_button = tk.Button(window, text="Browse", command=self.vid.browse)
        self.browse_button.place(x=0, **lower_row_dict)
        self.display_button = tk.Button(window, text="Display to SLM", command=self.vid.displayToSLM)
        self.display_button.place(x=1*large_button_width, **lower_row_dict)
        self.one_loop_button = tk.Button(window, text="1 loop")
        self.one_loop_button.place(x=2*large_button_width, **lower_row_dict)
        self.five_loop_button = tk.Button(window, text="5 loop")
        self.five_loop_button.place(x=3*large_button_width, **lower_row_dict)
        self.clear_button = tk.Button(window, text="Clear", command=self.vid.clearSLM)
        self.clear_button.place(x=4*large_button_width, **lower_row_dict)
        self.calibrate_button = tk.Button(window, text="Calibrate")
        self.calibrate_button.place(x=6*large_button_width, **lower_row_dict)

        # Create labels and entry widgets for exposure, gain, and save file
        self.exposure_button = tk.Button(window, text="Set Exposure", command=self.vid.exposure_change)
        self.exposure_button.place(x=window_width-3*large_button_width, **lower_row_dict)
        self.gain_button = tk.Button(window, text="Set Gain", command=self.vid.gain_change)
        self.gain_button.place(x=window_width-2*large_button_width, **lower_row_dict)
        self.save_button = tk.Button(window, text="Save File", command=self.vid.save_image)
        self.save_button.place(x=window_width-large_button_width, **lower_row_dict)

        self.exposure_entry = tk.Entry(window)
        self.exposure_entry.place(x=window_width-3*large_button_width, **upper_row_dict)
        self.gain_entry = tk.Entry(window)
        self.gain_entry.place(x=window_width-2*large_button_width, **upper_row_dict)
        self.save_entry = tk.Entry(window)
        self.save_entry.place(x=window_width-1*large_button_width, **upper_row_dict)
        
        # Detect SLM monitor
        self.SLMdisplayNum = 0
        self.SLMdisplay = screeninfo.get_monitors()[self.SLMdisplayNum]
        self.SLMdim = (int(self.SLMdisplay.width), int(self.SLMdisplay.height))

        # cv2.namedWindow('SLM', cv2.WINDOW_NORMAL)
        # cv2.moveWindow('SLM', self.SLMdisplay.x - 1, self.SLMdisplay.y - 1)
        # cv2.setWindowProperty('SLM', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        # print(self.SLMdim)     # width = 1280, height = 1024




        #Create a canvas that will fit the camera source
        self.SLM_image_widget = tk.Label(window, width=int(self.SLMdim[0]*scale_percent/100), height=int(self.SLMdim[1]*scale_percent/100))
        self.SLM_image_widget.place(x=1*window_width/4, y=window_height/2, anchor=tk.CENTER)

        # self.ccd_image_widget = tk.Label(window, width=width_scale, height=height_scale)
        self.ccd_image_widget = tk.Label(window, width=int(self.vid.getFrame().shape[1]*scale_percent/100), height=int(self.vid.getFrame().shape[0]*scale_percent/100))
        self.ccd_image_widget.place(x=3*window_width/4, y=window_height/2, anchor=tk.CENTER)

        self.delay=10
        self.update()






    def update(self):
        #Get a frame from cameraCapture

        # Example arrays (you can replace these with your actual image data)
        # image_array1 = np.random.randint(0, 256, size=(int(self.SLMdim[0]*scale_percent/100), int(self.SLMdim[1]*scale_percent/100)), dtype=np.uint8).T
        # image_array2 = np.random.randint(0, 10, size=(width_scale, height_scale), dtype=np.uint8).T
        # Convert NumPy arrays to Pillow Images
        # image1 = Image.fromarray(image_array1)
        # image2 = Image.fromarray(image_array2)

        photo1 = np.asarray(self.vid.SLMdisp)
        # print(type(photo1))
        photo1 = cv2.resize(photo1, dsize=(int(self.SLMdim[0]*scale_percent/100), int(self.SLMdim[1]*scale_percent/100)))
        photo1 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(photo1))
        self.SLM_image_widget.photo = photo1
        self.SLM_image_widget.config(image=photo1)

        # cv2.imshow('SLM', np.asarray(self.vid.SLMdisp))

        # photo2 = PIL.ImageTk.PhotoImage(image=image2)
        # self.ccd_image_widget.photo = photo2
        # self.ccd_image_widget.config(image=photo2)

        self.ccd_data = self.vid.getFrame() #This is an array
        self.ccd_data = cv2.resize(self.ccd_data, dsize=(int(self.vid.getFrame().shape[1]*scale_percent/100), int(self.vid.getFrame().shape[0]*scale_percent/100)), interpolation=cv2.INTER_CUBIC)
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.ccd_data))
        self.ccd_image_widget.config(image=self.photo)
        self.ccd_image_widget.photo = self.photo

        self.window.after(self.delay, self.update)


        # label = tk.Label(self.window2)
        # photo2 = PIL.ImageTk.PhotoImage(image=self.vid.SLMdisp)
        # label.photo = photo2
        # label.config(image=photo2)
        # self.window2.mainloop()


class window2(tk.Toplevel):
    def __init__(self, parent):

        tk.Toplevel.__init__(self,parent)
        self.parent = parent
        self.title("Second Window")
        self.geometry(f"{window_width}x{window_height}")
        self.another_widget = tk.Label(self, width = 600, height = 400)
        self.another_widget.place(x=300, y=200, anchor=tk.CENTER)



        self.delay=10
        self.update2()

    def update2(self):

        # image2 = np.asarray(Image.open("data.png"))
        image2 = np.random.randint(0, 256, size=(1200,800), dtype=np.uint8).T
        image2 = cv2.resize(np.uint8(image2), dsize=(600, 400))
        image3 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image2))
        self.another_widget.photo = image3
        self.another_widget.config(image=image3)

        self.after(self.delay, self.update2)



if __name__ == "__main__":
    root = tk.Tk()
    testWidget = Page(root, root) 

    window2 = window2(root)

    root.mainloop()

