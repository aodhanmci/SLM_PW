import tkinter as tk
from tkinter.constants import *
from PIL import Image
import numpy as np
import cv2
import PIL
from Anthony_flattening import *
from GA_flattening import *
from GA_weights import *
import pandas as pd
import laserbeamsize as lbs
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import random
from scipy.ndimage import gaussian_filter

class Page(tk.Frame):

    def __init__(self, parent, window, camera, Monitors, SLM):

        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.window = window
        self.SLM = SLM
        window.title("SLM & CCD Control")
        # window.geometry(f"{window_width}x{window_height}")
        self.camera=camera
        self.Monitors = Monitors
        

        # self.CCDwidth = camera.getFrame().shape[1] # 1920
        # self.CCDheight = camera.getFrame().shape[0] # 1200
        # print(self.camera.camera.Width)
        self.CCDwidth = self.camera.camera.Width.GetValue()
        self.CCDheight = self.camera.camera.Height.GetValue()
        # self.CCDwidth=1600
        # self.CCDheight=1200

        scale_percent = 30 # percent of original size
        self.scale_percent = scale_percent
        gap = min(self.Monitors.SLMwidth, self.CCDwidth)*scale_percent/600

        window_width = int(self.Monitors.SLMwidth*scale_percent/100 + self.CCDwidth*scale_percent/100 + 3*gap)
        window_height = int(max(self.Monitors.SLMheight, self.CCDheight)*scale_percent/50 + 3*gap)

        window.geometry(f"{window_width}x{window_height}+{int(self.Monitors.mainDim[0]/2-window_width/2)}+{int(self.Monitors.mainDim[1]/2-window_height/2-gap/2)}")

        # just leaving this here
        large_button_height = 30
        large_button_width = 60

        button_gap = 0

        first_row_button_height = window_height-2*large_button_height-2*button_gap
        second_row_button_height = window_height-large_button_height-button_gap

        upper_row_dict = {"y":first_row_button_height, "height":large_button_height, "width":large_button_width}
        lower_row_dict = {"y":second_row_button_height, "height":large_button_height, "width":large_button_width}

        df = pd.read_csv('./settings/prevVals.csv', usecols=['exposure','gain','loop'])
        self.ccd_data = np.zeros_like((self.CCDwidth, self.CCDheight))
        # Create a label for the SLM image
        self.slm_image_label = tk.Label(window, text="SLM")
        self.slm_image_label.place(
            x = self.Monitors.SLMwidth*scale_percent/200 + gap,
            y= gap/2,
            anchor=tk.CENTER
            )
        name_label = tk.Label(window, text="Aodhan McIlvenny and Anthony Lu LBNL")
        name_label.place(
            x = 120,
            y= 10, 
            anchor=tk.CENTER
            )
        # Create a label for the CCD image
        self.ccd_image_label = tk.Label(window, text="CCD")
        self.ccd_image_label.place(
            x = window_width - self.CCDwidth*scale_percent/200 - gap,
            y= gap/2, 
            anchor=tk.CENTER
            )
        
        self.slm_preview_label = tk.Label(window, text="SLM Preview")
        self.slm_preview_label.place(
            x = self.Monitors.SLMwidth*scale_percent/200 + gap,
            y= 3*gap/2 + max(self.Monitors.SLMheight, self.CCDheight)*scale_percent/100, 
            anchor=tk.CENTER
            )
        
        self.lineout_label = tk.Label(window, text="Center Lineout")
        self.lineout_label.place(
            x = window_width - self.CCDwidth*scale_percent/200 - gap,
            y= 3*gap/2 + max(self.Monitors.SLMheight, self.CCDheight)*scale_percent/100, 
            anchor=tk.CENTER
            )

        # Create buttons
        self.start_button = tk.Button(window, text="Start", command=self.testFunc)
        self.start_button.place(x=0, **upper_row_dict)
        self.stop_button = tk.Button(window, text="Stop", command=self.stopGUI)
        self.stop_button.place(x=large_button_width, **upper_row_dict)
        self.exit_button = tk.Button(window, text="Exit", command=self.exitGUI)
        self.exit_button.place(x=2*large_button_width, **upper_row_dict)
        self.save_SLM_entry = tk.Entry(window)
        self.save_SLM_entry.place(x=3*large_button_width, **upper_row_dict)
        self.GA_Start_button = tk.Button(window, text="GA GO", command=self.GA_Start)
        self.GA_Start_button.place(x=4*large_button_width, **upper_row_dict)
        self.background_button = tk.Button(window, text="BG", command=self.get_background)
        self.background_button.place(x=6*large_button_width, **upper_row_dict)

        self.loop_entry = tk.Entry(window)
        self.loop_entry.insert(0, str(df.loop[0]))
        self.loop_entry.place(x=5*large_button_width, **upper_row_dict)

        self.browse_button = tk.Button(window, text="Browse", command=self.SLM.browse)
        self.browse_button.place(x=0, **lower_row_dict)
        self.display_button = tk.Button(window, text="Display to SLM", command=SLM.displayToSLM)
        self.display_button.place(x=1*large_button_width, **lower_row_dict)
        self.clear_button = tk.Button(window, text="Clear", command=SLM.clearSLM)
        self.clear_button.place(x=2*large_button_width, **lower_row_dict)
        self.save_SLM_button = tk.Button(window, text="Save SLM", command=self.save_SLM)
        self.save_SLM_button.place(x=3*large_button_width, **lower_row_dict)
        self.GA_button = tk.Button(window, text="GA", command=self.GA_parameters)
        self.GA_button.place(x=4*large_button_width, **lower_row_dict)
        self.five_loop_button = tk.Button(window, text="n loop", command=self.nloops)
        self.five_loop_button.place(x=5*large_button_width, **lower_row_dict)
        self.crosshair_button = tk.Button(window, text="Crosshair", command=self.crosshair)
        self.crosshair_button.place(x=6*large_button_width, **lower_row_dict)
        self.calibrate_button = tk.Button(window, text="Calibrate", command=self.calibrate)
        self.calibrate_button.place(x=7*large_button_width, **lower_row_dict)
        self.circle_button = tk.Button(window, text="Circle", command=self.circleDetection)
        self.circle_button.place(x=8*large_button_width, **lower_row_dict)
        self.lineout_toggle=False
        self.lineout_button = tk.Button(window, text="Lineout", command= self.lineout)
        self.lineout_button.place(x=9*large_button_width, **lower_row_dict)
        self.trigger_button = tk.Button(window, text="Trigger", command=self.trigger)
        self.trigger_button.place(x=10*large_button_width, **lower_row_dict)
        self.wf_button = tk.Button(window, text="WF", command=self.wf)
        self.wf_button.place(x=11*large_button_width, **lower_row_dict)

        # Create labels and entry widgets for exposure, gain, and save file
        self.exposure_button = tk.Button(window, text="Set Exposure", command=self.exposure_change)
        self.exposure_button.place(x=window_width-4*large_button_width, **lower_row_dict)
        self.gain_button = tk.Button(window, text="Set Gain", command=self.gain_change)
        self.gain_button.place(x=window_width-3*large_button_width, **lower_row_dict)
        self.save_button = tk.Button(window, text="Save CCD", command=self.save_image)
        self.save_button.place(x=window_width-2*large_button_width, **lower_row_dict)
        self.save_lineout_button = tk.Button(window, text="Save Lineout", command=self.saveLineout)
        self.save_lineout_button.place(x=window_width-large_button_width, **lower_row_dict)

        self.exposure_entry = tk.Entry(window)
        self.exposure_entry.insert(0, str(df.exposure[0]))
        self.exposure_entry.place(x=window_width-4*large_button_width, **upper_row_dict)
        self.gain_entry = tk.Entry(window)
        self.gain_entry.insert(0, str(df.gain[0]))
        self.gain_entry.place(x=window_width-3*large_button_width, **upper_row_dict)
        self.save_entry = tk.Entry(window)
        self.save_entry.place(x=window_width-2*large_button_width, **upper_row_dict)
        
        self.save_lineout_entry = tk.Entry(window)
        self.save_lineout_entry.place(x=window_width-large_button_width, **upper_row_dict)
        # with self.camera.lock:
        #     self.ccd_data = self.camera.getFrame()
        # load in the last saved image transformation object
        try:
            with open('./settings/calibration/warp_transform.pckl', 'rb') as warp_trans_file:
                self.cal_transform = pickle.load(warp_trans_file)
        except FileNotFoundError:
            print('No image transform file found. Pls calibrate.')
            self.cal_transform = 0
        self.counter_flag = 0
        
        self.ccd_data_gui = np.zeros((int(self.CCDwidth*scale_percent/100),int(self.CCDheight*scale_percent/100)))
        #Create a canvas that will display what is on the SLM
        self.SLM_image_widget = tk.Label(window, 
                                         width=int(self.Monitors.SLMwidth*scale_percent/100),
                                         height=int(self.Monitors.SLMheight*scale_percent/100),
                                         anchor=tk.CENTER
                                         )
        self.SLM_image_widget.place(
                                    x = int(self.Monitors.SLMwidth*scale_percent/200 + gap),
                                    y = int(max(self.Monitors.SLMheight, self.CCDheight)*scale_percent/200 + gap),
                                    anchor=tk.CENTER
                                    )

        #Create a canvas that will show the CCD image
        self.ccd_image_widget = tk.Label(window, 
                                         width=int(self.CCDwidth*scale_percent/100), 
                                         height=int(self.CCDheight*scale_percent/100),
                                         anchor=tk.CENTER
                                         )
        self.ccd_image_widget.place(
                                    x = int(window_width - self.CCDwidth*scale_percent/200 - gap),
                                    y = int(max(self.Monitors.SLMheight, self.CCDheight)*scale_percent/200 + gap),
                                    anchor=tk.CENTER
                                    )

        #Create a canvas that will preview the SLM image
        self.SLM_preview_widget = tk.Label(window, 
                                         width=int(self.Monitors.SLMwidth*scale_percent/100),
                                         height=int(self.Monitors.SLMheight*scale_percent/100),
                                         anchor=tk.CENTER
                                         )
        self.SLM_preview_widget.place(
                                    x = int(self.Monitors.SLMwidth*scale_percent/200 + gap),
                                    y = int(max(self.Monitors.SLMheight, self.CCDheight)*scale_percent*1.5/100 + 2*gap),
                                    anchor=tk.CENTER
                                    )

        fig, ax = plt.subplots(figsize=(4.5,3.5))

        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().place(
                                    x = int(window_width - self.CCDwidth*scale_percent/200 - gap),
                                    y = int(max(self.Monitors.SLMheight, self.CCDheight)*scale_percent*1.5/100 + 2*gap),
                                    anchor=tk.CENTER
        )

        self.ax = ax
        self.canvas = canvas
        self.fig = fig

        self.circle_toggle = False
        self.lineout_toggle = False
        # self.trigger_toggle = False
        self.clearCanvas = True
        self.loop_pressed = False
        self.nloop_pressed = False
        self.clearSLM = False
        self.background_toggle = False
        self.background = np.zeros((self.CCDheight, self.CCDwidth))
        ##### initialising Anthony Feedback
        self.count = 0 
        self.CCDtime = 0
        self.SLMtime = 0
        self.initialtime = 0
        self.beginning_intensity = 0
        self.flattening_object = Flattening_algo(self.SLM.SLMwidth, self.SLM.SLMheight, self.loop_entry.get(), self.cal_transform)
        
        ##### initialisng machine learning feedback
        self.generation_number_counter = 0
        self.population_number_counter = 0
        self.GA_GO=False
        self.weights_pressed=False
        ##### end of anthony initialising
        self.delay=1000
        print("HELLO")
        self.after(self.delay, self.update)
        ## end of initialisation ##
    

    def gain_change(self):
        try:
            self.camera.Set_Gain(int(self.gain_entry.get()))
            self.gain_entry.config(background="white")
        except Exception as error:
            print(error)
            self.gain_entry.config(background="red")

    def exposure_change(self):
        try:
            self.camera.Set_Exposure(int(self.exposure_entry.get()))
            self.exposure_entry.config(background="white")
        except Exception as error:
            print(error)
            self.exposure_entry.config(background="red")
    
    
    def get_background(self):
        if self.background_toggle == False:
            self.background = self.ccd_data
            self.background_toggle = True
        else:
            self.background = np.zeros_like((self.CCDheight, self.CCDwidth))
            self.background_toggle = False



    def GA_parameters(self):
        
        self.GA_window = tk.Toplevel(self.parent)
        self.GA_window.geometry("300x300")
        self.GA_window.title("Genetic Algorithm Flattening")
        self.GA_population_label = tk.Label(self.GA_window , text="Initial Population")
        self.GA_population_label.grid(row=0, column=0)
        self.GA_population_entry = tk.Entry(self.GA_window)
        self.GA_population_entry.insert(0, "30")
        self.GA_population_entry.grid(row=0, column=1)
        self.GA_generation_label = tk.Label(self.GA_window , text="Number of Gens")
        self.GA_generation_label.grid(row=1, column=0)
        self.GA_generations_entry = tk.Entry(self.GA_window)
        self.GA_generations_entry.insert(0, "50")
        self.GA_generations_entry.grid(row=1, column=1)
        self.GA_mutation_label = tk.Label(self.GA_window , text="Mutation Rate")
        self.GA_mutation_label.grid(row=2, column=0)
        self.GA_mutation_rate_entry = tk.Entry(self.GA_window)
        self.GA_mutation_rate_entry.insert(0, "0.2")
        self.GA_mutation_rate_entry.grid(row=2, column=1)
        self.GA_parents_label = tk.Label(self.GA_window , text="Num of Parents")
        self.GA_parents_label.grid(row=3, column=0)
        self.GA_num_parents_entry = tk.Entry(self.GA_window)
        self.GA_num_parents_entry.insert(0, "10")
        self.GA_num_parents_entry.grid(row=3, column=1)
        self.GA_weight_button = tk.Button(self.GA_window, text="Weights", command=self.GA_Weight)
        self.GA_weight_button.grid(row=4, column=0)      
        self.GA_update = tk.Button(self.GA_window, text="Update and Close", command=self.GA_update_function)
        self.GA_update.grid(row=4, column=1)
    
    def GA_Weight(self):
        self.weights_pressed = True
        self.GA_weight_object = GA_weight(self.SLM.SLMwidth, self.SLM.SLMheight)

    def GA_update_function(self):
        self.GA_population = int(self.GA_population_entry.get())
        self.GA_generation = int(self.GA_generations_entry.get())
        self.GA_mutation_rate = float(self.GA_mutation_rate_entry.get())
        self.GA_num_parents = int(self.GA_num_parents_entry.get())
        self.GA_window.destroy()

    def GA_Start(self):
        self.GA_GO=True
        self.GA_object = flattening_GA(self.GA_population, self.GA_generation, self.GA_num_parents, self.GA_mutation_rate, self.SLM.SLMwidth, self.SLM.SLMheight)

    def nloops(self):
        self.nloop_pressed = True
    
    def save_SLM(self):
        filename = self.save_SLM_entry.get()
        try:
            cv2.imwrite(f'./data/{filename}.png', asarray(self.SLM.SLMdisp))  # Save the captured image to a file
            print(f"Image saved as /data/{filename}.png")
            self.save_SLM_button.config(background="SystemButtonFace")
        except Exception as error:
            print(error)
            self.save_SLM_button.config(background="red")
    
    def crosshair(self):
        self.SLM.SLMdisp = Image.open("./settings/calibration/HAMAMATSU/crosshairNums.png")
    
    def testFunc(self):
        # self.camera.StartGrabbing()
        pass
    
    ## this has been moved to Anthony flattening
    def calibrate(self):
        warp_transform = Flattening_algo.calibration(self.SLM.SLMdisp, self.ccd_data)
        self.cal_transform = warp_transform

    def save_image(self):
        filename = self.save_entry.get()
        try:
            cv2.imwrite(f'{filename}.png', self.ccd_data)  # Save the captured image to a file
            print(f"Image saved as {filename}.png")
            self.save_button.config(background="SystemButtonFace")

        except Exception as error:
            print(error)
            self.save_button.config(background="red")
    
    def saveLineout(self):
        filename = self.save_lineout_entry.get()
        try:
            self.fig.savefig(f"./data/{filename}")
            print(f"Image saved as /data/{filename}.png")
            self.save_SLM_button.config(background="SystemButtonFace")
        except Exception as error:
            print(error)
            self.save_SLM_button.config(background="red")

    def circleDetection(self):
        if self.circle_toggle:
            self.circle_toggle = False
            self.circle_button.config(background="SystemButtonFace")
        else:
            self.circle_toggle = True
            self.circle_button.config(background="white")

    def lineout(self):
        if self.lineout_toggle:
            self.lineout_toggle = False
            self.lineout_button.config(background="SystemButtonFace")
        else:
            self.lineout_toggle = True
            self.lineout_button.config(background="white")


    def trigger(self):
        self.camera.Set_Trigger()
        

    def stopGUI(self):
        self.camera.StopGrabbing()
        print("Stopped")
        pass

    def exitGUI(self):
        print("GOODBYE")
        df = pd.DataFrame({'exposure': [self.exposure_entry.get()],
                           'gain': [self.gain_entry.get()],
                           'loop': [self.loop_entry.get()]})
        df.to_csv('./settings/prevVals.csv', index=False)
        self.camera.camera.Close()
        self.parent.destroy()
        

    def wf(self):
            # gratingArray = Image.fromarray(gratingArray).show()

            # totalMultArray[xi,yi] = totalMultArray[xi,yi] + yshift
        # yshiftArray = np.ones(shape=gratingArray.shape)  # Initialize yshift array
            # print(yshiftArray[0][0])
            # yshiftArray = yshiftArray * 70
            # print(yshiftArray[0][0])
            # yshiftArray = yshiftArray
            # print(yshiftArray[0][0])

            # yshiftArray[xi,yi] = totalMultArray[xi,yi]     # Shift grating arary proportional to the local value of the grating array. Creates yshift the same shape as the grating
            # yshiftArray[xi,yi] = 70 - totalMultArray[xi,yi] * 2     # Shift entire grating upward, and antiproportional to shape of grating. With some tweaking, this creates a final grating which has a flat top (all values match at top) and the yshift mirrors that
            # yshiftArray[xi,yi] = 50     # Constant yshift ONLY IN THE THRESHOLD AREA. Gaussian blur below ensures smooth transition back to zero outside the threshold area.
            # yshiftArray[xi,yi] = 70 - (totalMultArray[xi,yi] **2) / 100     # Squaring totalMultArray accounts LESS for the shape of totalMultArray. Just testing other ways to make different yshift shapes.

        yshiftArray = gaussian_filter(yshiftArray,
                                          sigma=15)  # Smooth transition from yshift to zero. Testing shows ideal sigma value of 15.
            # totalMultArray = totalMultArray + yshiftArray     # Directly add yshift to previous grating
        totalMultArray = totalMultArray


    def update(self):
        # self.counter_flag +=1
        # print(f'CCD: {self.counter_flag}')
        with self.camera.lock:
            self.ccd_data = self.camera.getFrame() - self.background # Access the shared frame in a thread-safe manner
            self.ccd_data_gui = cv2.resize(self.ccd_data, dsize=(int(self.ccd_data.shape[1]*self.scale_percent/100), int(self.ccd_data.shape[0]*self.scale_percent/100)), interpolation=cv2.INTER_CUBIC)
        # print(np.shape(self.ccd_data))
        ########### Flattening

        ########### Anthony Flattening
        if self.nloop_pressed == True:
            
            self.flattening_object.ccd_data = self.ccd_data
            gratingImg, SLMgrating, goalArray, diff, threshold, allTest = self.flattening_object.feedback()
            self.flattening_object.threshold = threshold
            print(threshold)
        
            self.flattening_object.count +=1
            self.SLM.SLMdisp=PIL.Image.fromarray(SLMgrating)
            self.delay = 500
            if self.flattening_object.count == int(self.loop_entry.get()):
                self.nloop_pressed = False
                self.loop_pressed = False
                self.flattening_object.count=0
                # self.delay=100

        ##### creates weights used for genetic algorithm
                
        elif self.weights_pressed == True:
            if self.population_number_counter == 0:
                amplitudes = self.GA_weight_object.initialize_weight_individual_block_based(self.population_number_counter)
                image = self.GA_weight_object.apply_weight_block_pattern_to_grid(amplitudes)
            elif self.population_number_counter <= self.GA_weight_object.weight_population_size -1:
                amplitudes = self.GA_weight_object.initialize_weight_individual_block_based(self.population_number_counter)
                image = self.GA_weight_object.apply_weight_block_pattern_to_grid(amplitudes)
                self.GA_weight_object.input_weights(self.population_number_counter - 1, self.ccd_data)
            else: 
                self.weights_pressed = False  
                image = np.zeros((self.SLM.SLMwidth, self.SLM.SLMheight))
                self.population_number_counter = 0
                self.GA_weight_object.weights[-1, -1] = np.nanmax(self.GA_weight_object.weights)
                self.GA_weight_object.weights[-1, -2] = np.nanmax(self.GA_weight_object.weights)
                normalised_weights = np.abs(self.GA_weight_object.weights-np.nanmax(self.GA_weight_object.weights))
                plt.imshow(normalised_weights)
                plt.colorbar()
                plt.show()
                normalised_weights = (normalised_weights/np.max(normalised_weights))**2
                plt.imshow(normalised_weights)
                plt.colorbar()
                # plt.xlim(0, 13)
                # plt.ylim(0, 11)
                plt.show()
                np.save('./settings/GA_weights', normalised_weights)

            SLMgrating = image
            self.SLM.SLMdisp=PIL.Image.fromarray(SLMgrating)
            self.population_number_counter+=1
            

        ########## Genetic Algorithm
        elif self.GA_GO == True:
            # time.sleep(0.5)
            
            # set the goal using the initial CCD data
            if self.generation_number_counter == 0 and self.population_number_counter == 0:
                # set the threshold using the inital data and creating a cap
                goal = np.clip(self.ccd_data, 0, 120)
                self.GA_object.goal_image = goal
                print(self.GA_object.calculate_fitness(self.ccd_data))
                self.initialtime = int(round(time.time() * 1000))
                # self.weights = self.GA_object.tile_weights()
            self.count +=1
            self.time = int(round(time.time() * 1000)) - self.initialtime
            # print(f' CCD {self.count}, time :{self.time}')
            # print(f' gen num:{self.generation_number_counter}, pop num:{self.population_number_counter}')
            # generation loop
            if self.population_number_counter == 0:
                pass
            else:
                self.GA_object.fitness_of_population[self.population_number_counter - 1] = self.GA_object.calculate_fitness(self.ccd_data)
            # print(self.GA_object.calculate_fitness(self.ccd_data))
            if self.generation_number_counter ==0:
                # self.GA_population = self.GA_object.num_blocks_x * self.GA_object.num_blocks_y
                # creates initial population in the first generation from randomised blocks
                amplitudes = self.GA_object.initialize_individual_block_based(self.population_number_counter)*self.GA_object.tiled_weights
                # image = self.GA_object.apply_block_pattern_to_grid(amplitudes)
                image = self.GA_object.apply_block_pattern_to_grid(gaussian_filter(amplitudes,sigma=1))
                self.GA_object.amplitudes[self.population_number_counter, :, :] = amplitudes
                self.GA_object.population_of_generation[self.population_number_counter, :, :] = image
                # the fitness is from the previous iteration becasue this new one hasn't updated yet
                

            # if it's not the first generation then the data is taken from the parents by ranking and splicing them
            # to work on - the amplitudes should be all thats kept because thats all that matters - they can then be tiled with the underlying macroblock
            elif self.generation_number_counter > 0 and self.generation_number_counter < self.GA_generation:
                    # parent1, parent2 = random.sample(self.GA_object.parents, 2)
                    # amplitudes = self.GA_object.mutate_amplitudes(amplitudes)
                    indices = random.sample(range(self.GA_num_parents), 2)
                    parent1 = self.GA_object.parents[indices[0], :, :]
                    parent2 = self.GA_object.parents[indices[1], :, :]
                    child = self.GA_object.smooth_crossover(parent1, parent2)
                    child = self.GA_object.smooth_mutate(child)
                    child = gaussian_filter(child, sigma=1)

                    self.GA_object.amplitudes[self.population_number_counter, :, ] = child*self.GA_object.tiled_weights
                    image = self.GA_object.apply_block_pattern_to_grid(child)
                    self.GA_object.population_of_generation[self.population_number_counter, :, :] = image
            # if you're at the end of the number of generations then reset everything
            else:
                self.GA_GO = False
                self.generation_number_counter = 0
                self.population_number_counter = 0
                self.delay = 100

            # set the current image to the SLM so the CCD can be measured in the next loop
            SLMgrating = self.GA_object.population_of_generation[self.population_number_counter, :, :]
            self.SLM.SLMdisp=PIL.Image.fromarray(SLMgrating)
            # if self.generation_number_counter == 5:
            #     self.GA_object.mutation_rate = self.GA_object.mutation_rate/2
            #     self.GA_object.mutation_strength = self.GA_object.mutation_strength/2


            # keep increasing the number of the population until you hit the limit for the generation. then it will reset and increase the generation number
            if self.population_number_counter < self.GA_population-2:
                self.population_number_counter +=1
            
            # at the end of the generation, select the parents for the next generation    
            else:
                # need to select the best parents
                print(np.mean(self.GA_object.fitness_of_population))
                self.GA_object.select_parents()
                # resest the population so it can be filled with the next generation
                self.GA_object.population_of_generation = np.zeros((self.GA_population, self.SLM.SLMwidth, self.SLM.SLMheight))
                self.GA_object.amplitudes = np.zeros((self.GA_object.population_size, self.GA_object.num_blocks_x, self.GA_object.num_blocks_y))
                self.GA_object.fitness_of_population = np.zeros((self.GA_population, 1))
                self.population_number_counter =0  
                self.generation_number_counter +=1               

        ######### normal mode of operations
        else:
            SLMgrating = np.asarray(self.SLM.SLMdisp)

        if self.SLM.SLMimage[0][0] != None:
            check = np.array_equal(self.SLM.SLMimage, SLMgrating)
            if check != True:
                self.SLM.SLMimage = SLMgrating

                self.SLMgrating = cv2.resize(np.array(SLMgrating), dsize=(int(self.Monitors.SLMdim[0]*self.scale_percent/100), int(self.Monitors.SLMdim[1]*self.scale_percent/100)))
                self.SLMgrating = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.SLMgrating))
                self.SLM_image_widget.photo = self.SLMgrating
                self.SLM_image_widget.config(image=self.SLMgrating)
        
        if self.SLM.SLMpreview[0][0] != None:
            check2 = np.array_equal(self.SLM.SLMpreview, np.asarray(self.SLM.browseImg))
            if check2 != True:
                self.SLMbrowse = cv2.resize(np.asarray(self.SLM.browseImg), dsize=(int(self.Monitors.SLMdim[0]*self.scale_percent/100), int(self.Monitors.SLMdim[1]*self.scale_percent/100)))
                self.SLMbrowse = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.SLMbrowse))
                self.SLM_preview_widget.photo = self.SLMbrowse
                self.SLM_preview_widget.config(image=self.SLMbrowse)

        ############# End of flattening
        image = self.ccd_data
        cx, cy, dx, dy, phi = lbs.beam_size(image)
        detected_circle = np.uint16((cx,cy,(dx/3+dy/3)/2,phi))

        # Live lineout plotting


        if self.lineout_toggle:
            self.clearCanvas = False
            try:
                data_y = self.ccd_data[int(cy),:]
                data_x = self.ccd_data[:, int(cx)]
                x = np.arange(len(data_y))
                y = np.arange(len(data_x))

                self.ax.clear()
                self.ax.plot(x,data_y, color = "green")
                self.ax.plot(y,data_x, color = "red")
                self.ax.plot(x, self.GA_object.goal_image[int(cy),:])

                try:
                    if np.amax(self.SLM.SLMimage) != 0.0:
                        gratingArrayRescaled = cv2.resize(SLMgrating, dsize=(int(self.ccd_data.shape[1]*self.scale_percent/100), int(self.ccd_data.shape[0]*self.scale_percent/100)), interpolation=cv2.INTER_CUBIC)
                        SLMrescaledwidth, SLMrescaledheight = gratingArrayRescaled.shape
                        ySLM = gratingArrayRescaled[int(SLMrescaledwidth/2),:]
                        # ySLM = gratingArray[int(self.SLMheight/2),:]
                        self.ax.plot(x,ySLM, color="red")
                    else:
                        # if self.clearCanvas != False:
                        self.clearCanvas = False

                except Exception as error:
                    # print(error)
                    pass

                try:
                    goalArray = cv2.resize(goalArray, dsize=(int(self.ccd_data.shape[1]*self.scale_percent/100), int(self.ccd_data.shape[0]*self.scale_percent/100)), interpolation=cv2.INTER_CUBIC)
                    yGoal = goalArray[int(cy),:]
                    self.ax.plot(x,yGoal, color="black")
                except Exception as error:
                    pass
                self.ax.set_ylim([0,260])
                self.ax.set_xlabel("Position (x)")
                self.ax.set_ylabel("Pixel Intensity (0-255)")
                self.ax.set_title("Center Horizontal Lineout of CCD")
                self.canvas.draw()
            except Exception as error:
                print(error)
        else:
            if self.clearCanvas == False:
                self.ax.clear()
                self.canvas.draw()
                # print("CLEAR")
                self.clearCanvas = True

        # Circle detection

        if self.circle_toggle:
            try:
                cv2.circle(image, (detected_circle[0],detected_circle[1]), detected_circle[2], 255, 1)
                cv2.circle(image, (detected_circle[0],detected_circle[1]), 1, 255, 2)
            except Exception as error:
                print(error)


        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.ccd_data_gui))
        self.ccd_image_widget.config(image=self.photo)
        self.ccd_image_widget.photo = self.photo

        self.window.after(self.delay, self.update)
        time2 = time.time()
        # print(time2-time1)






