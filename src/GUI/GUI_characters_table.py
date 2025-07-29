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
        self.character_table.set_options(table_bg=parent["bg"], header_bg="#ccc8bc")
        self.character_table.place(x=5, y=260, width=self.character_table_width, height=self.character_table_height)
