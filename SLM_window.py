import tkinter as tk
from GUI import *

class window2(tk.Toplevel):
    def __init__(self, parent, Monitors, SLM):


        # print(mainWidth, mainHeight, SLMwidth, SLMheight)

        tk.Toplevel.__init__(self,parent)
        self.parent = parent
        self.Monitors = Monitors
        self.SLM = SLM
        self.title("SLM DISPLAY")
        self.geometry('%dx%d+%d+%d'%(self.Monitors.SLMwidth, self.Monitors.SLMheight, self.Monitors.mainDisplay.width, 0))
        self.overrideredirect(1) # Remove window borders
        self.another_widget = tk.Label(self, width = int(self.Monitors.SLMdim[0]*3), height = int(self.Monitors.SLMdim[1]*3))
        self.another_widget.place(x=self.Monitors.SLMdim[0]/2, y=self.Monitors.SLMdim[1]/2, anchor=tk.CENTER)

        self.delay=1
        self.update2()

    def update2(self):
        
        SLMimage = ImageOps.fit(Image.fromarray(self.SLM.SLMdisp), (int(self.Monitors.SLMdim[0]), int(self.Monitors.SLMdim[1])))
        SLMimage = np.asarray(SLMimage)
        self.SLM.Preview = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(SLMimage))
                # self.SLMpreview = PIL.ImageTk.PhotoImage(image=SLMimage)
                # self.SLMpreview = SLMimage
        self.another_widget.photo = self.SLM.Preview
                # self.another_widget.image = self.SLMpreview
        self.another_widget.config(image=self.SLM.Preview)
                # self.another_widget.attributes("-fullscreen", True)
                # self.another_widget.pack(fill="both")

                # print("CHANGED SLM")

        self.after(self.delay, self.update2)