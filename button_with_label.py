import tkinter as tk

class ButtonWithLabel:
    def __init__(
            self, 
            frame, 
            label_text, 
            buttom_text, 
            button_row_index, 
            command = None, 
            padx = 5, 
            pady = 5, 
            column_span = 1, 
            sticky = None
    ):
        self.label_value = tk.StringVar(frame, label_text)
        self.button = tk.Button(frame, text = buttom_text, command = command)
        self.label = tk.Label(frame, textvariable = self.label_value)

        self.button.grid(row = button_row_index, column = 0, padx = padx, pady = pady)
        self.label.grid(
            row = button_row_index, 
            column = 1, 
            columnspan = column_span, 
            sticky = sticky, 
            padx = padx, 
            pady = pady
        )