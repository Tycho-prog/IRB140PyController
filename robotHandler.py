import socket
import time
from console import console_class
import threading
import Kalibrera
#from robotController import robotController

    ## TODO ##
    ##  Lägg till multithreading för denna klassen
    ##  Lägg till hantering för offset
    ##  
    ##------##

class robotHandler():
    def __init__(self,console:console_class,robotFrontend) -> None:
        self.robotControls = robotFrontend
        self.console = console
        ## SOCKET ##
        self.simulationIP = "127.0.0.1" 
        self.actualIP = "192.168.125.1"
        self.usedIP = ''
        self.portNmbr = 4000
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.settimeout(10000)
        ##--------##
        
        ## KOMMUNIKATION ##
        self.rbtMsg = ''
        self.msg = ''
        ##--------##

        ## FÖR UI ##
        self.msgToFilter = ["xpos","ypos","zpos","xneg","yneg","zneg","ReadyForInput"]
        self.gripBool = False
        self.measuringBool = None
        self.connected = False
        self.keyboardMode = False
        self.outOfReachBool = False
        ##--------##

    def connectToRobot(self,simulation)->bool:
        if simulation:
            self.usedIP = self.simulationIP
        else:
            self.usedIP = self.actualIP
        
        self.console.appendEntry('System: Connecting...')
        try:
            self.client.connect((self.usedIP,4000))
            rbtMsg = self.client.recv(1024).decode()

            if rbtMsg == "Connection established":
                self.console.appendEntry(f'IRB140: {rbtMsg}. Waiting for instructions...')
                self.connected = True
                return True
            return False
            
        except Exception as e:
            self.console.appendEntry("System: Connect to robot failed: "+str(e))
            print("ConnectToRobot failed: ",e)
            return False
        
    def waitForReply(self):
        while rbtMsg != "Done":
            rbtMsg = self.client.recv(1024).decode()
            time.sleep(0.1)
        return rbtMsg

    def getReply(self):
        return self.client.recv(1024).decode()
    
    def matchReply(self,response):
        match response:
            case "Out of reach":
                self.robotControls.outOfreachLabel.configure(fg_color="red")
                self.msgToFilter.append("Out of reach")       

            case "Entering keyboard mode":
                self.robotControls.keyboardModeActiveRobot = True
                self.robotControls.keyboardModeActiveLabel.configure(fg_color="green")

            case "ReadyForInput":
                self.outOfReachBool = False
                if "Out of reach" in self.msgToFilter:
                    try:
                        self.msgToFilter.remove("Out of reach")
                    except:
                        pass

            case "Finished keyboard movement":
                self.robotControls.keyboardModeActiveLabel.configure(fg_color="green")

            case "Offset":
                self.robotControls.measuringLabel.configure(fg_color="green")
                t1 = threading.Thread(target=self.threadedMeasure)
                t1.start()

            case "gripActive":
                self.robotControls.gripActiveLabel.configure(fg_color="green")

            case "gripInactive":
                self.robotControls.gripActiveLabel.configure(fg_color="grey")

    def threadedMeasure(self):
        returnedValues = Kalibrera.defineObject(200,230,120,300)
        self.console.appendEntry("System: Försöker justera roboten "+str(returnedValues[0]-150))
        self.sendMsg(str(returnedValues[0]-150))

    
    def sendMsg(self,msg:str):
        if msg not in self.msgToFilter:
            self.console.appendEntry("System: Attempting to send: "+msg)
        try:
            self.client.send(msg.encode())
            response = str(self.client.recv(1024).decode())
            self.matchReply(response)
            if response not in self.msgToFilter:
                self.console.appendEntry("IRB-140: "+response)
        except Exception as e:
            self.console.appendEntry(f'System: {str(e)}')


















            # case "ReadyNextMeasurement":
            #     #KALLA PÅ MÄTNING#
            #     self.robotControls.measuringLabel.configure(fg_color="green")
            #     self.sendMsg("DONE")
            #     ## NÄR MEASURE ÄR KLAR ##
            #     self.robotControls.measuringLabel.configure(fg_color="grey")



        ## TIDIGARE ANVÄNT FÖR ATT KOMMUNICERA MED ROBOTEN ##

    # def temp(self):#client.connect(('192.168.125.1',4000)) #Anslutning till faktiska roboten

    #     if rbtMsg == "Connection established":
    #         #Socket successfully created
    #         print("Tog emot: "+rbtMsg+" från roboten\n")
    #         msg = input(self.menuString)
    #         while str(msg) != "3":
    #             match msg:
    #                 case "1":
    #                     self.client.send('getPos'.encode())
    #                     print("\nTog emot...: '"+self.getReply()+"' från roboten\n")
    #                     msg = input(self.menuString)
                    

    #                 case "3":
    #                     self.client.send('Exit'.encode())
    #                     print("avslutar programmet...")
    #                     exit()

    #         pass



# client.send('Move'.encode())
# print(client.recv(1024).decode())
# client.send('-20'.encode())




