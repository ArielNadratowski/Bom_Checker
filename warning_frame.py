import tkinter as tk

class WarningFrame:
    def __init__(self, position, padx_ = 10, pady_ = 10):

        # make frame to display the warnings
        self.warning_frame = tk.Frame()
        self.warning_frame.pack(side = position, padx = padx_, pady = pady_)




            