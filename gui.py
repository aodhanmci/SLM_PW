import PySimpleGUI as sg
import cv2
import numpy as np
from pypylon import pylon
from pypylon import genicam
import os
import time
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from SLM_TEST_GUI import runFeedback, feedback, calibration
import screeninfo
from numpy import asarray
import csv
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure

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

screen_id = 1

# get the size of the screen
screen = screeninfo.get_monitors()[screen_id]
# screen = screeninfo.get_monitors()
print(screen)
window_name = 'SLM'
width, height = screen.width, screen.height
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                                cv2.WINDOW_FULLSCREEN)

crosshairImg = Image.open('/Users/loasis/Documents/GitHub/SLM_PW/calibration/crosshair4.png')
crosshairArray = asarray(crosshairImg)



def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def displayImage(dataArray, window):
    frame = cv2.resize(dataArray, dim, interpolation=cv2.INTER_AREA)
    SLM_image = cv2.imencode('.png', frame)[1].tobytes()
    window['SLM Image'].update(SLM_image)
    cv2.imshow(window_name, dataArray)

def grabCCD(camera, window):
    grabResult = camera.RetrieveResult(50000, pylon.TimeoutHandling_ThrowException)
    data = grabResult.GetArray()

    frame = cv2.resize(data, dim, interpolation=cv2.INTER_AREA)
    imgdata = cv2.imencode('.png', frame)[1].tobytes()

    window['CCD Image'].update(imgdata)

    return data

def clearSLM(window):
    dataClear = np.zeros((1920,1080))
    displayImage(dataClear, window)


def main():

    sg.theme('Black')

    df = pd.read_csv('prevVals.csv', usecols=['exposure','gain'])

    # define the window layout
    SLM_layout = [  [sg.Text('SLM')],
                [sg.Image(filename='', key='SLM Image')],
                [sg.Button('Start'), sg.Button('Stop'), sg.Button('Exit')],
                [sg.Button('Upload Single'), sg.FileBrowse(key="-SLM_Single-"), sg.Button('1 loop'), sg.Button('5 loop'), sg.Button('Clear'), sg.Button('Calibrate'), sg.Button('Lineout')]
                ]
    
    CCD_layout =  [  [sg.Text('CCD')],
                [sg.Image(filename='', key='CCD Image')],
                [sg.Text('save file', key='-SAVE_OUT-', font=('Arial Bold', 12), justification='center'), sg.Text('Exposure', key='-EXPOSURE_OUT-', font=('Arial Bold', 12), justification='center'), sg.Text('Gain', key='-GainE_OUT-', font=('Arial Bold', 12), justification='center')],
                [sg.Input('', enable_events=True, key='-INPUT_SAVE-', font=('Arial Bold', 12), justification='left'), sg.Input(str(df.exposure[0]), enable_events=True, key='-INPUT_EXP-', font=('Arial Bold', 12), justification='left'), sg.Input(str(df.gain[0]), enable_events=True, key='-INPUT_Gain-', font=('Arial Bold', 12), justification='left')],
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
                       layout, location=(100, 100), resizable=False)

