from gui_superclass import ctk_gui_element
from logHandler import logHandler
import customtkinter as ctk
import cv2
import numpy as np
import threading
import tkinter as tk
from PIL import Image, ImageTk

#import Kalibrera

class camera_window(ctk_gui_element):
    def __init__(self, master:ctk.CTkFrame, rowId:int, colId:int,width:int,height:int,log:logHandler,console):
        self.console = console
        self.cameraVar = ctk.StringVar()
        self.cameraVar.set("Camera disconnected...")
        super().__init__(master, rowId, colId,width,height)
        self.createWindow()

    def createWindow(self):
        self.cameraFrame = ctk.CTkFrame(
            self.master,
            width=self.width,
            height=self.height
        )
        self.cameraFrame.grid(row=self.rowId,column=self.colId,padx=5,pady=5,sticky='nsew')

        self.cameraFeed = ctk.CTkLabel(
            self.cameraFrame,
            height=250,
            width=self.width,
            textvariable=self.cameraVar,
            fg_color="black",
            corner_radius=5
        )
        self.cameraFeed.grid(row=0,padx=5,pady=1,sticky='ew')

        ## KNAPPAR ##
        self.buttonFrame = ctk.CTkFrame(
            self.cameraFrame,
            width=140,
            height=35,
            fg_color="transparent"
        )
        self.buttonFrame.grid(row=1,pady=2,padx=2)
        
        self.startStreamButton = ctk.CTkButton(
            self.buttonFrame,
            height=30,
            width=60,
            text="Start",
            command=self.startLiveStream
        )
        self.startStreamButton.pack(side=ctk.LEFT,padx=5,pady=2)

        self.stopStreamButton = ctk.CTkButton(
            self.buttonFrame,
            height=30,
            width=60,
            text="Stop"
        )
        self.stopStreamButton.pack(side=ctk.RIGHT,padx=5,pady=2)


    def startLiveStream(self): ## för att programmet inte ska frysa under livestream
        self.cameraVar.set("")
        test = Kalibrera.defineObject(200,230,120,300)
        opencv_image = cv2.cvtColor(test[2], cv2.COLOR_BGR2RGBA) 
        captured_image = Image.fromarray(opencv_image) 
        photo_image = ImageTk.PhotoImage(image=captured_image) 
        self.cameraFeed.photo_image = photo_image 
        self.cameraFeed.configure(image=photo_image)
        #self.console.appendEntry("Avståndet var: "+str(test[0]))
        # t1 = threading.Thread(target=self.startFeed)
        # t1.start()
        

    def startFeed(self):
        ## Setup ##
        self.cameraVar.set("")
        self.capture = cv2.VideoCapture(0) # Om 0 inte fungerar, testa 1,2...,10.
        self.open_camera()

    def open_camera(self):
        ret,frame = self.capture.read()

        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
        captured_image = Image.fromarray(opencv_image) 
        photo_image = ImageTk.PhotoImage(image=captured_image) 
        #photo_image = ctk.CTkImage(captured_image)
        self.cameraFeed.photo_image = photo_image 
        self.cameraFeed.configure(image=photo_image) 
        self.cameraFeed.after(10, self.open_camera)
