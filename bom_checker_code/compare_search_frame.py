import tkinter as tk
import pandas as pd
from functools import reduce
from bom_checker_code.highlight_error import HighlightError
import tableview.tableview as tableview
from tkinter import ttk
from importlib import reload

""" Frame that shows compare, search, and clear bom buttons as well as stores error information """
class CompareSearchFrame:    
    def __init__(
            self, 
            main_window, 
            compare_button_coords = [0, 0], 
            search_coords  = [2, 0], 
            padx = 10, 
            pady = 10, 
            search_input_height = 1, 
            search_input_width = 10
    ):
        self.COLOR_MAP = {
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
        
        self.main_window = main_window
        self.compare_search_subframe = None
        self.compare_button_coords = compare_button_coords
        self.search_coords = search_coords
        self.padx = padx
        self.pady = pady
        self.highlight_error_list = []
        self.highlight_error_dataframe = None
        self.all_boms_merged = None
        self.search_button = None
        self.search_input = None

        self._set_up_window()
        self._compare_bom_button()
        self._clear_boms_button()
        self._search_bom_button(search_input_height, search_input_width)
    
    def _set_up_window(self):
        # set up frame for compare and search bom buttons
        self.compare_search_subframe = tk.Frame(self.main_window)
        self.compare_search_subframe.grid(column = 0, row = 3, padx = self.padx, pady = self.pady)

    def _compare_bom_button(self):
        compare_button = tk.Button(
            self.compare_search_subframe, 
            text = 'COMPARE BOMs', 
            command = self._compare_boms
        )
        compare_button.grid(
            row = self.compare_button_coords[0], 
            column = self.compare_button_coords[1], 
            padx = self.padx, 
            pady = self.pady
        )

    def _clear_boms_button(self):
        clear_boms = tk.Button(
            self.compare_search_subframe, text = 'CLEAR BOMs', 
            foreground = 'red', 
            command = self._clear_data
        )
        clear_boms.grid(
            row = self.compare_button_coords[0], 
            column = self.compare_button_coords[1] + 1, 
            padx = self.padx, 
            pady = self.pady
        )

    def _search_bom_button(self, search_input_height, search_input_width): 
        self.search_button = tk.Button(
            self.compare_search_subframe, 
            text = 'Search Ref Dsg', 
            command = self._search_reference_designator
        )
        self.search_button.grid(
            row = self.search_coords[0], 
            column = self.search_coords[1], 
            padx = self.padx, 
            pady = self.pady
        )
        self.search_button.config(state = tk.DISABLED)
        self.search_input = tk.Text(
            self.compare_search_subframe, 
            height = search_input_height, 
            width = search_input_width
        )
        self.search_input.grid(
            row = self.search_coords[0], 
            column = self.search_coords[1] + 1, 
            padx = self.padx, 
            pady = self.pady
        )

    def _compare_boms(self):
        # clear warnings, highlight errors frame, merged boms, but not any uploaded boms
        self._clear_data(clear_boms = False)
        
        selected_boms = self._filter_selected_boms()
        self._check_quantity_mismatch(selected_boms)
        self._check_for_duplicates(selected_boms)
        self._check_missing_reference_designators(selected_boms)
        self._compare_reference_designators(selected_boms)
        self._set_up_table_view()
        self._fill_table(self.highlight_error_dataframe)
        self._highlight_table_cells()
        self._display_warnings()
        # enable search bom button (button needs merged boms to be available first)
        self.search_button.config(state = tk.NORMAL) 

    def _filter_selected_boms(self):
        # filter for selected dataframes only
        selected_boms = []
        for bom in self.main_window.upload_frame.boms:
            if bom.selected.get() == 1:
                selected_boms.append(bom)
        return selected_boms

    def _check_for_duplicates(self, selected_boms):
        for bom in selected_boms:
            if bom.bom_dataframe['split_ref_designators'].duplicated().any():
                duplicated = bom.bom_dataframe['split_ref_designators'].duplicated()
                list_of_duplicates = []
                self._make_duplplicate_warning(duplicated, list_of_duplicates, bom)
        
    def _make_duplplicate_warning(self, duplicated, list_of_duplicates, bom_object):
        for index, item in enumerate(duplicated):
            if item == True:
                list_of_duplicates.append(bom_object.bom_dataframe.loc[index]['split_ref_designators'])
        for item in list_of_duplicates:
            message = 'There are duplicates of ' + str(item) + ' in ' + bom_object.name
            # using None to indicate entire row gets highlighted for right now
            highlight_error_item = HighlightError(item, message, 'duplicate', None) 
            self.highlight_error_list.append(highlight_error_item)

    """ Makes a key of all possible reference designators across selected boms, and checks if any are missing from each bom """
    def _check_missing_reference_designators(self, selected_boms):
        list_of_reference_designator_lists = []
        for bom in selected_boms:
            list_of_reference_designator_lists.append(bom.bom_dataframe['split_ref_designators'].to_list())
        reference_designator_key = self._create_reference_designator_key(list_of_reference_designator_lists)
        self._make_missing_warning(list_of_reference_designator_lists, reference_designator_key, selected_boms)

    def _create_reference_designator_key(self, list_of_reference_designator_lists):
        key_storage = []
        for list in list_of_reference_designator_lists:
            for reference_designator in list:
                if reference_designator not in key_storage:
                    key_storage.append(reference_designator)
        return set(key_storage)

    def _make_missing_warning(self, list_of_reference_designator_lists, reference_designator_key, selected_boms):
        for index, list in enumerate(list_of_reference_designator_lists):
            missing_reference_designators = set(reference_designator_key).difference(list)
            for reference_designator in missing_reference_designators:
                # depends on the index staying consistent between selected_boms and list_of_reference_designator_lists, 
                # which I think should be the case
                message = str(reference_designator) + ' is missing from ' + str(selected_boms[index].name) 
                # using None to indicate entire row gets highlighted for right now
                highlight_error_item = HighlightError(reference_designator, message, 'missing', None) 
                self.highlight_error_list.append(highlight_error_item)

    def _check_quantity_mismatch(self, selected_boms):
        for bom in selected_boms:
            quantity_mismatch_list = []
            for index, part_number in enumerate(bom.bom_dataframe[bom.manufacturer_part_number]):
                if bom.bom_dataframe.iloc[index]['quantity_mismatch']:
                    quantity_mismatch_list.append(part_number)
            quantity_mismatch_set = set(quantity_mismatch_list)
            for item in quantity_mismatch_set:
                self._make_quantity_mismatch_warning(bom, item)

    def _make_quantity_mismatch_warning(self, bom, item):
        message = 'Quantity for ' + str(item) + ' does not match number of reference designators assigned to it in ' + str(bom.name)
        highlight_error_item = HighlightError(None, message, 'quantity mismatch', None) 
        self.highlight_error_list.append(highlight_error_item)

    def _compare_reference_designators(self, selected_boms):
        selected_bom_dataframes = []
        selected_bom_names = []
        self.all_boms_merged = self._clean_merge_boms(selected_boms, selected_bom_dataframes, selected_bom_names)
        self._compare_all_columns(self.all_boms_merged, selected_bom_names)
        self._make_highlight_error_dataframe(self.all_boms_merged)

    def _clean_merge_boms(self, selected_boms, selected_bom_dataframes, selected_bom_names):
        for bom in selected_boms:
            # drop quantity column because the way it currently is isn't useful 
            bom_drop_cols = bom.bom_dataframe.drop([bom.quantity, 'quantity_mismatch'], axis=1, inplace=False) 
            # need to rename columns besides split_ref_designators to prevent merge error later
            bom_drop_cols.columns = bom_drop_cols.columns.map(
                lambda x : x + '_' + str(bom.name) if x !='split_ref_designators' else x
            )  
            selected_bom_dataframes.append(bom_drop_cols)
            selected_bom_names.append(bom.name)

        all_boms_merged = reduce(lambda  left,right: pd.merge(left,right,on=['split_ref_designators'],
                                            how='outer'), selected_bom_dataframes)
        
        all_boms_merged = all_boms_merged.infer_objects(copy=False).fillna('MISSING')

        # do some cleaning so that it will be in the same format as will be shown in the highlight errors frame
        all_boms_merged = all_boms_merged[['split_ref_designators'] 
                                          + [ col for col in all_boms_merged.columns if col != 'split_ref_designators' ]]
        all_boms_merged = all_boms_merged.loc[:, ~(all_boms_merged.columns.str.startswith('index')
                                                   |all_boms_merged.columns.str.startswith('original_index')
                                                   |all_boms_merged.columns.str.startswith('ref_dsg_position'))]

        return all_boms_merged

    """ 
    Three layered nested for loop because you need to iterate down each row per reference designator, 
    across columns per column type, and do this n times per number of boms that you are comparing 
    """
    def _compare_all_columns(self, all_boms_merged, selected_bom_names):
        for index, reference_designator in enumerate(all_boms_merged['split_ref_designators']):
            for i in range(len(selected_bom_names)): 
                for j, col in enumerate(['description', 'manufacturer', 'manufacturer part number'], start = 1):
                    self._compare_columns(
                        all_boms_merged, 
                        index, 
                        selected_bom_names, 
                        reference_designator, 
                        self.highlight_error_list, 
                        i, 
                        j, 
                        col
                    )

    """ 
    Compare coresponding columns (description1 index vs description2 index, description1 index vs description3 index...) 
    First bom will be the comparison bom for sake of simplicity 
    """
    def _compare_columns(
            self, 
            all_boms_merged, 
            index, 
            selected_bom_names, 
            reference_designator, 
            place_storing_highlight_errors, 
            loop_iteration, 
            reference_column_index, 
            category_name
    ):
        if (all_boms_merged.iloc[index, reference_column_index] != 
            all_boms_merged.iloc[index, reference_column_index + loop_iteration*3]):
            message = (str(selected_bom_names[loop_iteration]) 
                + ' ' 
                + str(category_name) 
                + ' for ' 
                + str(reference_designator) 
                + ' does not match ' 
                + str(selected_bom_names[0])
            )
            highlight_error_item = HighlightError(
                reference_designator, 
                message, 
                str(category_name) + ' discrepancy', 
                [reference_column_index, reference_column_index + loop_iteration*3])
            place_storing_highlight_errors.append(highlight_error_item)

    """ Compiles list of all ref dsg in highlight error list and pulls those rows from all_boms_merged """
    def _make_highlight_error_dataframe(self, all_boms_merged):
        reference_designators_with_errors = []
        for item in self.highlight_error_list:
            reference_designators_with_errors.append(item.reference_designator)
        reference_designators_with_errors_set = set(reference_designators_with_errors)
        self.highlight_error_dataframe = all_boms_merged[all_boms_merged['split_ref_designators'].isin \
            (reference_designators_with_errors_set)]
        self.highlight_error_dataframe = self.highlight_error_dataframe.reset_index(drop=True)

    def _set_up_table_view(self):
        # set up table view 
        header_list = list(self.highlight_error_dataframe.columns)
        column_width = []
        for i in header_list:
            column_width.append(200)
            
        tableview.setup_columns(root = self.main_window, 
                                window = self.main_window.highlight_errors_frame.highlight_errors_subframe.interior, 
                                column_headers = header_list, 
                                column_widths = column_width, 
                                table_height = 20, 
                                frame_height = 200, 
                                column_height = 200, 
                                header_height = 49, 
                                table_color_map = self.COLOR_MAP,
                                xpad=0, 
                                ypad=0
                                )
        tableview.pack()

    def _fill_table(self, dataframe):
        tableview.clear()

        number_rows = len(dataframe.index)
        for i in range(number_rows):
            column_number = 0
            row_as_list = dataframe.iloc[i].tolist()
            for item in row_as_list:
                tableview.insert_item(column_number, text = item)
                column_number += 1

    def _highlight_table_cells(self):
        for error in self.highlight_error_list: # iterates down the list of highlight errors
            if error.error_type == 'duplicate':
                self._handle_duplicate_error(error)
            elif error.error_type == 'missing':
                self._handle_missing_error(error)
            else:
                self._handle_general_error(error)

    def _handle_duplicate_error(self, error, background_color = 'orange'):
        row_indexes = self.highlight_error_dataframe[
            self.highlight_error_dataframe['split_ref_designators'] == error.reference_designator
        ].index.tolist()
        # because there are more than one index here, but can only feed highlight_cell 1 row at a time
        for row_index in row_indexes: 
            # column = 0 + 1 because tableview doesn't zero index this for some reason??
            tableview.highlight_cell(column = 1, row = row_index, bg = background_color, fg = 'black') 
    
    def _handle_missing_error(self, error):
        self._handle_duplicate_error(error, background_color = 'red')

    def _handle_general_error(self, error):
        row_indexes = self.highlight_error_dataframe[
            self.highlight_error_dataframe['split_ref_designators'] == error.reference_designator
        ].index.tolist()
        for row_index in row_indexes: 
            for column_index in error.error_location:
                    tableview.highlight_cell(column = column_index + 1, row = row_index, bg = 'yellow', fg = 'black')

    def _display_warnings(self):
        for error in self.highlight_error_list:
            if error.error_type == 'duplicate':
                self._make_warning_label(error, 'orange')
            elif error.error_type == 'missing':
                self._make_warning_label(error, 'red')
            elif error.error_type == 'quantity mismatch':
                self._make_warning_label(error, 'purple')
            else:
                self._make_warning_label(error, 'black')
    
    def _make_warning_label(self, error, color):
        label = ttk.Label(self.main_window.warning_frame.warning_subframe.interior, text = error.warning, foreground = color)
        label.pack()

    def _clear_data(self, clear_boms = True):
        self._clear_highlight_errors_and_dataframe()
        if clear_boms == True:
            self._clear_boms()
        self._clear_highlight_error_frame()
        self.search_button.config(state = tk.DISABLED)
        self._clear_warnings()

    def _clear_highlight_errors_and_dataframe(self):
        self.highlight_error_list = []
        self.highlight_error_dataframe = None
        self.all_boms_merged = []

    def _clear_boms(self):
        # clear uploaded boms
        self.main_window.upload_frame.boms = []

        # clear checkboxes for uploaded boms
        for widget in self.main_window.upload_frame.boms_uploaded_frame.winfo_children():
            widget.destroy()
    
    def _clear_highlight_error_frame(self):
        for widget in self.main_window.highlight_errors_frame.highlight_errors_subframe.interior.winfo_children():
            widget.destroy()
        # theres some variables hanging around here that need to get cleared and idk which ones and how many 
        # so uh just axing everything
        reload(tableview) 

    def _clear_warnings(self):
        for widget in self.main_window.warning_frame.warning_subframe.interior.winfo_children():
            widget.destroy()

    def _search_reference_designator(self):
            self._clear_warnings()
            searched_rows = self._get_searched_reference_designators()
            self._fill_table(searched_rows)

    def _get_searched_reference_designators(self):
        search_text = self.search_input.get('1.0', 'end')
        search_text = search_text.strip()

        self.all_boms_merged['split_ref_designators'] = self.all_boms_merged['split_ref_designators'].str.strip()
        searched_rows = self.all_boms_merged[self.all_boms_merged['split_ref_designators'] == search_text]
        return searched_rows
