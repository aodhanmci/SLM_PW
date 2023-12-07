import tkinter as tk
from PIL import Image
import numpy as np
from tkinter import ttk, PhotoImage, filedialog

class DisplaySLM(tk.Frame):
    def __init__(self, Monitors):
        self.SLMwidth = Monitors.SLMwidth
        self.SLMheight = Monitors.SLMheight
        self.SLMdisp = Image.fromarray(np.zeros((1080,1920)))
        self.browseImg = Image.open("./settings/PreSets/HAMAMATSU/HAMAMATSU_black.png")
        self.browseImg = np.array(Image.open("./settings/PreSets/HAMAMATSU/HAMAMATSU_black.png"))

    def browse(self):
        try:
            f_types = [('hurry up and pick one', '*.*')]
            filename = filedialog.askopenfilename(filetypes=f_types)
            self.browseImg = Image.open(filename)
            self.browseImgArray = np.asarray(self.browseImg)
            # self.page.browse_button.config(background='SystemButtonFace')
        except Exception as error:
            self.page.browse_button.config(background='red')
            print(error)

    def displayToSLM(self):
        try:
            self.SLMdisp = Image.fromarray(self.browseImgArray)
            # self.page.display_button.config(background='SystemButtonFace')
        except AttributeError as error:
            print("NO IMAGE SELECTED")
            # print(error)
            # self.page.display_button.config(background='red')
        except Exception as error:
            print(error)
            # self.page.display_button.config(background='red')

    def clearSLM(self):
        self.SLMdisp = Image.fromarray(np.zeros((1080,1920)))
        self.page.clearSLM = True

