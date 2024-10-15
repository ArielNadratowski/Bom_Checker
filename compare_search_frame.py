import tkinter as tk
import numpy as np
import pandas as pd
from functools import reduce
import highlight_error
from tableview import tableview
from tkinter import ttk
from importlib import reload

class CompareSearchFrame:
    def __init__(self, frame_holding_boms, highlight_errors_frame, warning_frame, position, compare_button_coords = [0, 0], search_coords  = [2, 0], padx_ = 10, pady_ = 10, search_input_height = 1, search_input_width = 10):
        # set up frame for compare and search bom buttons
        compare_search_frame = tk.Frame()
        compare_search_frame.pack(side = position)

        # place to hold highlight errors list and dataframes
        self.highlight_error_list = []
        self.highlight_error_dataframe = None
        self.all_boms_dataframe = None

        # compare bom button
        compare_button = tk.Button(compare_search_frame, text = 'COMPARE BOMs', command = lambda: self.compare_boms(frame_holding_boms, highlight_errors_frame, warning_frame))
        compare_button.grid(row = compare_button_coords[0], column = compare_button_coords[1], padx = padx_, pady = pady_)

        # clear boms button
        clear_boms = tk.Button(compare_search_frame, text = 'CLEAR BOMs', foreground = 'red', command = lambda: self.clear_data(frame_holding_boms, highlight_errors_frame, warning_frame))
        clear_boms.grid(row = compare_button_coords[0], column = compare_button_coords[1] + 1, padx = padx_, pady = pady_)

        # search bom button 
        search_button = tk.Button(compare_search_frame, text = 'Search Ref Dsg', command = lambda: self.search_reference_designator(warning_frame))
        search_button.grid(row = search_coords[0], column = search_coords[1], padx = padx_, pady = pady_)
        self.search_input = tk.Text(compare_search_frame, height = search_input_height, width = search_input_width)
        self.search_input.grid(row = search_coords[0], column = search_coords[1] + 1, padx = padx_, pady = pady_)

    def compare_boms(self, frame_holding_boms, highlight_errors_frame, warning_frame):
        # clear warnings and highlight errors frame, but not any uploaded boms
        self.clear_data(frame_holding_boms, highlight_errors_frame, warning_frame, clear_boms = False)
        
        # filter for selected dataframes only
        selected_boms = []
        for bom in frame_holding_boms.boms:
            if bom.selected.get() == 1:
                selected_boms.append(bom)
        # check for duplicates
        self.check_for_duplicates(selected_boms)
        # check for missing reference designators
        self.check_missing_reference_designators(selected_boms)
        # check for differences between reference designator rows (different manufacturer, etc)
        self.compare_reference_designators(selected_boms)
        # set up tableview
        self.set_up_table_view(highlight_errors_frame)
        # fill out highlight error table table
        self.fill_table()
        # highlight stuff in table
        self.highlight_table_cells()
        # display warnings
        self.display_warnings(warning_frame)

    def check_for_duplicates(self, selected_boms):
        for bom in selected_boms:
            if bom.bom_dataframe['split_ref_designators'].duplicated().any():
                duplicated = bom.bom_dataframe['split_ref_designators'].duplicated()
                list_of_duplicates = []
                for index, item in enumerate(duplicated, start=0):
                    if item == True:
                        list_of_duplicates.append(bom.bom_dataframe.loc[index]['split_ref_designators'])
                for item in list_of_duplicates:
                    message = 'There are duplicates of ' + str(item) + ' in ' + bom.name
                    highlight_error_item = highlight_error.HighlightError(item, message, 'duplicate', None) # using None to indicate entire row gets highlighted for right now
                    self.highlight_error_list.append(highlight_error_item)

    def check_missing_reference_designators(self, selected_boms):
        list_of_reference_designator_lists = []
        for bom in selected_boms:
            list_of_reference_designator_lists.append(bom.bom_dataframe['split_ref_designators'].to_list())
        key_as_list = []
        for list in list_of_reference_designator_lists:
            for reference_designator in list:
                if reference_designator not in key_as_list:
                    key_as_list.append(reference_designator)
        key = set(key_as_list)
        # key is now a set of all possible reference designators

        for index, list in enumerate(list_of_reference_designator_lists):
            missing_reference_designators = set(key).difference(list)
            for reference_designator in missing_reference_designators:
                message = str(reference_designator) + ' is missing from ' + str(selected_boms[index].name) # depends on the index staying consistent between selected_boms and list_of_reference_designator_lists, which I think should be the case
                highlight_error_item = highlight_error.HighlightError(reference_designator, message, 'missing', None) # using None to indicate entire row gets highlighted for right now
                self.highlight_error_list.append(highlight_error_item)

    ## Compare reference designators

    def compare_reference_designators(self, selected_boms):
        selected_bom_dataframes = []
        selected_bom_names = []
        for bom in selected_boms:
            bom_drop_quantity = bom.bom_dataframe.drop(bom.bom_dataframe.columns[3], axis=1, inplace=False) # drop quantity column because the way it currently is isn't useful TODO: add a function to check quantity somehow (probably count duplicates in Description?)
            bom_drop_quantity.columns = bom_drop_quantity.columns.map(lambda x : x + '_' + str(bom.name) if x !='split_ref_designators' else x)  # need to rename columns besides split_ref_designators to prevent merge error later
            selected_bom_dataframes.append(bom_drop_quantity)
            selected_bom_names.append(bom.name)

        all_boms_merged = reduce(lambda  left,right: pd.merge(left,right,on=['split_ref_designators'],
                                            how='outer'), selected_bom_dataframes)
        
        # do some cleaning so that it will be in the same format as will be shown in the highlight errors frame
        all_boms_merged = all_boms_merged[['split_ref_designators'] + [ col for col in all_boms_merged.columns if col != 'split_ref_designators' ]] # pull split_ref_designators to front of dataframe
        all_boms_merged = all_boms_merged.loc[:, ~(all_boms_merged.columns.str.startswith('index')|all_boms_merged.columns.str.startswith('original_index')|all_boms_merged.columns.str.startswith('ref_dsg_position'))] # drop some additional columns that aren't useful
        print(all_boms_merged)

        for index, reference_designator in enumerate(all_boms_merged['split_ref_designators'], start= 0): # will iterate down the rows of merged boms
            for i in range(len(selected_bom_names)): # using this to compare coresponding columns (description1 index vs description2 index, description1 index vs description3 index...) First bom will be the comparison bom for sake of simplicity
                self.compare_columns(all_boms_merged, index, selected_bom_names, reference_designator, self.highlight_error_list, i, 1, 'description')
                self.compare_columns(all_boms_merged, index, selected_bom_names, reference_designator, self.highlight_error_list, i, 2, 'manufacturer')
                self.compare_columns(all_boms_merged, index, selected_bom_names, reference_designator, self.highlight_error_list, i, 3, 'manufacturer part number')
        
        # make highlight_error_dataframe
        self.make_highlight_error_dataframe(all_boms_merged)

        # save merged dataframe (needed for search reference designators)
        self.all_boms_dataframe = all_boms_merged

    def compare_columns(self, all_boms_merged, index, selected_bom_names, reference_designator, place_storing_highlight_errors, loop_iteration, reference_column_index, category_name):
        if all_boms_merged.iloc[index, reference_column_index] != all_boms_merged.iloc[index, reference_column_index + loop_iteration*3]:
            message = str(selected_bom_names[loop_iteration]) + ' ' + str(category_name) + ' for ' + str(reference_designator) + ' does not match ' + str(selected_bom_names[0])
            highlight_error_item = highlight_error.HighlightError(reference_designator, message, str(category_name) + ' discrepancy', [reference_column_index, reference_column_index + loop_iteration*3])
            place_storing_highlight_errors.append(highlight_error_item)

    def make_highlight_error_dataframe(self, all_boms_merged):
        
        # compile list of all ref dsg in highlight error list and pull from all_boms_merged
        reference_designators_with_errors = []
        for item in self.highlight_error_list:
            reference_designators_with_errors.append(item.reference_designator)
        reference_designators_with_errors_set = set(reference_designators_with_errors)
        self.highlight_error_dataframe = all_boms_merged[all_boms_merged['split_ref_designators'].isin(reference_designators_with_errors_set)]
        self.highlight_error_dataframe = self.highlight_error_dataframe.reset_index(drop=True)

    def set_up_table_view(self, highlight_errors_frame):
        # set up table view 
        header_list = list(self.highlight_error_dataframe.columns)
        column_width = []
        for i in header_list:
            column_width.append(200)

        COLOR_MAP = {
            'header_background': 'grey70',
            'header_foreground': 'black',
            'tree_background': 'white',
            'tree_foreground': 'grey',
            'item_foreground': 'black',
            'tree_erase_background': 'white',
            'selected_row_bg_color': 'grey90',
            'selected_row_text_color': 'black',
            'separator_color':'grey'
            }
            
        tableview.setup_columns(root = highlight_errors_frame.highlight_errors_frame, 
                                window = highlight_errors_frame.highlight_errors_frame, 
                                column_headers = header_list, 
                                column_widths = column_width, 
                                table_height = 20, 
                                frame_height = 300, 
                                column_height = 200, 
                                header_height = 49, 
                                table_color_map = COLOR_MAP)
        tableview.pack()

    def fill_table(self):
        tableview.clear()

        number_rows = len(self.highlight_error_dataframe.index)
        for i in range(number_rows):
            column_number = 0
            row_as_list = self.highlight_error_dataframe.iloc[i].tolist()
            for item in row_as_list:
                tableview.insert_item(column_number, text = item)
                column_number += 1

    def highlight_table_cells(self):
        # wow I hate this entire for loop
        for error in self.highlight_error_list: # iterates down the list of highlight errors
            if error.error_type == 'duplicate':
                row_indexes = self.highlight_error_dataframe[self.highlight_error_dataframe['split_ref_designators'] == error.reference_designator].index.tolist()
                for row_index in row_indexes: # because there are more than one index here, but can only feed highlight_cell 1 row at a time
                    for column_index in range(len(list(self.highlight_error_dataframe.columns))): # also need to iterate through each column because highlight_cell also only takes 1 column at a time
                        tableview.highlight_cell(column = column_index + 1, row = row_index, bg = 'orange', fg = 'black') # column index gets +1 because tableview doesn't zero index this for some reason??
            elif error.error_type == 'missing':
                row_indexes = self.highlight_error_dataframe[self.highlight_error_dataframe['split_ref_designators'] == error.reference_designator].index.tolist()
                for row_index in row_indexes: 
                    for column_index in error.error_location:
                            tableview.highlight_cell(column = column_index + 1, row = row_index, bg = 'red', fg = 'black')
            else:
                row_indexes = self.highlight_error_dataframe[self.highlight_error_dataframe['split_ref_designators'] == error.reference_designator].index.tolist()
                for row_index in row_indexes: 
                    for column_index in error.error_location:
                            tableview.highlight_cell(column = column_index + 1, row = row_index, bg = 'yellow', fg = 'black')

    def display_warnings(self, warning_frame):
        
        for error in self.highlight_error_list:
            if error.error_type == 'duplicate':
                label = ttk.Label(warning_frame.warning_frame, text = error.warning, foreground = 'orange')
                label.pack()
            elif error.error_type == 'missing':
                label = ttk.Label(warning_frame.warning_frame, text = error.warning, foreground = 'red')
                label.pack()
            else:
                label = ttk.Label(warning_frame.warning_frame, text = error.warning, foreground = 'black')
                label.pack()

    def clear_data(self, frame_holding_boms, highlight_errors_frame, warning_frame, clear_boms = True):
        # clear highlight errors list and highlight error dataframe
        self.highlight_error_list = []
        self.highlight_error_dataframe = None

        if clear_boms == True:
            # clear uploaded boms
            frame_holding_boms.boms = []

            # clear checkboxes for uploaded boms
            for widget in frame_holding_boms.boms_uploaded_frame.winfo_children():
                widget.destroy()

        # clear highlight error frame 
        for widget in highlight_errors_frame.highlight_errors_frame.winfo_children():
            widget.destroy()

        reload(tableview) # theres some variables hanging around here that need to get cleared and idk which ones and how many so uh just axing everything

        # clear warnings in warning frame
        for widget in warning_frame.warning_frame.winfo_children():
            widget.destroy()

    def search_reference_designator(self, warning_frame):
            # clear tableview
            tableview.clear()

            # clear warnings in warning frame
            for widget in warning_frame.warning_frame.winfo_children():
                widget.destroy()

            search_text = self.search_input.get('1.0', 'end')
            search_text = search_text.strip()

            self.all_boms_dataframe['split_ref_designators'] = self.all_boms_dataframe['split_ref_designators'].str.strip()

            searched_rows = self.all_boms_dataframe[self.all_boms_dataframe['split_ref_designators'] == search_text]

            # fill in table 
            number_rows = len(searched_rows.index)
            for i in range(number_rows):
                column_number = 0
                row_as_list = searched_rows.iloc[i].tolist()
                for item in row_as_list:
                    tableview.insert_item(column_number, text = item)
                    column_number += 1
        
            

