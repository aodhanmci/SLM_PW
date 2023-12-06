import tkinter as tk
from video_display import *
from SLM_window import *
from oneCameraCapture import *

def onClose():
    # Your code to handle the window close event
    print("Window is closing")
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    print('1')
    camera = cameraCapture()
    testWidget = Page(root, root, camera) 
    # SLMwindow = window2(root)

    root.protocol("WM_DELETE_WINDOW", onClose)
    # root.bind('<Escape>', lambda x: onClose) # not working
    print('2')
    root.mainloop()