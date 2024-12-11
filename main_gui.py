import customtkinter as ctk
import threading
from console import console_class
from camera_window import camera_window
from logHandler import logHandler
#from robotHandler import robotHandler
from robotControls import robotController

main_window = ctk.CTk()
main_window.bind('<Escape>',lambda e: main_window.quit())
main_window.title('IRB140-PyController')
main_window.resizable(False,False)
main_window.geometry("870x720")

log = logHandler()
console = console_class(main_window,1,0,400,300,log) #frame,row,col,width,height,log
#robotBackend = robotHandler(console)
robotFrontend = robotController(main_window,0,1,400,400,console)
camWindow = camera_window(main_window,0,0,400,450,log,console)



main_window.bind("<Up>",lambda e: robotFrontend.movementEvent(e))
main_window.bind("<Left>",lambda e: robotFrontend.movementEvent(e))
main_window.bind("<Right>",lambda e: robotFrontend.movementEvent(e))
main_window.bind("<Down>",lambda e: robotFrontend.movementEvent(e))
main_window.bind("9",lambda e: robotFrontend.movementEvent(e))
main_window.bind("0",lambda e: robotFrontend.movementEvent(e))

main_window.bind("<Return>",lambda e: robotFrontend.entryBoxFunc())


main_window.mainloop()