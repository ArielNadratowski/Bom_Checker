import tkinter as tk
from upload_frame import UploadFrame
from compare_search_frame import CompareSearchFrame
from warning_frame import WarningFrame
from highlight_errors_frame import HighlightErrorsFrame

""" Main window that contains everything """
class BomCheckerMainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.set_up_window()
        self.upload_frame = UploadFrame(self, 'top')
        self.highlight_errors_frame = HighlightErrorsFrame(self)
        self.warning_frame = WarningFrame(self)  
        self.compare_search_frame = CompareSearchFrame(self, self.upload_frame, self.highlight_errors_frame, self.warning_frame)    

    """ Set up main window and title """
    def set_up_window(self):
        self.geometry('1700x800')
        self.title('Bom Checker')
        self.grid_columnconfigure(0, weight=1) # center everything
        
        self.test_name = tk.Label(self, text = 'Bom Checker :)', font = ('Segoe UI', 15, 'bold'))
        self.test_name.grid(column = 0, row = 0)
        self.resizable(width=True, height=True)

          

        



