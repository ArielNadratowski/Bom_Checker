# Bom Checker main window

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def main():

    BomCheckerMainWindow().mainloop() 



def compareBoms(event = None):
    print("comparing boms")

class BomCheckerMainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # set up main window size and title
        self.geometry("1500x800")
        self.title("Bom Checker")
        self.test_name = tk.Label(self, text = "Bom Checker :)")
        self.test_name.pack(side = "top")

        # set up frame for buttons you interact with
        input_frame = tk.Frame(self, width = 1400, height = 200)
        input_frame.pack(side = "top")

        self.bomA_label_value = tk.StringVar(input_frame, "Please upload file")
        self.bomA_button = tk.Button(input_frame, text = "upload BOM A", command = self.uploadFileA)
        self.bomA_label = tk.Label(input_frame, textvariable=self.bomA_label_value)
        self.bomA_button.grid(row = 0, column = 0)
        self.bomA_label.grid(row = 0, column = 1)

        self.bomB_label_value = tk.StringVar(input_frame, "Please upload file")
        self.bomB_button = tk.Button(input_frame, text = "upload BOM B", command = self.uploadFileB)
        self.bomB_label = tk.Label(input_frame, textvariable=self.bomB_label_value)   
        self.bomB_button.grid(row = 1, column = 0)
        self.bomB_label.grid(row = 1, column = 1)

        self.compare_button = tk.Button(input_frame, text = "COMPARE BOMs", command = compareBoms)
        self.compare_button.grid(row = 3, column = 0, columnspan = 2)

    def uploadFileA(self, *_):
        filename = filedialog.askopenfilename()
        print('Selected:', filename)
        self.bomA_label_value.set(filename)

    def uploadFileB(self, *_):
        filename = filedialog.askopenfilename()
        print('Selected:', filename)
        self.bomB_label_value.set(filename)


        warnings_frame = tk.Frame(self, background = "grey", width = 1400, height = 200)
        warnings_frame.pack(side = "top")


main()