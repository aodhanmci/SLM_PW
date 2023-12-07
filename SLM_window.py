import tkinter as tk
from GUI import *

class window2(tk.Toplevel):
    def __init__(self, parent):

        mainDim = [1920, 1080]
        SLMdim = [1024, 768]
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
        self.overrideredirect(1) # Remove window borders
        self.another_widget = tk.Label(self, width = int(SLMdim[0]*3), height = int(SLMdim[1]*3))
        self.another_widget.place(x=SLMdim[0]/2, y=SLMdim[1]/2, anchor=tk.CENTER)
        self.SLMimage = np.zeros((SLMdim[0], SLMdim[1]))
        self.SLMimage[0][0] = None
        self.SLMpreview = self.SLMimage

        self.delay=1
        self.update2()

    def update2(self):
        
        SLMimage = ImageOps.fit(Image.fromarray(self.SLMimage), (int(self.SLMdims[0]), int(self.SLMdims[1])))
        SLMimage = np.asarray(SLMimage)
        self.SLMpreview = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(SLMimage))
                # self.SLMpreview = PIL.ImageTk.PhotoImage(image=SLMimage)
                # self.SLMpreview = SLMimage
        self.another_widget.photo = self.SLMpreview
                # self.another_widget.image = self.SLMpreview
        self.another_widget.config(image=self.SLMpreview)
                # self.another_widget.attributes("-fullscreen", True)
                # self.another_widget.pack(fill="both")

                # print("CHANGED SLM")

        self.after(self.delay, self.update2)