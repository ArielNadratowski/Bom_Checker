# Bom Checker main window

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, font
import pandas as pd

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
        self.test_name = tk.Label(self, text = "Bom Checker :)", font = ("Segoe UI", 15, "bold"))
        self.test_name.pack(side = "top")

        # set up frame for buttons you interact with
        input_frame = tk.Frame(self)
        input_frame.pack(side = "top")

        self.bomA_label_value = tk.StringVar(input_frame, "Please upload file")
        bomA_button = tk.Button(input_frame, text = "upload BOM A", command = self.uploadFileA)
        self.bomA_label = tk.Label(input_frame, textvariable=self.bomA_label_value)
        bomA_button.grid(row = 3, column = 2, padx = 5, pady = (30, 5))
        self.bomA_label.grid(row = 3, column = 3, columnspan = 7, sticky = "W", padx = 5, pady = (30, 5))

        self.bomB_label_value = tk.StringVar(input_frame, "Please upload file")
        bomB_button = tk.Button(input_frame, text = "upload BOM B", command = self.uploadFileB)
        self.bomB_label = tk.Label(input_frame, textvariable=self.bomB_label_value)   
        bomB_button.grid(row = 4, column = 2)
        self.bomB_label.grid(row = 4, column = 3, columnspan = 7, sticky = "W", padx = 5, pady = 5)

        # take input for what columns are what
        instructions = tk.Label(input_frame, text = "Please type the following column names EXACTLY as labeled in their respective BOM file", font = ("Segoe UI", 11, "bold"))
        instructions.grid(row = 0, column = 0, columnspan = 10, sticky = "W", padx = 5, pady = 5)

        descriptionA_input = tk.Text(input_frame, height =1, width = 15)
        descriptionA_label = tk.Label(input_frame, text = "Description BOM A")
        descriptionA_input.grid(row = 1, column = 1, padx = 5, pady = 5)
        descriptionA_label.grid(row = 1, column = 0, padx = 5, pady = 5)

        descriptionB_input = tk.Text(input_frame, height = 1, width = 15)
        descriptionB_label = tk.Label(input_frame, text = "Description BOM B")
        descriptionB_input.grid(row = 2, column = 1, padx = 5, pady = 5)
        descriptionB_label.grid(row = 2, column = 0, padx = 5, pady = 5)

        quantityA_input = tk.Text(input_frame, height = 1, width = 15)
        quantityA_label = tk.Label(input_frame, text = "Quantity BOM A")
        quantityA_input.grid(row = 1, column = 3, padx = 5, pady = 5)
        quantityA_label.grid(row = 1, column = 2, padx = 5, pady = 5)

        quantityB_input = tk.Text(input_frame, height = 1, width = 15)
        quantityB_label = tk.Label(input_frame, text = "Quantity BOM B")
        quantityB_input.grid(row = 2, column = 3, padx = 5, pady = 5)
        quantityB_label.grid(row = 2, column = 2, padx = 5, pady = 5)

        ref_dsgA_input = tk.Text(input_frame, height = 1, width = 15)
        ref_dsgA_label = tk.Label(input_frame, text = "Reference Designator BOM A")
        ref_dsgA_input.grid(row = 1, column = 5, padx = 5, pady = 5)
        ref_dsgA_label.grid(row = 1, column = 4, padx = 5, pady = 5)

        ref_dsgB_input = tk.Text(input_frame, height = 1, width = 15)
        ref_dsgB_label = tk.Label(input_frame, text = "Reference Designator BOM B")
        ref_dsgB_input.grid(row = 2, column = 5, padx = 5, pady = 5)
        ref_dsgB_label.grid(row = 2, column = 4, padx = 5, pady = 5)

        manuA_input = tk.Text(input_frame, height = 1, width = 15)
        manuA_label = tk.Label(input_frame, text = "Manufacturer BOM A")
        manuA_input.grid(row = 1, column = 7, padx = 5, pady = 5)
        manuA_label.grid(row = 1, column = 6, padx = 5, pady = 5)

        manuB_input = tk.Text(input_frame, height = 1, width = 15)
        manuB_label = tk.Label(input_frame, text = "Manufacturer BOM B")
        manuB_input.grid(row = 2, column = 7, padx = 5, pady = 5)
        manuB_label.grid(row = 2, column = 6, padx = 5, pady = 5)
        
        mpnA_input = tk.Text(input_frame, height = 1, width = 15)
        mpnA_label = tk.Label(input_frame, text = "Manufacturer Part Number BOM A")
        mpnA_input.grid(row = 1, column = 9, padx = 5, pady = 5)
        mpnA_label.grid(row = 1, column = 8, padx = 5, pady = 5)

        mpnB_input = tk.Text(input_frame, height = 1, width = 15)
        mpnB_label = tk.Label(input_frame, text = "Manufacturer Part Number BOM B")
        mpnB_input.grid(row = 2, column = 9, padx = 5, pady = 5)
        mpnB_label.grid(row = 2, column = 8, padx = 5, pady = 5)
 
        headerA_input = tk.Text(input_frame, height = 1, width = 10)
        headerA_label = tk.Label(input_frame, text = "Header *Row Number* BOM A")
        headerA_input.grid(row = 3, column = 1, padx = 5, pady = (30, 5))
        headerA_label.grid(row = 3, column = 0, padx = 5, pady = (30, 5))

        headerB_input = tk.Text(input_frame, height = 1, width = 10)
        headerB_label = tk.Label(input_frame, text = "Header *Row Number* BOM B")
        headerB_input.grid(row = 4, column = 1, padx = 5, pady = 5)
        headerB_label.grid(row = 4, column = 0, padx = 5, pady = 5)

        compare_button = tk.Button(input_frame, text = "COMPARE BOMs", command = compareBoms)
        compare_button.grid(row = 7, column = 0, columnspan = 10, padx = 10, pady = 10)

        # make frame to display the warnings
        warnings_frame = tk.Frame(self)
        warnings_frame.pack(side = "top", padx = 10, pady = 10)
        warnings_frame.pack_propagate(False)
        
        warnings_row = []
        warnings_list = ["warning1", "warning2", "warning3"]
        for index, value in enumerate(warnings_list):
            warnings_row.append(ttk.Label(warnings_frame, text = value))
            warnings_row[index].grid()

        # frame for the flagged rows from the BOMs
        flagged_rows_frame = tk.LabelFrame(self, text = "Flagged Rows")
        flagged_rows_frame.pack(side = "bottom", fill = "both", expand = True, padx = 10, pady = 10)

        # treeview for the actual data
        flagged_rows = ttk.Treeview(flagged_rows_frame)
        flagged_rows.place(relheight = 1, relwidth = 1)
        flagged_rows_scrolly = tk.Scrollbar(flagged_rows_frame, orient = "vertical", command = flagged_rows.yview)
        flagged_rows_scrollx = tk.Scrollbar(flagged_rows_frame, orient = "horizontal", command = flagged_rows.xview)
        flagged_rows.configure(xscrollcommand = flagged_rows_scrollx.set, yscrollcommand = flagged_rows_scrolly.set)
        flagged_rows_scrolly.pack(side = "right", fill = "y")
        flagged_rows_scrollx.pack(side = "bottom", fill = "x")


    def uploadFileA(self, *_):
        filename = filedialog.askopenfilename()
        self.bomA_label_value.set(filename)

    def uploadFileB(self, *_):
        filename = filedialog.askopenfilename()
        self.bomB_label_value.set(filename)
    
    def compareBoms(self, *_):
        print("do stuff! :)))")
        
        



# https://stackoverflow.com/questions/44798950/how-to-display-a-dataframe-in-tkinter
# https://stackoverflow.com/questions/64298669/how-to-show-pandas-data-frame-in-tkinter-gui-inside-the-gui-screen
# https://www.youtube.com/watch?v=PgLjwl6Br0kS


main()