import tkinter as tk
from bom_checker_code.bom_upload_window import BomUploadWindow

""" Holds BOM objects as well as shows the checkboxes for each BOM """
class UploadFrame:
    def __init__(self, main_window, padx = 10, pady = 10):
        self.main_window = main_window
        self.boms = []
        self.upload_button_frame = None
        self.boms_uploaded_frame = None

        self._set_up_window(padx, pady)
        self._set_up_boms_uploaded_frame(padx, pady)
        self._set_up_upload_bom_button()
    
    def _set_up_window(self, padx, pady):
        self.upload_button_frame = tk.Frame(self.main_window)
        self.upload_button_frame.grid(column = 0, row = 1, padx = padx, pady = pady)

    def _set_up_boms_uploaded_frame(self, padx, pady):
        self.boms_uploaded_frame = tk.Frame(self.main_window)
        self.boms_uploaded_frame.grid(column = 0, row = 2, padx = padx, pady = pady)

    def _set_up_upload_bom_button(self):
        upload_bom = tk.Button(self.upload_button_frame, text = 'UPLOAD BOM')
        upload_bom.bind("<Button>", 
                        lambda e: BomUploadWindow(self.main_window))
        upload_bom.pack(side = 'top')








        

