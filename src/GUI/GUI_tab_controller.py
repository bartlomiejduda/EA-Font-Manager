import tkinter as tk
from tkinter import ttk

from src.GUI.GUI_file_header_info_box import GuiFileHeaderInfoBox
from src.GUI.GUI_shape_header_info_box import GuiShapeHeaderInfoBox


class GuiTabController(tk.Frame):
    def __init__(self, parent, gui_main):
        super().__init__(parent)

        self.tab_controller_box = ttk.Notebook(parent)
        self.tab_controller_box.place(x=5, y=5, width=490, height=250)

        self.tab1_file_header = ttk.Frame(self.tab_controller_box)
        self.tab2_shape_header = ttk.Frame(self.tab_controller_box)
        self.tab3_font_flags = ttk.Frame(self.tab_controller_box)

        self.tab_controller_box.add(self.tab1_file_header, text="File Header")
        self.tab_controller_box.add(self.tab2_shape_header, text="Shape Header")
        self.tab_controller_box.add(self.tab3_font_flags, text="Font Flags")

        self.file_header_info_box = GuiFileHeaderInfoBox(self.tab1_file_header, gui_main)
        self.shape_header_info_box = GuiShapeHeaderInfoBox(self.tab2_shape_header, gui_main)
