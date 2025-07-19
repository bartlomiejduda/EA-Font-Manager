import tkinter as tk

from src.GUI.right_clicker import RightClicker


class GuiFileHeaderInfoBox(tk.Frame):
    def __init__(self, parent, gui_main):
        super().__init__(parent)

        # File Header
        self.file_header_labelframe = tk.LabelFrame(parent, text="")
        self.file_header_labelframe.place(x=5, y=5, width=475, height=215)

        # Signature
        self.fh_label_sign = tk.Label(self.file_header_labelframe, text="Signature:", anchor="w")
        self.fh_label_sign.place(x=5, y=5, width=60, height=20)
        self.fh_text_sign = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.fh_text_sign.place(x=90, y=5, width=80, height=20)
        self.fh_text_sign.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Total file size
        self.fh_label_total_f_size = tk.Label(self.file_header_labelframe, text="Total Size:", anchor="w")
        self.fh_label_total_f_size.place(x=5, y=35, width=60, height=20)
        self.fh_text_total_f_size = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.fh_text_total_f_size.place(x=90, y=35, width=80, height=20)
        self.fh_text_total_f_size.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Version
        self.fh_label_version = tk.Label(self.file_header_labelframe, text="Version:", anchor="w")
        self.fh_label_version.place(x=5, y=65, width=90, height=20)
        self.fh_text_version = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.fh_text_version.place(x=90, y=65, width=80, height=20)
        self.fh_text_version.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Number of Characters
        self.fh_label_number_of_characters = tk.Label(self.file_header_labelframe, text="Char. Count:", anchor="w")
        self.fh_label_number_of_characters.place(x=5, y=95, width=90, height=20)
        self.fh_text_number_of_characters = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.fh_text_number_of_characters.place(x=90, y=95, width=80, height=20)
        self.fh_text_number_of_characters.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Font Flags
        self.fh_label_font_flags = tk.Label(self.file_header_labelframe, text="Font Flags:", anchor="w")
        self.fh_label_font_flags.place(x=5, y=125, width=90, height=20)
        self.fh_text_font_flags = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.fh_text_font_flags.place(x=90, y=125, width=80, height=20)
        self.fh_text_font_flags.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Char. Info Offset
        self.fh_label_char_info_offset = tk.Label(self.file_header_labelframe, text="Char. Info:", anchor="w")
        self.fh_label_char_info_offset.place(x=5, y=155, width=90, height=20)
        self.fh_text_char_info_offset = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.fh_text_char_info_offset.place(x=90, y=155, width=80, height=20)
        self.fh_text_char_info_offset.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Center X
        self.fh_label_center_x = tk.Label(self.file_header_labelframe, text="Center X:", anchor="w")
        self.fh_label_center_x.place(x=235, y=5, width=90, height=20)
        self.fh_text_center_x = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.fh_text_center_x.place(x=310, y=5, width=80, height=20)
        self.fh_text_center_x.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Center Y
        self.fh_label_center_y = tk.Label(self.file_header_labelframe, text="Center Y:", anchor="w")
        self.fh_label_center_y.place(x=235, y=35, width=90, height=20)
        self.fh_text_center_y = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.fh_text_center_y.place(x=310, y=35, width=80, height=20)
        self.fh_text_center_y.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Ascent
        self.fh_label_ascent = tk.Label(self.file_header_labelframe, text="Ascent:", anchor="w")
        self.fh_label_ascent.place(x=235, y=65, width=90, height=20)
        self.fh_text_ascent = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.fh_text_ascent.place(x=310, y=65, width=80, height=20)
        self.fh_text_ascent.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Descent
        self.fh_label_descent = tk.Label(self.file_header_labelframe, text="Descent:", anchor="w")
        self.fh_label_descent.place(x=235, y=95, width=90, height=20)
        self.fh_text_descent = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.fh_text_descent.place(x=310, y=95, width=80, height=20)
        self.fh_text_descent.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Kerning Table Offset
        self.fh_label_kerning_table_offset = tk.Label(self.file_header_labelframe, text="Kern. Info:", anchor="w")
        self.fh_label_kerning_table_offset.place(x=235, y=125, width=90, height=20)
        self.fh_text_kerning_table_offset = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.fh_text_kerning_table_offset.place(x=310, y=125, width=80, height=20)
        self.fh_text_kerning_table_offset.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Shape Header Offset
        self.fh_label_shape_header_offset = tk.Label(self.file_header_labelframe, text="Shape. Info:", anchor="w")
        self.fh_label_shape_header_offset.place(x=235, y=155, width=90, height=20)
        self.fh_text_shape_header_offset = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.fh_text_shape_header_offset.place(x=310, y=155, width=80, height=20)
        self.fh_text_shape_header_offset.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))
