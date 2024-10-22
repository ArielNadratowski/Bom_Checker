import tkinter as tk
import scrolled_frame

""" Place where warnings are shown """
class WarningFrame:
    def __init__(self, parent, padx_ = 10, pady_ = 10):
        self.warning_frame = scrolled_frame.ScrolledFrame(parent, True)
        self.warning_frame.grid(column = 0, row = 4, sticky = 'EW',padx = padx_, pady = pady_)




            