# second window  things
    # layout2 = [[sg.Text('Animated Matplotlib', size=(40, 1),
    #             justification='center', font='Helvetica 20')],
    #           [sg.Canvas(size=(640, 480), key='-CANVAS-')]
    # ]

    # # create the form and show it without the plot
    # window2 = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI',
    #             layout2, finalize=True)

    # canvas_elem = window2['-CANVAS-']
    # canvas = canvas_elem.TKCanvas

    # # draw the initial plot in the window
    # fig = Figure()
    # ax = fig.add_subplot(111)
    # ax.set_xlabel("X axis")
    # ax.set_ylabel("Y axis")
    # ax.grid()
    # fig_agg = draw_figure(canvas, fig)


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
    # camera.ExposureTimeRaw = 180000
    # camera.GainRaw = 190
    camera.PixelFormat = "Mono8"
    # take previously set values as default
    camera.ExposureTimeRaw = int(df.exposure[0])
    camera.GainRaw = int(df.gain[0])
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
            clearSLM(window)

        elif event == 'Stop':
            running = False

            df = pd.DataFrame({'exposure': [camera.ExposureTimeRaw.GetValue()],
                               'gain': [camera.GainRaw.GetValue()]})
            df.to_csv('prevVals.csv', index=False)
            

        if running:
            data = grabCCD(camera, window)
            # ax.cla()                    # clear the subplot
            # ax.grid()                   # draw the grid
            # ax.plot(data[120, :],  color='purple')
            # fig_agg.draw()
        if event == 'save':
            filename = values['-INPUT_SAVE-']
            cv2.imwrite(f'/Users/loasis/Documents/GitHub/SLM_PW/{filename}.png', data)
        if event == 'exposure':
            camera.ExposureTimeRaw = int(values['-INPUT_EXP-'])
        if event == 'gain':
            camera.GainRaw = int(values['-INPUT_Gain-'])
        if event == 'Upload Single':
            SLM_image = values["-SLM_Single-"]
            print(SLM_image)
            data_single_upload = cv2.imread(SLM_image)
            displayImage(data_single_upload, window)
            
            # cv2.waitKey()
        if event == 'Clear':
            clearSLM(window)
        if event == '1 loop':
            resultImg, resultArray, diff = feedback(initialArray = data)

            print("DIFF: " + str(np.round(diff,2)))
            displayImage(resultArray, window)

            resultImg.save('/Users/loasis/Documents/GitHub/SLM_PW/manualTestRESULT.png')

            # SLM_grating_img = Image.fromarray(resultArray, 'L')
            # # data = cv2.imread(resultImg)
            # data = cv2.imread(SLM_grating_img)
            # frame = cv2.resize(data, dim, interpolation=cv2.INTER_AREA)
            # SLM_image = cv2.imencode('.png', frame)[1].tobytes()
            # window['SLM Image'].update(SLM_image)
        if event == '5 loop':
            for i in np.arange(9):
                camera.StopGrabbing()
                # data = grabCCD(camera, window)
                print("RUNNING")
                # try:
                camera.StartGrabbingMax(1)
                data = grabCCD(camera, window)
                gratingImg, gratingArray, diff = feedback(
                    count = i,
                    plot = True,
                    initialArray = data
                )
                displayImage(gratingArray, window)
                window.refresh()
                time.sleep(1)
                

                # data = grabCCD(camera, window)

                # gratingImg.show()
                print("DIFF: " + str(np.round(diff,2)))
                # data = grabCCD(camera, window)

                window.refresh()
               
                if i == 8:
                    camera.StartGrabbing()
                # except:
                #     print("ERROR")
                #     pass
        if event == 'Calibrate':
                match = False
                camera.StopGrabbing()
                while match == False:
                # data = grabCCD(camera, window)

                    # for i in np.arange(2):
                    #     displayImage(data, window)
                    #     window.refresh()
                    #     time.sleep(0.1)
                    #     displayImage(crosshairArray, window)
                    #     window.refresh()
                    #     time.sleep(0.1)
                    #     data = grabCCD(camera, window)
                    # displayImage(crosshairArray, window)
                    # time.sleep(2)
                    # camera.StartGrabbingMax(1)
                    # time.sleep(1)
                    # window.refresh()
                    # time.sleep(2)

                    xZoom = input("Enter xZoom: ")
                    yZoom = input("Enter yZoom: ")
                    xShift = input("Enter xShift: ")
                    yShift = input("Enter yShift: ")
                    angle = input("Enter angle: ")

                    data2 = calibration(data, float(xZoom), float(yZoom), float(xShift), float(yShift), float(angle))

                    data2Img = Image.fromarray(data2)
                    data2Img.show()
                    crosshairImg.show()

            # userInput = input("Input here: ")
                # if userInput == "Done":
                #     match = True
            


        # 
        # print

# print("Hello")

main()
