import tkinter as tk
from bom_upload_window import BomUploadWindow

""" Holds BOM objects as well as shows the checkboxes for each BOM """
class UploadFrame:
    def __init__(self, parent, position, padx_ = 10, pady_ = 10):
        self.set_up_window(parent, padx_, pady_)
        self.boms = []
        self.set_up_boms_uploaded_frame(parent, padx_, pady_)
        self.set_up_upload_bom_button(self.upload_button_frame, parent, position)
    
    def set_up_window(self, parent, padx_, pady_):
        self.upload_button_frame = tk.Frame(parent)
        self.upload_button_frame.grid(column = 0, row = 1, padx = padx_, pady = pady_)

    def set_up_boms_uploaded_frame(self, parent, padx_, pady_):
        self.boms_uploaded_frame = tk.Frame(parent)
        self.boms_uploaded_frame.grid(column = 0, row = 2, padx = padx_, pady = pady_)

    def set_up_upload_bom_button(self, upload_button_frame, parent, position):
        upload_bom = tk.Button(upload_button_frame, text = 'UPLOAD BOM')
        upload_bom.bind("<Button>", 
                        lambda e: BomUploadWindow(self.boms, self.boms_uploaded_frame, parent))
        upload_bom.pack(side = position)








        

