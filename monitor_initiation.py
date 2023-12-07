import tkinter as tk
import screeninfo

class InitiateMonitors(tk.Frame):
    def __init__(self):
        self.mainDisplayNum = 0
        self.mainDisplay = screeninfo.get_monitors()[self.mainDisplayNum]
        self.mainDim = (int(self.mainDisplay.width), int(self.mainDisplay.height))

        self.SLMdisplayNum = 1
        self.SLMdisplay = screeninfo.get_monitors()[self.SLMdisplayNum]
        self.SLMdim = (int(self.SLMdisplay.width), int(self.SLMdisplay.height))
        SLMdim = self.SLMdim

        # Define dimensions for object placement
        SLMwidth = SLMdim[0]
        SLMheight = SLMdim[1]
        self.SLMwidth = SLMwidth
        self.SLMheight = SLMheight
