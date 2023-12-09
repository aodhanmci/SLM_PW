Code which controls a spatial light modulator (SLM) and a Basler Camera in a closed loop to optimise the near field of the laser beam. 

The GUI is built in Tkinter and should be cross platform. 

The SLM to be used is arbitary since it should be recognised as an auxiliary display. 

Current a Basler camera is required for full closed loop iteration, but this can be subsitituded for camera with a python based API.


The code works by running main.py which initiailsies the monitors (one of the SLMs) and the camera (basler). It builds the GUI. The Tkinter root.mainloop() acts as the while loop which refreshes the window with updated data (live camera feed, SLM preview etc). This runs continously until you close it. 

The 'basic' mode of operation is to find an image on your desktop and load it. this will display to the SLM. Other alternatives can be to run a function for a premade code e.g. which writes the phase map for a lens etc. 

The 'normal' mode of operation (fastest and most tested) requires a spatial calibration by imaging the SLM surface on the camera. Then one can click the 4 corners and it performs an automatic imaghe transofrm to map the SLM pixels to the camera pixels. By using the 'nloop' button, it begins the smoothing alhorithm which 'shaves' off energy into different diffraction orders (blocked by a spatial filter or removed from the beam) by setting a threshold target. The SLM has a grating fucntion which is then mutlipled by a function which detects where the beam amplitude is over a limit. It then iterates until it is close to the threshold. 

The 'development' mode requires no spatial calibration and one typically images the beam at an aribtrary location. The beam image is deskewed and then a genetic algorithm iteratively works to smooth the beam. 