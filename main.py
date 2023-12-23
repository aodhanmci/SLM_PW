import tkinter as tk
import PIL
from GUI import *
from SLM_window import *
from Camera import *
from monitor_initiation import *
from SLM_display import *

def close_application():
    if SLMwindow.winfo_exists():
        SLMwindow.destroy()
    GUIwindow.exitGUI()

if __name__ == "__main__":
    root = tk.Tk()

    camera = cameraCapture()
    camera.start_capture() # thread locking
    
    Monitors = InitiateMonitors()
    SLM=DisplaySLM(Monitors)
    GUIwindow = Page(root, root, camera, Monitors, SLM) 
    SLMwindow = window2(root, Monitors, SLM, GUIwindow)
    root.protocol("WM_DELETE_WINDOW", close_application)
    root.mainloop()
    camera.stop_capture() # thread locking

