import tkinter as tk
from PIL import Image
import numpy as np

class DisplaySLM(tk.Frame):
    def __init__(self, Monitors):
        self.SLMwidth = Monitors.SLMwidth
        self.SLMheight = Monitors.SLMheight
        self.SLMdisp = Image.fromarray(np.zeros((1080,1920)))
        self.browseImg = Image.open("./settings/PreSets/HAMAMATSU/HAMAMATSU_black.png")

