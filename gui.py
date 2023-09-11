import PySimpleGUI as sg
import cv2
import numpy as np
# from pypylon import pylon
# from pypylon import genicam
import os
import time
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
# import screeninfo
from numpy import asarray
import csv
import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import messagebox
import pypylon as pylon

small_button_height = 20
small_button_width = 50

large_button_height = 30
large_button_width = 90

button_gap = 0

window_width = 1500
window_height = 800

second_row_button_height = window_height-2*large_button_height-button_gap
first_row_button_height = window_height-large_button_height

upper_row_dict = {"y":first_row_button_height, "height":large_button_height, "width":large_button_width}
lower_row_dict = {"y":second_row_button_height, "height":large_button_height, "width":large_button_width}
root = tk.Tk()
root.title("SLM CCD")
root.geometry(f"{window_width}x{window_height}")

# Create a label for the SLM image
slm_image_label = tk.Label(root, text="SLM")
slm_image_label.place(x=0.25*window_width, y=20)
slm_image_window = tk.Canvas(root, width = 100, height=100)
slm_image_window.pack()
slm_image_window.create_image(0, 0, image = np.ones((100, 100)))

# Create a label for the CCD image
ccd_image_label = tk.Label(root, text="CCD")
ccd_image_label.place(x=0.75*window_width, y=20)

# Create buttons
start_button = tk.Button(root, text="Start")
start_button.place(x=0, **upper_row_dict)
stop_button = tk.Button(root, text="Stop")
stop_button.place(x=large_button_width, **upper_row_dict)
exit_button = tk.Button(root, text="Exit")
exit_button.place(x=2*large_button_width, **upper_row_dict)

upload_single_button = tk.Button(root, text="Upload Single")
upload_single_button.place(x=0, **lower_row_dict)
one_loop_button = tk.Button(root, text="1 loop")
one_loop_button.place(x=large_button_width, **lower_row_dict)
five_loop_button = tk.Button(root, text="5 loop")
five_loop_button.place(x=2*large_button_width, **lower_row_dict)
clear_button = tk.Button(root, text="Clear")
clear_button.place(x=3*large_button_width, **lower_row_dict)
calibrate_button = tk.Button(root, text="Calibrate")
calibrate_button.place(x=4*large_button_width, **lower_row_dict)

# Create labels and entry widgets for exposure, gain, and save file
exposure_button = tk.Button(root, text="Set Exposure")
exposure_button.place(x=window_width-3*large_button_width, **upper_row_dict)
gain_button = tk.Button(root, text="Set Gain")
gain_button.place(x=window_width-2*large_button_width, **upper_row_dict)
save_button = tk.Button(root, text="Save File")
save_button.place(x=window_width-large_button_width, **upper_row_dict)

exposure_entry = tk.Entry(root)
exposure_entry.place(x=window_width-3*large_button_width, **lower_row_dict)
gain_entry = tk.Entry(root)
gain_entry.place(x=window_width-2*large_button_width, **lower_row_dict)
save_entry = tk.Entry(root)
save_entry.place(x=window_width-1*large_button_width, **lower_row_dict)

# converter = pylon.ImageFormatConverter()

# # converting to opencv bgr format
# converter.OutputPixelFormat = pylon.PixelType_BGR8packed
# converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

# maxCamerasToUse = 2
# # get transport layer and all attached devices
# maximagestograb = 50
# tlf = pylon.TlFactory.GetInstance()
# devices = tlf.EnumerateDevices()
# NUM_CAMERAS = len(devices)
# os.environ["PYLON_CAMEMU"] = f"{NUM_CAMERAS}"
# exitCode = 0
# if NUM_CAMERAS == 0:
#     raise pylon.RuntimeException("No camera connected")
# else:
#     print(f'{NUM_CAMERAS} cameras detected:\n')
    
#     for counter, device in enumerate(devices):
#         print(f'{counter}) {device.GetFriendlyName()}') # return readable name
#         print(f'{counter}) {device.GetFullName()}\n') # return unique code

# scale_percent = 60 # percent of original size
# width = int(1920 * scale_percent / 100)
# height = int(1200 * scale_percent / 100)
# dim = (width, height)


# camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
# screen_id = 1

# # get the size of the screen
# screen = screeninfo.get_monitors()[screen_id]
# # screen = screeninfo.get_monitors()
# print(screen)


def display_image(dataArray):
    frame = cv2.resize(dataArray, dim, interpolation=cv2.INTER_AREA)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    slm_photo = ImageTk.PhotoImage(Image.fromarray(img))
    slm_image_label.config(image=slm_photo)
    slm_image_label.image = slm_photo

def grab_ccd(camera):
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    data = grabResult.GetArray()
    frame = cv2.resize(data, dim, interpolation=cv2.INTER_AREA)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    ccd_photo = ImageTk.PhotoImage(Image.fromarray(img))
    ccd_image_label.config(image=ccd_photo)
    ccd_image_label.image = ccd_photo
    return data

def clear_slm():
    data_clear = np.zeros((1920, 1080))
    display_image(data_clear)

def on_start():
    global running
    running = True
    clear_slm()

def on_stop(camera):
    global running
    running = False
    df = pd.DataFrame({'exposure': [camera.ExposureTimeRaw.GetValue()],
                       'gain': [camera.GainRaw.GetValue()]})
    df.to_csv('prevVals.csv', index=False)

def on_save(camera, filename):
    data = grab_ccd(camera)
    cv2.imwrite(f'/Users/loasis/Documents/GitHub/SLM_PW/{filename}.png', data)

def on_exposure_change():
    try:
        camera.ExposureTimeRaw = int(exposure_entry.get())
        exposure_entry.config(background="white")
    except ValueError:
        exposure_entry.config(background="red")

def on_gain_change():
    try:
        camera.GainRaw = int(gain_entry.get())
        gain_entry.config(background="white")
    except ValueError:
        gain_entry.config(background="red")

def on_upload_single():
    filename = filedialog.askopenfilename()
    if filename:
        data_single_upload = cv2.imread(filename)
        display_image(data_single_upload)

def on_clear():
    clear_slm()

def on_one_loop():
    global threshold
    resultImg, resultArray, diff = feedback(initialArray=data)
    print("DIFF: " + str(np.round(diff, 2)))
    display_image(resultArray)
    resultImg.save('/Users/loasis/Documents/GitHub/SLM_PW/manualTestRESULT.png')

def on_five_loop():
    numLoops = 9
    for i in np.arange(numLoops):
        camera.StopGrabbing()
        camera.StartGrabbingMax(1)
        data = grab_ccd(camera)
        if i == 0:
            gratingImg, gratingArray, diff, threshold, allTest = feedback(
                count=i,
                plot=True,
                initialArray=data
            )
        else:
            gratingImg, gratingArray, diff, threshold, allTest = feedback(
                count=i,
                plot=True,
                threshold=threshold,
                initialArray=data
            )
        display_image(gratingArray)
        root.update()
        time.sleep(1)
    camera.StartGrabbing()


def on_save_slm_image():
    gratingImg.save('/Users/loasis/Documents/GitHub/SLM_PW/SLMimage.png')
    print("SLM image saved")

start_button.config(command=on_start)
stop_button.config(command=lambda: on_stop(camera))
exit_button.config(command=root.destroy)
upload_single_button.config(command=on_upload_single)
one_loop_button.config(command=on_one_loop)
five_loop_button.config(command=on_five_loop)
clear_button.config(command=on_clear)
# save_exposure_button.config(command=on_exposure_change)
# save_gain_button.config(command=on_gain_change)
# save_slm_image_button.config(command=on_save_slm_image)

root.mainloop()