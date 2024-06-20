import tkinter as tk
from bom_upload_window import BomUploadWindow

class UploadFrame:
    def __init__(self, main_window, position, padx_ = 10, pady_ = 10):
         # set up frame
        upload_button_frame = tk.Frame()
        upload_button_frame.pack(side = position, padx = padx_, pady = pady_)

        # place to store bom objects
        self.boms = []

        # set up frame to show uploaded boms
        self.boms_uploaded_frame = tk.Frame()
        self.boms_uploaded_frame.pack(side = position, padx = padx_, pady = pady_)
        
        # upload bom button
        upload_bom = tk.Button(upload_button_frame, text = 'UPLOAD BOM')
        upload_bom.bind("<Button>", 
                        lambda e: BomUploadWindow(self.boms, self.boms_uploaded_frame, main_window))
        upload_bom.pack(side = position)



        

