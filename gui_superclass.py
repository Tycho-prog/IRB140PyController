import customtkinter as ctk
class ctk_gui_element():
    def __init__(self,master,rowId,colId,width,height):
        self.master:ctk.CTkFrame = master
        self.rowId:int = rowId
        self.colId:int = colId
        self.width:int = width
        self.height:int = height
        
    