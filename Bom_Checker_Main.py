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
        input_frame = tk.Frame(self)
        input_frame.pack(side = "top")

        self.bomA_label_value = tk.StringVar(input_frame, "Please upload file")
        bomA_button = tk.Button(input_frame, text = "upload BOM A", command = self.uploadFileA)
        self.bomA_label = tk.Label(input_frame, textvariable=self.bomA_label_value)
        bomA_button.grid(row = 0, column = 0)
        self.bomA_label.grid(row = 0, column = 1, padx = 5, pady = 5)

        self.bomB_label_value = tk.StringVar(input_frame, "Please upload file")
        bomB_button = tk.Button(input_frame, text = "upload BOM B", command = self.uploadFileB)
        self.bomB_label = tk.Label(input_frame, textvariable=self.bomB_label_value)   
        bomB_button.grid(row = 1, column = 0)
        self.bomB_label.grid(row = 1, column = 1, padx = 5, pady = 5)

        compare_button = tk.Button(input_frame, text = "COMPARE BOMs", command = compareBoms)
        compare_button.grid(row = 3, column = 0, columnspan = 2, padx = 10, pady = 10)

        # make frame to display the warnings
        warnings_frame = tk.Frame(self)
        warnings_frame.pack(side = "top", padx = 10, pady = 10)
        warnings_frame.pack_propagate(False)
        
        warnings_row = []
        warnings_list = ["warning1", "warning2", "warning3"]
        for index, value in enumerate(warnings_list):
            warnings_row.append(ttk.Label(warnings_frame, text = value))
            warnings_row[index].grid()

        # display the flagged rows from the BOMs
        




    def uploadFileA(self, *_):
        filename = filedialog.askopenfilename()
        print('Selected:', filename)
        self.bomA_label_value.set(filename)

    def uploadFileB(self, *_):
        filename = filedialog.askopenfilename()
        print('Selected:', filename)
        self.bomB_label_value.set(filename)
        



# https://stackoverflow.com/questions/44798950/how-to-display-a-dataframe-in-tkinter

main()