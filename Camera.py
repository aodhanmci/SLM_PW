import os
from pypylon import pylon
import tkinter as tk
from tkinter.filedialog import askopenfile
import pandas as pd
import os
import threading
os.environ["PYLON_CAMEMU"] = "3"

class cameraCapture(tk.Frame):

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(cameraCapture, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            # Initialization code here
            self._initialized = True
        self.img0 = []
        self.windowName = 'SLM CCD'
        self.lock = threading.Lock()
        self.frame = None

        try:
            df = pd.read_csv('./settings/prevVals.csv', usecols=['exposure','gain'])
            # Create an instant camera object with the camera device found first.
            # maxCamerasToUse = 2
            # get transport layer and all attached devices
            tlf = pylon.TlFactory.GetInstance()
            devices = tlf.EnumerateDevices()
            NUM_CAMERAS = len(devices)
            os.environ["PYLON_CAMEMU"] = f"{NUM_CAMERAS}"
            exitCode = 0
            if NUM_CAMERAS == 0:
                raise pylon.RuntimeException("No camera connected")
            else:
                # print(f'{NUM_CAMERAS} cameras detected:\n')
                
                # for counter, device in enumerate(devices):
                #     print(f'{counter}) {device.GetFriendlyName()}') # return readable name
                #     print(f'{counter}) {device.GetFullName()}\n') # return unique code

                self.camera = pylon.InstantCamera(tlf.CreateDevice(devices[0]))
                # running=False
                # Print the model name of the camera.
                print("Using device ", self.camera.GetDeviceInfo().GetModelName())
            

            # self.camera.PixelFormat = "Mono8"
            self.camera.Open()  #Need to open camera before can use camera.ExposureTime
            # self.camera.PixelFormat = "Mono8"
            self.camera.ExposureTimeRaw = int(df.exposure[0])
            # self.camera.height = self.camera.Height.GetValue()
            # self.camera.width = self.camera.width.GetValue()
            self.camera.GainRaw = int(df.gain[0])
            self.camera.TriggerSource.SetValue("Line1")
            self.camera.AcquisitionMode.SetValue("Continuous")

            # self.camera.TriggerMode.SetValue("On")
            # self.camera.TriggerMode.GetValue()
            # Print the model name of the camera.
            # print("Using device ", self.camera.GetDeviceInfo().GetModelName())
            # print("Exposure time ", self.camera.ExposureTime.GetValue())

            # According to their default configuration, the cameras are
            # set up for free-running continuous acquisition.
            #Grabbing continuously (video) with minimal delay
            self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
            # converting to opencv bgr format
            self.converter = pylon.ImageFormatConverter()
            self.converter.OutputPixelFormat = pylon.PixelType_Mono8
            self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned


        # except genicam.GenericException as e:
        #     # Error handling
        #     print("An exception occurred.", e.GetDescription())
        #     exitCode = 1

        except Exception as error:
            print(error)
            pass
    


    def start_capture(self):
        # thread locking
        self.continue_capture = True
        self.capture_thread = threading.Thread(target=self.getFrame)
        self.capture_thread.start()

        
    def getFrame(self):
        while self.continue_capture:
            try:
                self.grabResult = self.camera.RetrieveResult(2000, pylon.TimeoutHandling_ThrowException)
                if self.grabResult.GrabSucceeded():
                    image = self.converter.Convert(self.grabResult) # Access the openCV image data
                    self.img0 = image.GetArray()
                else:
                    print("Error: ", self.grabResult.ErrorCode)
        
                self.grabResult.Release()
                #time.sleep(0.01)

                return self.img0
                
            # except genicam.GenericException as e:
            #     # Error handling
            #     print("An exception occurred.", e.GetDescription())
            #     exitCode = 1
            except Exception as error:
                if self.camera.TriggerMode.GetValue() == "On":
                    self.camera.StopGrabbing()
                    self.camera.TriggerMode.SetValue("Off")
                    self.camera.StartGrabbing()
                    print("TRIGGER NOT CONNECTED")

                    self.grabResult = self.camera.RetrieveResult(2000, pylon.TimeoutHandling_ThrowException)
                    if self.grabResult.GrabSucceeded():
                        image = self.converter.Convert(self.grabResult)  # Access the openCV image data
                        self.img0 = image.GetArray()
                    else:
                        print("Error: ", self.grabResult.ErrorCode)

                    self.grabResult.Release()
                    # time.sleep(0.01)

                    return self.img0
                else:
                    print(error)

    def stop_capture(self):
        self.continue_capture = False
        self.capture_thread.join()

    def Set_Exposure(self, exposure_value):
        with self.lock:
            self.camera.ExposureTimeRaw = exposure_value
    
    def Set_Gain(self, gain_value):
        with self.lock:
            self.camera.GainRaw = gain_value

    def Set_Trigger(self):
        with self.lock:
            if self.camera.TriggerMode.GetValue() == "On":
                try:
                    self.camera.StopGrabbing()
                    self.camera.TriggerMode.SetValue("Off")
                    self.camera.StartGrabbing()
                        # print("TRIGGER OFF")
                except Exception as error:
                    print(error)
            else:
                try:
                    self.camera.StopGrabbing()
                    self.camera.TriggerMode.SetValue("On")
                    self.camera.StartGrabbing()
                        # print("TRIGGER ON")
                except Exception as error:
                    self.camera.StopGrabbing()
                    self.camera.TriggerMode.SetValue("Off")
                    self.camera.StartGrabbing()
                        # print("TRIGGER OFF")
                    print(error)




    