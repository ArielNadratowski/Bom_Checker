import tkinter as tk
from bom_upload_window import BomUploadWindow

class UploadFrame:
    def __init__(self, position, padx_ = 10, pady_ = 10):
         # set up frame
        upload_button_frame = tk.Frame()
        upload_button_frame.pack(side = position, padx = padx_, pady = pady_)

        # place to store bom objects
        self.boms = []
        
        # upload bom button
        upload_bom = tk.Button(upload_button_frame, text = 'UPLOAD BOM')
        upload_bom.bind("<Button>", 
                        lambda e: BomUploadWindow(self.boms))
        upload_bom.pack(side = 'top')

        # show uploaded boms
        ## make a function that adds a label when a bom is uploaded with its name or something like that
