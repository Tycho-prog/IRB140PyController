from gui_superclass import ctk_gui_element
from logHandler import logHandler
import customtkinter as ctk
from datetime import datetime

class console_class(ctk_gui_element):
    def __init__(self, master:ctk.CTkFrame, rowId:int, colId:int,width:int,height:int,log:logHandler):
        super().__init__(master, rowId, colId,width,height)
        self.log = log
        self.createLogElement()
        self.labels = []
        

    def createLogElement(self):
        self.console_frame = ctk.CTkFrame(
            self.master,
            width=self.width,
            height= self.height,
        )
        self.console_frame.grid(row=self.rowId,column=self.colId,padx=5,pady=5)

        self.infoFrame = ctk.CTkFrame(
            self.console_frame,
            width=self.width,
            height=40,
            fg_color="transparent"
        )
        self.infoFrame.grid(row=0,padx=2,pady=2,sticky='ew')

        self.infoLabel = ctk.CTkLabel(
            self.infoFrame,
            height=30,
            text="Console output",
            justify="center"
        )
        self.infoLabel.pack(side=ctk.TOP,padx=2,pady=2,fill='both')
        

        self.buttonFrame = ctk.CTkFrame(
            self.console_frame,
            width=140,
            height=35,
            fg_color="transparent"
        )
        self.buttonFrame.grid(row=2,pady=2,padx=2)

        self.clearButton = ctk.CTkButton(
            #self.console_frame,
            self.buttonFrame,
            height=30,
            width=60,
            text="Clear",
            command=self.clearEntries
        )
        #self.clearButton.grid(row=2,column=0,padx=2,pady=5)
        self.clearButton.pack(side=ctk.LEFT,padx=5,pady=2)

        self.openLogButton = ctk.CTkButton(
            #self.console_frame,
            self.buttonFrame,
            height=30,
            width=60,
            text="Open log",
            command=self.log.openLog
        )
        #self.openLogButton.grid(row=2,column=1,padx=2,pady=5)
        self.openLogButton.pack(side=ctk.RIGHT,padx=5,pady=2)
        
        self.createScFrame()


    def createScFrame(self):
        self.entryScFrame = ctk.CTkScrollableFrame(
            self.console_frame,
            height=self.height,
            width=self.width
        )
        self.entryScFrame.grid(row=1,padx=1,pady=2)


    def appendEntry(self,entry:str):
        entryToAppend = entry
        if entry is not None or not "":
            print("entry var ",len(entry))
            limit = 55
            if len(entry) > limit:
                entryToAppend = f"{entry[0:limit]}..."
            self.labelFrameToAppend = ctk.CTkFrame(
                self.entryScFrame,
                height=40
            )
            self.labelFrameToAppend.pack(side=ctk.TOP,fill='both',pady=2,padx=1)
            
            currentTime = datetime.now()
            self.labelToAppend = ctk.CTkLabel(
                self.labelFrameToAppend,
                text=f"{currentTime.strftime('%H:%M:%S'):<10}"+f"{entryToAppend}",
                font=('Arial',12),
                justify="left"
            )
            self.labelToAppend.pack(side=ctk.LEFT,fill='both')
            self.labels.append([self.labelToAppend,self.labelFrameToAppend])
            self.log.appendToLog(entry)


    def clearEntries(self):
        for label,frame in self.labels:
            label.destroy()
            frame.destroy()

        self.labels.clear()
        self.entryScFrame.grid_forget()
        self.createScFrame()
        
        self.log.clearLog()
        self.appendEntry("Console & log cleared")

    


