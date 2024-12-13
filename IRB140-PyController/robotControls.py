import customtkinter as ctk
from robotHandler import robotHandler
from gui_superclass import ctk_gui_element
from console import console_class

class robotController(ctk_gui_element):
    def __init__(self, master:ctk.CTkFrame, rowId:int, colId:int,width:int,height:int,console:console_class) -> None:
        super().__init__(master, rowId, colId,width,height)
        self.commands = ["getPos","Change increment","Grip","StartKeyboardMovement","Home","moveToPickup"]
        self.createWindow()
        self.buttons:ctk.CTkButton = []
        self.console = console
        self.createInputs()
        self.keyboardModeActiveRobot = False
        self.robot = robotHandler(console,self)

    ## FUNKTIONER ##
    def connectFunc(self):
        connectionStatus = self.robot.connectToRobot(self.simSwitch.get() == 1)
        if connectionStatus:
            self.connectToRobotButton.configure(fg_color="green")
            self.connectToRobotButton.configure(text="Connected")
        else:
            self.connectToRobotButton.configure(fg_color=['#3B8ED0', '#1F6AA5'])

    def exitFunc(self):
        exit()

    def movementEvent(self,event):
        if self.keyboardSwitch.get():
            pressedKey = event.keysym
            match pressedKey:
                case "Up":
                    self.robot.sendMsg("xpos") #Öka X-värde

                case "Right":
                    self.robot.sendMsg("ypos") #Öka Y-värde

                case "Down":
                    self.robot.sendMsg("xneg") #Minska X-värde

                case "Left":
                    self.robot.sendMsg("yneg")#Minska Y-värde

                case "0":
                    self.robot.sendMsg("zpos") #Öka z-värde

                case "9":
                    self.robot.sendMsg("zneg") # Minska z-värde
    
    def toggleNavigation(self,activateBool:bool):
        if activateBool:
            for button,buttonVal in self.buttons:
                button.configure(state="default")
        else:
            for button,buttonVal in self.buttons:
                button.configure(state="default")

    def toggleKeyboardMode(self):
        if self.keyboardSwitch.get() == 1 and self.keyboardModeActiveRobot:
            self.keyboardModeActiveLabel.configure(fg_color="green")
            self.toggleNavigation(True)
        
        elif self.keyboardSwitch.get() == 1 and not self.keyboardModeActiveRobot:
            self.console.appendEntry("System: Robot not in keyboardmode yet...")

        else:
            self.keyboardModeActiveLabel.configure(fg_color="grey")
            self.toggleNavigation(False)

    def comboBoxFunc(self):
        entry = str(self.msgCombobox.get()).strip() #get hämtar texten i input, strip tar bort extra mellanslag
        self.msgCombobox.set("Input or select command")
        if self.robot.connected and entry != "":
            self.robot.sendMsg(entry)
        else:
            self.console.appendEntry("System: Not connected or invalid input")

    ##                    ##
    ##--------------------##
    ##  SKAPA UI-ELEMENT  ##
    def createButton(self,rowId,colId,masterFrame,textVar):
        inputButton = ctk.CTkButton(
            masterFrame,
            width=50,
            height=50,
            text=textVar,
            state="disabled",
            font=("Arial",16)
        )
        inputButton.grid(row=rowId,column=colId,padx=5,pady=5)
        self.buttons.append((inputButton,textVar)) 
        
        return inputButton
    
    def createInputs(self):
        self.xPosButton = self.createButton(0,1,self.inputButtonFrame,"+x") #row,col,frame,buttonText
        self.xNegButton = self.createButton(1,1,self.inputButtonFrame,"-x")
        self.yPosButton = self.createButton(1,2,self.inputButtonFrame,"+y")
        self.yNegButton = self.createButton(1,0,self.inputButtonFrame,"-y")
        ## Z-AXIS ##
        self.zPosButton = self.createButton(1,0,self.zAxisButtonFrame,"+z")
        self.zNegButton = self.createButton(2,0,self.zAxisButtonFrame,"-z")

        for button,buttonText in self.buttons:
            if buttonText[0] == "+":
                button.configure(command=lambda e = buttonText: self.robot.sendMsg(e[1]+"pos"))
            else:
                button.configure(command=lambda e= buttonText: self.robot.sendMsg(e[1]+"neg"))

    def createWindow(self):
        self.mainControllerFrame = ctk.CTkFrame(
            self.master,
            width=self.width,
            height=self.height,
        )
        self.mainControllerFrame.grid(row=self.rowId,column=self.colId,padx=5,pady=5,sticky='nsew',rowspan=2)
        self.mainControllerFrame.grid_rowconfigure(1,weight=10)

        self.mainControllerLabel = ctk.CTkLabel(
            self.mainControllerFrame,
            width=self.width,
            height=30,
            text="IRB-140 Controls",
            justify="center"
        )
        self.mainControllerLabel.grid(row=0,padx=5,pady=5,sticky='ew',columnspan=2)

        self.inputControlsFrame = ctk.CTkFrame(
            self.mainControllerFrame,
            width=self.width,
            height=100,
        )
        self.inputControlsFrame.grid(row=1,padx=60,pady=5,sticky='nsew')#,columnspan=2
        self.inputControlsFrame.columnconfigure((0,1),weight=1)

        self.infoLabelsFrame = ctk.CTkFrame(
            self.inputControlsFrame,
            width=120,
            height=40,
        )
        self.infoLabelsFrame.pack(padx=5,pady=5)

        self.indicatorsTitleLabel = ctk.CTkLabel(
            self.infoLabelsFrame,
            height=40,
            text="Indicators",
            justify='center'
        )
        self.indicatorsTitleLabel.grid(row=0,column=0,padx=5,pady=5,columnspan=2)

        self.outOfreachLabel = ctk.CTkLabel(
            self.infoLabelsFrame,
            width=125,
            height=30,
            fg_color="grey",
            text="Out of Reach",
            corner_radius=5
        )
        self.outOfreachLabel.grid(row=1,column=0,padx=5,pady=5,sticky='nsew')

        self.keyboardModeActiveLabel = ctk.CTkLabel(
            self.infoLabelsFrame,
            width=125,
            height=30,
            fg_color="grey",
            text="Keyboard Mode",
            corner_radius=5
        )
        self.keyboardModeActiveLabel.grid(row=1,column=1,padx=5,pady=5,sticky='nsew')

        self.gripActiveLabel = ctk.CTkLabel(
            self.infoLabelsFrame,
            width=125,
            height=30,
            fg_color="grey",
            text="Grip Active",
            corner_radius=5
        )
        self.gripActiveLabel.grid(row=2,column=0,padx=5,pady=5,sticky='nsew')

        self.measuringLabel = ctk.CTkLabel(
            self.infoLabelsFrame,
            width=125,
            height=30,
            fg_color="grey",
            text="Measuring",
            corner_radius=5
        )
        self.measuringLabel.grid(row=2,column=1,padx=5,pady=5,sticky='nsew')
        
        self.subFrameInput = ctk.CTkFrame( ## För att hålla xy-frame & Z-frame ##
            self.inputControlsFrame,
            width=250,
            height=100,
        )
        self.subFrameInput.pack(side=ctk.BOTTOM,padx=5,pady=5)

        self.inputButtonFrame = ctk.CTkFrame( ##För att hålla xy-buttons
            self.subFrameInput,
            width=250,
            height=100,
            fg_color="transparent"
        )
        self.inputButtonFrame.grid(row=1,column=0,padx=5,pady=5,sticky='nsew')
        self.inputButtonFrame.columnconfigure((0,1),weight=1)
        self.inputButtonFrame.rowconfigure((0,1,2),weight=1)

        self.zAxisButtonFrame = ctk.CTkFrame( ## För att hålla z-buttons ##
            self.subFrameInput,
            width=250,
            height=100,
            fg_color="transparent"
        )
        self.zAxisButtonFrame.grid(row=1,column=2,padx=5,pady=5,sticky='nsew')
        self.zAxisButtonFrame.columnconfigure((0,1),weight=1)
        self.zAxisButtonFrame.rowconfigure((0,1,2),weight=1)

        self.commandButtonFrame = ctk.CTkFrame(
            self.mainControllerFrame,
            width=self.width,
            height=100,
            fg_color="transparent"
        )
        self.commandButtonFrame.grid(row=3,padx=20,pady=5,sticky='ew',columnspan=2)

        self.commandFrame = ctk.CTkFrame(
            self.commandButtonFrame,
            width=300,
            height=60
        )
        self.commandFrame.grid(row=0,column=0,sticky='nsew',padx=5,pady=5)

        self.msgCombobox = ctk.CTkComboBox(
            self.commandFrame,
            width=200,
            height=40,
            corner_radius=5,
            values = self.commands,
        )
        self.msgCombobox.grid(row=0,padx=5,pady=5)
        self.msgCombobox.set("Input or select command")

        self.sendMsgButton = ctk.CTkButton(
            self.commandFrame,
            width=200,
            height=40,
            text="Send",
            command=self.comboBoxFunc
        )
        self.sendMsgButton.grid(row=1,padx=5,pady=5)

        ##--------------------##

        self.buttonFrame = ctk.CTkFrame(
            self.commandButtonFrame,
            width=100,
            height=self.height
        )
        self.buttonFrame.grid(row=0,column=1,padx=5,pady=5,sticky='nsew')

        self.connectToRobotButton = ctk.CTkButton(
            self.buttonFrame,
            width=100,
            height=40,
            text = "Connect to robot",
            command=self.connectFunc
        )
        self.connectToRobotButton.grid(row=0,padx=2,pady=5)

        self.simSwitch = ctk.CTkSwitch(
            self.buttonFrame,
            height=40,
            text='Simulation'
        )
        self.simSwitch.grid(row=2,padx=20,pady=2,sticky='ew')

        self.keyboardSwitch = ctk.CTkSwitch(
            self.buttonFrame,
            height=40,
            text='Keyboard',
            command=self.toggleKeyboardMode
        )
        self.keyboardSwitch.grid(row=3,padx=20,pady=2,sticky='ew')
        
        self.exitButton = ctk.CTkButton(
            self.buttonFrame,
            width=100,
            height=40,
            text="Exit",
            command=self.exitFunc
        )
        self.exitButton.grid(row=4,column=0,padx=2,pady=5)
