import cv2
import numpy as np
import os
import pandas as pd
import timeit
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from pypylon import pylon
from pypylon import genicam
import screeninfo
from numpy import asarray
from SLM_TEST_GUI import *
maxCamerasToUse = 2

# get transport layer and all attached devices
maximagestograb = 50
tlf = pylon.TlFactory.GetInstance()
devices = tlf.EnumerateDevices()
NUM_CAMERAS = len(devices)
os.environ["PYLON_CAMEMU"] = f"{NUM_CAMERAS}"
exitCode = 0
if NUM_CAMERAS == 0:
    raise pylon.RuntimeException("No camera connected")
else:
    print(f'{NUM_CAMERAS} cameras detected:\n')

    for counter, device in enumerate(devices):
        print(f'{counter}) {device.GetFriendlyName()}')  # return readable name
        print(f'{counter}) {device.GetFullName()}\n')  # return unique code

scale_percent = 60  # percent of original size
width = int(1920 * scale_percent / 100)
height = int(1200 * scale_percent / 100)
dim = (width, height)

screen_id = 1

# get the size of the screen
screen = screeninfo.get_monitors()[screen_id]
# screen = screeninfo.get_monitors()
print(screen)
window_name = 'SLM'
width, height = screen.width, screen.height

root = tk.Tk()
root.title("SLM CCD")
root.geometry(f"{width}x{height}")

# Create a label for the SLM image
slm_image_label = tk.Label(root)
slm_image_label.pack()

# Create a label for the CCD image
ccd_image_label = tk.Label(root)
ccd_image_label.pack()

# Create buttons
start_button = tk.Button(root, text="Start")
stop_button = tk.Button(root, text="Stop")
exit_button = tk.Button(root, text="Exit")
upload_single_button = tk.Button(root, text="Upload Single")
one_loop_button = tk.Button(root, text="1 loop")
five_loop_button = tk.Button(root, text="5 loop")
clear_button = tk.Button(root, text="Clear")
calibrate_button = tk.Button(root, text="Calibrate")

start_button.pack()
stop_button.pack()
exit_button.pack()
upload_single_button.pack()
one_loop_button.pack()
five_loop_button.pack()
clear_button.pack()
calibrate_button.pack()

# Create labels and entry widgets for exposure, gain, and save file
exposure_label = tk.Label(root, text="Exposure")
gain_label = tk.Label(root, text="Gain")
save_label = tk.Label(root, text="Save File")

exposure_label.pack()
exposure_entry = tk.Entry(root)
exposure_entry.pack()

gain_label.pack()
gain_entry = tk.Entry(root)
gain_entry.pack()

save_label.pack()
save_entry = tk.Entry(root)
save_entry.pack()

# Create buttons for saving exposure, gain, and image
save_exposure_button = tk.Button(root, text="Save Exposure")
save_gain_button = tk.Button(root, text="Save Gain")
save_slm_image_button = tk.Button(root, text="Save SLM Image")

save_exposure_button.pack()
save_gain_button.pack()
save_slm_image_button.pack()

# Create canvas for Matplotlib plot
canvas_frame = tk.Frame(root)
canvas_frame.pack()

# Define Matplotlib figure
fig = Figure()
ax = fig.add_subplot(111)
ax.set_xlabel("X axis")
ax.set_ylabel("Y axis")
ax.grid()
canvas = FigureCanvasTkAgg(fig, canvas_frame)
canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

# Add event handlers for buttons

def display_image(dataArray):
    global slm_image_label
    global slm_photo
    frame = cv2.resize(dataArray, dim, interpolation=cv2.INTER_AREA)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    slm_photo = ImageTk.PhotoImage(Image.fromarray(img))
    slm_image_label.config(image=slm_photo)
    slm_image_label.image = slm_photo

def grab_ccd(camera):
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    data = grabResult.GetArray()
    global ccd_photo
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

def on_calibrate():
    match = False
    camera.StopGrabbing()
    while not match:
        xZoom = input("Enter xZoom: ")
        yZoom = input("Enter yZoom: ")
        xShift = input("Enter xShift: ")
        yShift = input("Enter yShift: ")
        angle = input("Enter angle: ")
        data2 = calibration(data, float(xZoom), float(yZoom), float(xShift), float(yShift), float(angle))
        data2Img = Image.fromarray(data2)
        data2Img.show()
        crosshairImg.show()

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
calibrate_button.config(command=on_calibrate)
save_exposure_button.config(command=on_exposure_change)
save_gain_button.config(command=on_gain_change)
save_slm_image_button.config(command=on_save_slm_image)

image_window = pylon.PylonImageWindow()
image_window.Create(1)
# Create an instant camera object with the camera device found first.
camera = pylon.InstantCamera(tlf.CreateDevice(devices[0]))
running = False
# Print the model name of the camera.
print("Using device ", camera.GetDeviceInfo().GetModelName())

camera.Open()
# default acquisition attributes when opening the camera
# camera.ExposureTimeRaw = 180000
# camera.GainRaw = 190
camera.PixelFormat = "Mono8"
# take previously set values as default
camera.ExposureTimeRaw = int(100)
camera.GainRaw = int(0)
# camera.StartGrabbingMax(5000, pylon.GrabStrategy_LatestImageOnly)
camera.StartGrabbing()
# pylon.FeaturePersistence.Save("test.txt", camera.GetNodeMap())

root.mainloop()
