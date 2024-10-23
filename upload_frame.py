import tkinter as tk
from bom_upload_window import BomUploadWindow

""" Holds BOM objects as well as shows the checkboxes for each BOM """
class UploadFrame:
    def __init__(self, main_window, position, padx = 10, pady = 10):
        self.set_up_window(main_window, padx, pady)
        self.boms = []
        self.set_up_boms_uploaded_frame(main_window, padx, pady)
        self.set_up_upload_bom_button(self.upload_button_frame, main_window, position)
    
    def set_up_window(self, main_window, padx, pady):
        self.upload_button_frame = tk.Frame(main_window)
        self.upload_button_frame.grid(column = 0, row = 1, padx = padx, pady = pady)

    def set_up_boms_uploaded_frame(self, main_window, padx, pady):
        self.boms_uploaded_frame = tk.Frame(main_window)
        self.boms_uploaded_frame.grid(column = 0, row = 2, padx = padx, pady = pady)

    def set_up_upload_bom_button(self, upload_button_frame, main_window, position):
        upload_bom = tk.Button(upload_button_frame, text = 'UPLOAD BOM')
        upload_bom.bind("<Button>", 
                        lambda e: BomUploadWindow(self.boms, self.boms_uploaded_frame, main_window))
        upload_bom.pack(side = position)








        

