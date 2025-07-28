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

        data = [
            [f"Dane {i + 1}.1", f"Dane {i + 1}.2", f"Dane {i + 1}.3"]
            for i in range(50)
        ]

        self.character_table = Sheet(parent,
                                     data=data,
                                     headers=["Kolumna 1", "Kolumna 2", "Kolumna 3"],
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
