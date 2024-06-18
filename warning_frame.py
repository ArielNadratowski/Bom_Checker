import tkinter as tk

class WarningFrame:
    def __init__(self, position, padx_ = 10, pady_ = 10):

        # make frame to display the warnings
        warnings_frame = tk.Frame()
        warnings_frame.pack(side = position, padx = padx_, pady = pady_)
        warnings_frame.pack_propagate(False)