import PySimpleGUI as sg
import cv2
import numpy as np
from pypylon import pylon
from pypylon import genicam
import os
import time
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

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
        print(f'{counter}) {device.GetFriendlyName()}') # return readable name
        print(f'{counter}) {device.GetFullName()}\n') # return unique code

scale_percent = 60 # percent of original size
width = int(1920 * scale_percent / 100)
height = int(1200 * scale_percent / 100)
dim = (width, height)


def main():

    sg.theme('Black')

    # define the window layout
    SLM_layout = [  [sg.Text('SLM')],
                [sg.Image(filename='', key='SLM Image')],
                [sg.Button('Start'), sg.Button('Stop'), sg.Button('Exit')],
                [sg.Button('Upload Single'), sg.FileBrowse(key="-SLM_Single-"), sg.Button('1 loop'), sg.Button('5 loop')]
                ]
    
    CCD_layout =  [  [sg.Text('CCD')],
                [sg.Image(filename='', key='CCD Image')],
                [sg.Text('save file', key='-SAVE_OUT-', font=('Arial Bold', 12), justification='center'), sg.Text('Exposure', key='-EXPOSURE_OUT-', font=('Arial Bold', 12), justification='center'), sg.Text('Gain', key='-GainE_OUT-', font=('Arial Bold', 12), justification='center')],
                [sg.Input('', enable_events=True, key='-INPUT_SAVE-', font=('Arial Bold', 12), justification='left'), sg.Input('', enable_events=True, key='-INPUT_EXP-', font=('Arial Bold', 12), justification='left'), sg.Input('', enable_events=True, key='-INPUT_Gain-', font=('Arial Bold', 12), justification='left')],
                [sg.Button('save'), sg.Button('exposure'), sg.Button('gain')]
                                ]
    # layout = [[sg.VPush()],
    #           [sg.Push(), sg.Column(column_to_be_centered,element_justification='c'), sg.Push()],
    #           [sg.VPush()]]

    layout =   [  [sg.Column(SLM_layout),
     sg.VSeperator(),
     sg.Column(CCD_layout)]]
    # create the window and show it without the plot
    window = sg.Window('SLM CCD',
                       layout, location=(100, 100), resizable=True)

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    imageWindow = pylon.PylonImageWindow()
    imageWindow.Create(1)
        # Create an instant camera object with the camera device found first.
    camera = pylon.InstantCamera(tlf.CreateDevice(devices[0]))
    running=False
    # Print the model name of the camera.
    print("Using device ", camera.GetDeviceInfo().GetModelName())

    camera.Open()
    # default acquisition attributes when opening the camera
    camera.ExposureTimeRaw = 5000
    camera.GainRaw = 0
    camera.PixelFormat = "Mono8"
    # camera.StartGrabbingMax(5000, pylon.GrabStrategy_LatestImageOnly)
    camera.StartGrabbing()
    # pylon.FeaturePersistence.Save("test.txt", camera.GetNodeMap())

    while True:
        event, values = window.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            window.close()
            camera.Close()
            return

        elif event == 'Start':
            running = True

        elif event == 'Stop':
            running = False

        if running:
            grabResult = camera.RetrieveResult(50000, pylon.TimeoutHandling_ThrowException)
            data = grabResult.GetArray()

            frame = cv2.resize(data, dim, interpolation=cv2.INTER_AREA)
            imgdata = cv2.imencode('.png', frame)[1].tobytes()

            window['CCD Image'].update(imgdata)
        
        if event == 'save':
            filename = values['-INPUT_SAVE-']
            cv2.imwrite(f'{filename}.png', data)
        if event == 'exposure':
            camera.ExposureTimeRaw = int(values['-INPUT_EXP-'])
        if event == 'gain':
            camera.GainRaw = int(values['-INPUT_Gain-'])
        if event == 'Upload Single':
            SLM_image = values["-SLM_Single-"]
            print(SLM_image)
            data = cv2.imread(SLM_image)
            frame = cv2.resize(data, dim, interpolation=cv2.INTER_AREA)
            SLM_image = cv2.imencode('.png', frame)[1].tobytes()
            window['SLM Image'].update(SLM_image)

        # 
        # print



main()