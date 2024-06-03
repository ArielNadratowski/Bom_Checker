import tkinter as tk

class ButtonWithLabel:
    def __init__(self, frame, label_text, buttom_text, button_cord, command_ = None, padx_ = 5, pady_ = 5, column_span = 1, sticky_ = None):
        self.label_value = tk.StringVar(frame, label_text)
        self.button = tk.Button(frame, text = buttom_text, command = command_)
        self.label = tk.Label(frame, textvariable = self.label_value)

        self.button.grid(row = button_cord[0], column = button_cord[1], padx = padx_, pady = pady_)
        self.label.grid(row = button_cord[0], column = button_cord[1] + 1, columnspan = column_span, sticky = sticky_, padx = padx_, pady = pady_)


class ButtonWithText:
    def __init__(self, frame, label_text, text_cord, padx_ = 5, pady_ = 5, column_span = 1, sticky_ = None):    
        self.input = tk.Text(frame, height =1, width = 15)
        self.label = tk.Label(frame, text = label_text)

        self.input.grid(row = text_cord[0], column = text_cord[1], padx = padx_, pady = pady_)
        self.label.grid(row = text_cord[0], column = text_cord[1] - 1, padx = padx_, pady = pady_)