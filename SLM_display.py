import tkinter as tk
from PIL import Image
import numpy as np
from tkinter import filedialog
import os

class DisplaySLM(tk.Frame):
    def __init__(self, Monitors):
        self.SLMwidth = Monitors.SLMwidth
        self.SLMheight = Monitors.SLMheight
        self.SLMdisp = Image.fromarray(np.zeros((Monitors.SLMdim[1],Monitors.SLMdim[0])))
        self.browseImg = np.array(self.SLMdisp)
        # self.SLMdisp = Image.open("./settings/PreSets/HAMAMATSU/HAMAMATSU_black.png")
        # self.browseImg = Image.open("./settings/PreSets/HAMAMATSU/HAMAMATSU_black.png")
        # self.browseImg = np.array(Image.open("./settings/PreSets/HAMAMATSU/HAMAMATSU_black.png"))
        
        self.SLMimage = np.zeros((Monitors.SLMdim[1], Monitors.SLMdim[0]))
        self.SLMimage[0][0] = None
        self.SLMpreview = self.SLMimage

    def browse(self):
        try:
            f_types = [('are you sure?', '*.*')]
            filename = filedialog.askopenfilename(filetypes=f_types)
            self.browseImg = Image.open(filename)
            self.browseImgArray = np.asarray(self.browseImg)
            self.basename = os.path.basename(filename)
            return self.basename
            # self.page.browse_button.config(background='SystemButtonFace')
        except Exception as error:
            # self.GUI.browse_button.config(background='red')
            print(error)
            return str("Error")

    def displayToSLM(self):
        try:
            self.SLMdisp = Image.fromarray(self.browseImgArray)
            return self.basename
            # self.page.display_button.config(background='SystemButtonFace')
        except AttributeError as error:
            print("NO IMAGE SELECTED")
            return str("NO IMAGE SELECTED")
            # print(error)
            # self.page.display_button.config(background='red')
        except Exception as error:
            print(error)
            return str("Error")
            # self.page.display_button.config(background='red')

    def clearSLM(self):
        self.SLMdisp = Image.fromarray(np.zeros((self.SLMheight, self.SLMwidth)))
        # print(self.SLMheight, self.SLMwidth)
        # self.page.clearSLM = True

