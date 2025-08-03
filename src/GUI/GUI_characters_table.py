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
        self.character_table.place(x=5, y=260, width=self.character_table_width, height=self.character_table_height)

    def on_row_click(self, event):
        selected_row_data = self.character_table.get_row_data(event.selected.row)
        self.gui_main.entry_preview.draw_red_rectangle(selected_row_data)
