import tkinter as tk

from reversebox.common.logger import get_logger
from tksheet import Sheet

logger = get_logger(__name__)


# fmt: off

class GuiCharactersTable(tk.Frame):
    def __init__(self, parent, gui_main):
        super().__init__(parent)

        self.character_table_width = 935
        self.character_table_height = 190
        self.gui_main = gui_main

        self.character_table = Sheet(parent,
                                     width=self.character_table_width,
                                     height=self.character_table_height)

        self.character_table.enable_bindings((  # type: ignore
            "single_select",
            "row_select",
            "column_select",
            "edit_cell",
            "arrowkeys",
            "rc_popup_menu",
            "copy", "paste",
            "delete", "undo"
        ))
        self.character_table.bind("<<SheetSelect>>", self.on_row_click)
        self.character_table.set_options(table_bg=parent["bg"], header_bg="#ccc8bc")

        self.character_table.edit_validation(self.validate_cell)
        self.character_table.place(x=5, y=260, width=self.character_table_width, height=self.character_table_height)

    def on_row_click(self, event):
        if event.selected:
            selected_row_data = self.character_table.get_row_data(event.selected.row)
            self.gui_main.entry_preview.draw_red_rectangle(selected_row_data)

    def validate_cell(self, cell_info):
        column_number: int = cell_info["column"]
        new_cell_value = cell_info["value"]
        expected_column_type = str if column_number == 0 else int

        r, c = cell_info.row, cell_info.column
        try:
            old_cell_value = cell_info.cells.table.get((r, c))
        except Exception:
            old_cell_value = self.character_table[(r, c)].data

        signed_flag: bool = False
        if column_number in (5, 6, 7, 10):  # advance_y, x_offset, y_offset, advance_x
            signed_flag = True

        is_one_byte_flag: bool = False
        if column_number in (1, 2, 5, 6, 7, 8):  # width, height, advance_y, x_offset, y_offset,
            is_one_byte_flag = True

        if expected_column_type is int:
            try:
                temp_int_value = int(new_cell_value)
                if is_one_byte_flag:
                    if signed_flag:
                        if temp_int_value not in range(-128, 127):
                            return old_cell_value
                    else:
                        if temp_int_value not in range(0, 255):
                            return old_cell_value
                else:
                    if signed_flag:
                        if temp_int_value not in range(-32768, 32767):
                            return old_cell_value
                    else:
                        if temp_int_value not in range(0, 65535):
                            return old_cell_value
                return temp_int_value
            except ValueError:
                return old_cell_value
        elif expected_column_type is str:
            if isinstance(new_cell_value, str):
                try:
                    temp_new_ord_value: int = ord(new_cell_value)
                    if temp_new_ord_value not in range(0, 65535):
                        return old_cell_value
                except Exception:
                    return old_cell_value
                return new_cell_value
            else:
                return old_cell_value
        else:
            return old_cell_value
