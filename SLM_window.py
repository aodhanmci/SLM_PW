import tkinter as tk
from GUI import *

class window2(tk.Toplevel):
    def __init__(self, parent, Monitors, SLM):
        tk.Toplevel.__init__(self,parent)
        self.parent = parent
        self.Monitors = Monitors
        self.SLM = SLM
        self.title("SLM DISPLAY")
        self.geometry('%dx%d+%d+%d'%(self.Monitors.SLMwidth, self.Monitors.SLMheight, self.Monitors.mainDisplay.width, 0))
        self.overrideredirect(1) # Remove window borders
        self.another_widget = tk.Label(self, width = int(self.Monitors.SLMdim[0]*3), height = int(self.Monitors.SLMdim[1]*3))
        self.another_widget.place(x=self.Monitors.SLMdim[0]/2, y=self.Monitors.SLMdim[1]/2, anchor=tk.CENTER)

        self.delay=50
        self.update2()

    def update2(self):
        
        self.another_widget.config(image=ImageTk.PhotoImage(self.SLM.SLMdisp))
        self.after(self.delay, self.update2)