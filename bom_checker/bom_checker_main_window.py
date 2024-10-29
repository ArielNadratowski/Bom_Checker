import tkinter as tk
from bom_checker.upload_frame import UploadFrame
from bom_checker.compare_search_frame import CompareSearchFrame
from bom_checker.warning_frame import WarningFrame
from bom_checker.highlight_errors_frame import HighlightErrorsFrame

""" Main window that contains everything """
class BomCheckerMainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1700x800')
        self.title('Bom Checker')
        self.test_name = None

        self._set_up_window()

        self.upload_frame = UploadFrame(self)
        self.highlight_errors_frame = HighlightErrorsFrame(self)
        self.warning_frame = WarningFrame(self)  
        self.compare_search_frame = CompareSearchFrame(self)    

    """ Set up main window and title """
    def _set_up_window(self):
        self.grid_columnconfigure(0, weight=1) # center everything
        self.test_name = tk.Label(self, text = 'Bom Checker :)', font = ('Segoe UI', 15, 'bold'))
        self.test_name.grid(column = 0, row = 0)
        self.resizable(width=True, height=True)

          

        



