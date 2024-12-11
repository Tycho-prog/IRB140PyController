import os
import glob
from datetime import datetime

class logHandler():
    def __init__(self) -> None:
        self.path = f"{os.path.expanduser('~')}\\robotLog.txt"
        self.checkIfFileExists()

    def checkIfFileExists(self):
        if glob.glob(self.path) == []:
            self.createFile()
            return False
        else:
            self.clearLog()
            return True

    def createFile(self):
        try:
            test = open(self.path,"w+",encoding="utf8")
            lines = list()
            currentTime = datetime.now()
            lines.append(f"{currentTime.strftime('%H:%M:%S'):<10}"+f"Log file created")
            lines.append("\n")
            test.writelines(lines)
            test.close()
            print('Log file was successfully created')
        except Exception as e:
            print('Something went wrong while trying to create the log file', e)

    def appendToLog(self,entry:str):
        if entry is not None and not "":   
            try:
                lines = open(self.path,"r",encoding="utf8").readlines()
                currentTime = datetime.now()
                lines.append(f"{currentTime.strftime('%H:%M:%S'):<10}"+f"{entry}")
                lines.append("\n")
                txt = open(self.path,'w',encoding="utf8")
                txt.writelines(lines)
                txt.close()
            except:
                pass

    def clearLog(self):
        txt = open(self.path,'w',encoding="utf8")
        txt.close()


    def openLog(self):
        try:
            os.startfile(self.path)
        except:
            pass