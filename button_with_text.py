import tkinter as tk

class ButtonWithText:
    def __init__(self, frame, label_text, text_cord, padx_ = 5, pady_ = 5):    
        self.input = tk.Text(frame, height =1, width = 15)
        self.label = tk.Label(frame, text = label_text)

        self.input.grid(row = text_cord, column = 0, padx = padx_, pady = pady_)
        self.label.grid(row = text_cord, column = 1, padx = padx_, pady = pady_)