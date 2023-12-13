import tkinter as tk
from GUI import *

class window2(tk.Toplevel):
    def __init__(self, parent, Monitors, SLM):
        tk.Toplevel.__init__(self,parent)
        self.parent = parent
        self.Monitors = Monitors
        self.SLM = SLM
        self.title("SLM DISPLAY")
        self.geometry('%dx%d+%d+%d'%(self.Monitors.SLMwidth, self.Monitors.SLMheight, self.Monitors.SLMdisplay.x, self.Monitors.SLMdisplay.y))
        self.overrideredirect(1) # Remove window borders
        # self.geometry('%dx%d+%d+%d'%(self.Monitors.SLMwidth, self.Monitors.SLMheight, 0, 0))
        self.another_widget = tk.Label(self, width = int(self.Monitors.SLMdim[0]*3), height = int(self.Monitors.SLMdim[1]*3))
        self.another_widget.place(x=self.Monitors.SLMdim[0]/2, y=self.Monitors.SLMdim[1]/2, anchor=tk.CENTER)
        # this delay allows it to write things to the window
        self.counter_flag = 0
        self.delay=500
        self.update2()

    def update2(self):
        # this reference needs to be here to avoid garbage collection
        self.another_widget.photo = ImageTk.PhotoImage(self.SLM.SLMdisp)
        self.another_widget.config(image= self.another_widget.photo)
        self.counter_flag+=1
        # print(f'SLM: {self.counter_flag}')
        self.after(self.delay, self.update2)