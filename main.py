import tkinter as tk
from GUI import *
from SLM_window import *
from Camera import *
from monitor_initiation import *
from SLM_display import *

def onClose():
    # Your code to handle the window close event
    print("Window is closing")
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    camera = cameraCapture()
    camera.start_capture()
    Monitors = InitiateMonitors()
    SLM=DisplaySLM(Monitors)
    testWidget = Page(root, root, camera, Monitors, SLM) 
    # SLMwindow = window2(root)

    root.protocol("WM_DELETE_WINDOW", onClose)

    root.mainloop()
    camera.stop_capture()

    