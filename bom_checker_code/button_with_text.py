import tkinter as tk

class ButtonWithText:
    def __init__(self, frame, label_text, text_row_index, padx = 5, pady = 5):    
        self.input = tk.Text(frame, height =1, width = 15)
        self.label = tk.Label(frame, text = label_text)

        self.input.grid(row = text_row_index, column = 0, padx = padx, pady = pady)
        self.label.grid(row = text_row_index, column = 1, padx = padx, pady = pady)