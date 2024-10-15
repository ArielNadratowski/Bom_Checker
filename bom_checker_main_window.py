import tkinter as tk
from upload_frame import UploadFrame
from compare_search_frame import CompareSearchFrame
from warning_frame import WarningFrame
from highlight_errors_frame import HighlightErrorsFrame

class BomCheckerMainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # set up main window size and title
        self.geometry('1700x800')
        self.title('Bom Checker')
        self.test_name = tk.Label(self, text = 'Bom Checker :)', font = ('Segoe UI', 15, 'bold'))
        self.test_name.pack(side = 'top')
        self.resizable(width=False, height=False) # does funky things when resizing

        # values for setting frames and buttons

        # set up upload frame (contains upload button and uploaded boms visualization)
        self.upload_frame = UploadFrame(self, 'top')

        # set up highlight errors frame (highlights mismatches and other potential errors)
        self.highlight_errors_frame = HighlightErrorsFrame(self, 'bottom')

        # set up warning frame (displays warnings)
        self.warning_frame = WarningFrame('bottom')  

        # set up compare and search frame (contains just the compare and search buttons)
        self.compare_search_frame = CompareSearchFrame(self.upload_frame, self.highlight_errors_frame, self.warning_frame, 'top')      

        



