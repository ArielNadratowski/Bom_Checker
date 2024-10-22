import tkinter as tk
import numpy as np
import pandas as pd
from functools import reduce
import highlight_error
from tableview import tableview
from tkinter import ttk
from importlib import reload

""" Frame that shows compare, search, and clear bom buttons as well as stores error information """
class CompareSearchFrame:    
    def __init__(self, main_window, frame_holding_boms, highlight_errors_frame, warning_frame, compare_button_coords = [0, 0], search_coords  = [2, 0], padx_ = 10, pady_ = 10, search_input_height = 1, search_input_width = 10):
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
        
        self.set_up_window(main_window, padx_, pady_)
        self.set_up_storage_places()
        self.compare_bom_button(self.compare_search_frame, main_window, frame_holding_boms, highlight_errors_frame, warning_frame, compare_button_coords, padx_, pady_, COLOR_MAP)
        self.clear_boms_button(self.compare_search_frame, frame_holding_boms, highlight_errors_frame, warning_frame, compare_button_coords, padx_, pady_)
        self.search_bom_button(self.compare_search_frame, warning_frame, search_coords, padx_, pady_, search_input_height, search_input_width)
    
    def set_up_window(self, main_window, padx_, pady_):
        # set up frame for compare and search bom buttons
        self.compare_search_frame = tk.Frame(main_window)
        self.compare_search_frame.grid(column = 0, row = 3, padx = padx_, pady = pady_)

    def set_up_storage_places(self):
        # place to hold highlight errors list and dataframes
        self.highlight_error_list = []
        self.highlight_error_dataframe = None
        self.all_boms_merged = None

    def compare_bom_button(self, compare_search_frame, main_window, frame_holding_boms, highlight_errors_frame, warning_frame, compare_button_coords, padx_, pady_, COLOR_MAP):
        compare_button = tk.Button(compare_search_frame, text = 'COMPARE BOMs', command = lambda: self.compare_boms(main_window, frame_holding_boms, highlight_errors_frame, warning_frame, COLOR_MAP))
        compare_button.grid(row = compare_button_coords[0], column = compare_button_coords[1], padx = padx_, pady = pady_)

    def clear_boms_button(self, compare_search_frame, frame_holding_boms, highlight_errors_frame, warning_frame, compare_button_coords, padx_, pady_):
        clear_boms = tk.Button(compare_search_frame, text = 'CLEAR BOMs', foreground = 'red', command = lambda: self.clear_data(frame_holding_boms, highlight_errors_frame, warning_frame))
        clear_boms.grid(row = compare_button_coords[0], column = compare_button_coords[1] + 1, padx = padx_, pady = pady_)

    def search_bom_button(self, compare_search_frame, warning_frame, search_coords, padx_, pady_, search_input_height, search_input_width): 
        self.search_button = tk.Button(compare_search_frame, text = 'Search Ref Dsg', command = lambda: self.search_reference_designator(warning_frame))
        self.search_button.grid(row = search_coords[0], column = search_coords[1], padx = padx_, pady = pady_)
        self.search_button.config(state = tk.DISABLED)
        self.search_input = tk.Text(compare_search_frame, height = search_input_height, width = search_input_width)
        self.search_input.grid(row = search_coords[0], column = search_coords[1] + 1, padx = padx_, pady = pady_)

    def compare_boms(self, main_window, frame_holding_boms, highlight_errors_frame, warning_frame, COLOR_MAP):
        # clear warnings, highlight errors frame, merged boms, but not any uploaded boms
        self.clear_data(frame_holding_boms, highlight_errors_frame, warning_frame, clear_boms = False)
        
        selected_boms = self.filter_selected_boms(frame_holding_boms)
        self.check_for_duplicates(selected_boms)
        self.check_missing_reference_designators(selected_boms)
        self.compare_reference_designators(selected_boms)
        self.set_up_table_view(main_window, highlight_errors_frame, COLOR_MAP)
        self.fill_table(self.highlight_error_dataframe)
        self.highlight_table_cells()
        self.display_warnings(warning_frame)
        self.search_button.config(state = tk.NORMAL) # enable search bom button (button needs merged boms to be available first)

    def filter_selected_boms(self, frame_holding_boms):
        # filter for selected dataframes only
        selected_boms = []
        for bom in frame_holding_boms.boms:
            if bom.selected.get() == 1:
                selected_boms.append(bom)
        return selected_boms

    def check_for_duplicates(self, selected_boms):
        for bom in selected_boms:
            if bom.bom_dataframe['split_ref_designators'].duplicated().any():
                duplicated = bom.bom_dataframe['split_ref_designators'].duplicated()
                list_of_duplicates = []
                self.make_duplplicate_warning(duplicated, list_of_duplicates, bom)
        
    def make_duplplicate_warning(self, duplicated, list_of_duplicates, bom):
        for index, item in enumerate(duplicated):
            if item == True:
                list_of_duplicates.append(bom.bom_dataframe.loc[index]['split_ref_designators'])
        for item in list_of_duplicates:
            message = 'There are duplicates of ' + str(item) + ' in ' + bom.name
            highlight_error_item = highlight_error.HighlightError(item, message, 'duplicate', None) # using None to indicate entire row gets highlighted for right now
            self.highlight_error_list.append(highlight_error_item)

    """ Makes a key of all possible reference designators across selected boms, and checks if any are missing from each bom """
    def check_missing_reference_designators(self, selected_boms):
        list_of_reference_designator_lists = []
        for bom in selected_boms:
            list_of_reference_designator_lists.append(bom.bom_dataframe['split_ref_designators'].to_list())
        key_as_list = []
        key = self.create_reference_designator_key(list_of_reference_designator_lists, key_as_list)
        self.make_missing_warning(list_of_reference_designator_lists, key, selected_boms)

    def create_reference_designator_key(self, list_of_reference_designator_lists, key_as_list):
        for list in list_of_reference_designator_lists:
            for reference_designator in list:
                if reference_designator not in key_as_list:
                    key_as_list.append(reference_designator)
        return set(key_as_list)

    def make_missing_warning(self, list_of_reference_designator_lists, key, selected_boms):
        for index, list in enumerate(list_of_reference_designator_lists):
            missing_reference_designators = set(key).difference(list)
            for reference_designator in missing_reference_designators:
                message = str(reference_designator) + ' is missing from ' + str(selected_boms[index].name) # depends on the index staying consistent between selected_boms and list_of_reference_designator_lists, which I think should be the case
                highlight_error_item = highlight_error.HighlightError(reference_designator, message, 'missing', None) # using None to indicate entire row gets highlighted for right now
                self.highlight_error_list.append(highlight_error_item)

    def compare_reference_designators(self, selected_boms):
        selected_bom_dataframes = []
        selected_bom_names = []
        self.all_boms_merged = self.clean_merge_boms(selected_boms, selected_bom_dataframes, selected_bom_names)
        self.compare_all_columns(self.all_boms_merged, selected_bom_names)
        self.make_highlight_error_dataframe(self.all_boms_merged)

    def clean_merge_boms(self, selected_boms, selected_bom_dataframes, selected_bom_names):
        for bom in selected_boms:
            bom_drop_quantity = bom.bom_dataframe.drop(bom.bom_dataframe.columns[3], axis=1, inplace=False) # drop quantity column because the way it currently is isn't useful TODO: add a function to check quantity somehow (probably count duplicates in Description?)
            bom_drop_quantity.columns = bom_drop_quantity.columns.map(lambda x : x + '_' + str(bom.name) if x !='split_ref_designators' else x)  # need to rename columns besides split_ref_designators to prevent merge error later
            selected_bom_dataframes.append(bom_drop_quantity)
            selected_bom_names.append(bom.name)

        all_boms_merged = reduce(lambda  left,right: pd.merge(left,right,on=['split_ref_designators'],
                                            how='outer'), selected_bom_dataframes)
        
        all_boms_merged = all_boms_merged.infer_objects(copy=False).fillna('MISSING')

        # do some cleaning so that it will be in the same format as will be shown in the highlight errors frame
        all_boms_merged = all_boms_merged[['split_ref_designators'] + [ col for col in all_boms_merged.columns if col != 'split_ref_designators' ]] # pull split_ref_designators to front of dataframe
        all_boms_merged = all_boms_merged.loc[:, ~(all_boms_merged.columns.str.startswith('index')|all_boms_merged.columns.str.startswith('original_index')|all_boms_merged.columns.str.startswith('ref_dsg_position'))] # drop some additional columns that aren't useful

        return all_boms_merged

    """ Three layered nested for loop because you need to iterate down each row per reference designator, across columns per column type, and do this n times per number of boms that you are comparing """
    def compare_all_columns(self, all_boms_merged, selected_bom_names):
        for index, reference_designator in enumerate(all_boms_merged['split_ref_designators']):
            for i in range(len(selected_bom_names)): 
                for j, col in enumerate(['description', 'manufacturer', 'manufacturer part number'], start = 1):
                    self.compare_columns(all_boms_merged, index, selected_bom_names, reference_designator, self.highlight_error_list, i, j, col)

    """ Compare coresponding columns (description1 index vs description2 index, description1 index vs description3 index...) First bom will be the comparison bom for sake of simplicity """
    def compare_columns(self, all_boms_merged, index, selected_bom_names, reference_designator, place_storing_highlight_errors, loop_iteration, reference_column_index, category_name):
        if all_boms_merged.iloc[index, reference_column_index] != all_boms_merged.iloc[index, reference_column_index + loop_iteration*3]:
            message = str(selected_bom_names[loop_iteration]) + ' ' + str(category_name) + ' for ' + str(reference_designator) + ' does not match ' + str(selected_bom_names[0])
            highlight_error_item = highlight_error.HighlightError(reference_designator, message, str(category_name) + ' discrepancy', [reference_column_index, reference_column_index + loop_iteration*3])
            place_storing_highlight_errors.append(highlight_error_item)

    """ Compiles list of all ref dsg in highlight error list and pulls those rows from all_boms_merged """
    def make_highlight_error_dataframe(self, all_boms_merged):
        reference_designators_with_errors = []
        for item in self.highlight_error_list:
            reference_designators_with_errors.append(item.reference_designator)
        reference_designators_with_errors_set = set(reference_designators_with_errors)
        self.highlight_error_dataframe = all_boms_merged[all_boms_merged['split_ref_designators'].isin(reference_designators_with_errors_set)]
        self.highlight_error_dataframe = self.highlight_error_dataframe.reset_index(drop=True)

    def set_up_table_view(self, main_window, highlight_errors_frame, COLOR_MAP):
        # set up table view 
        header_list = list(self.highlight_error_dataframe.columns)
        column_width = []
        for i in header_list:
            column_width.append(200)
            
        tableview.setup_columns(root = main_window, 
                                window = highlight_errors_frame.highlight_errors_frame.interior, 
                                column_headers = header_list, 
                                column_widths = column_width, 
                                table_height = 20, 
                                frame_height = 200, 
                                column_height = 200, 
                                header_height = 49, 
                                table_color_map = COLOR_MAP,
                                xpad=0, 
                                ypad=0
                                )
        tableview.pack()

    def fill_table(self, dataframe):
        tableview.clear()

        number_rows = len(dataframe.index)
        for i in range(number_rows):
            column_number = 0
            row_as_list = dataframe.iloc[i].tolist()
            for item in row_as_list:
                tableview.insert_item(column_number, text = item)
                column_number += 1

    def highlight_table_cells(self):
        for error in self.highlight_error_list: # iterates down the list of highlight errors
            if error.error_type == 'duplicate':
                self.handle_duplicate_error(error)
            elif error.error_type == 'missing':
                self.handle_missing_error(error)
            else:
                self.handle_general_error(error)

    def handle_duplicate_error(self, error, background = 'orange'):
        row_indexes = self.highlight_error_dataframe[self.highlight_error_dataframe['split_ref_designators'] == error.reference_designator].index.tolist()
        for row_index in row_indexes: # because there are more than one index here, but can only feed highlight_cell 1 row at a time
            tableview.highlight_cell(column = 1, row = row_index, bg = background, fg = 'black') # column = 0 + 1 because tableview doesn't zero index this for some reason??
    
    def handle_missing_error(self, error):
        self.handle_duplicate_error(error, background = 'red')

    def handle_general_error(self, error):
        row_indexes = self.highlight_error_dataframe[self.highlight_error_dataframe['split_ref_designators'] == error.reference_designator].index.tolist()
        for row_index in row_indexes: 
            for column_index in error.error_location:
                    tableview.highlight_cell(column = column_index + 1, row = row_index, bg = 'yellow', fg = 'black')

    def display_warnings(self, warning_frame):
        for error in self.highlight_error_list:
            if error.error_type == 'duplicate':
                self.make_warning_label(warning_frame, error, 'orange')
            elif error.error_type == 'missing':
                self.make_warning_label(warning_frame, error, 'red')
            else:
                self.make_warning_label(warning_frame, error, 'black')
    
    def make_warning_label(self, warning_frame, error, color):
        label = ttk.Label(warning_frame.warning_frame.interior, text = error.warning, foreground = color)
        label.pack()

    def clear_data(self, frame_holding_boms, highlight_errors_frame, warning_frame, clear_boms = True):
        self.clear_highlight_errors_and_dataframe()
        if clear_boms == True:
            self.clear_boms(frame_holding_boms)
        self.clear_highlight_error_frame(highlight_errors_frame)
        self.search_button.config(state = tk.DISABLED)
        self.clear_warnings(warning_frame)

    def clear_highlight_errors_and_dataframe(self):
        self.highlight_error_list = []
        self.highlight_error_dataframe = None
        self.all_boms_merged = []

    def clear_boms(self, frame_holding_boms):
        # clear uploaded boms
        frame_holding_boms.boms = []

        # clear checkboxes for uploaded boms
        for widget in frame_holding_boms.boms_uploaded_frame.winfo_children():
            widget.destroy()
    
    def clear_highlight_error_frame(self, highlight_errors_frame):
        for widget in highlight_errors_frame.highlight_errors_frame.interior.winfo_children():
            widget.destroy()
        reload(tableview) # theres some variables hanging around here that need to get cleared and idk which ones and how many so uh just axing everything

    def clear_warnings(self, warning_frame):
        for widget in warning_frame.warning_frame.interior.winfo_children():
            widget.destroy()

    def search_reference_designator(self, warning_frame):
            self.clear_warnings(warning_frame)
            searched_rows = self.get_searched_reference_designators()
            self.fill_table(searched_rows)

    def get_searched_reference_designators(self):
        search_text = self.search_input.get('1.0', 'end')
        search_text = search_text.strip()

        self.all_boms_merged['split_ref_designators'] = self.all_boms_merged['split_ref_designators'].str.strip()
        searched_rows = self.all_boms_merged[self.all_boms_merged['split_ref_designators'] == search_text]
        return searched_rows
