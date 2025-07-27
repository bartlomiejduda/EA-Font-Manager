import tkinter as tk

from src.GUI.right_clicker import RightClicker


class GuiFontFlagsInfoBox(tk.Frame):
    def __init__(self, parent, gui_main):
        super().__init__(parent)

        # font flags box
        self.file_header_labelframe = tk.LabelFrame(parent, text="")
        self.file_header_labelframe.place(x=5, y=5, width=475, height=215)

        # Flags (DEC)
        self.ff_label_flags_dec = tk.Label(self.file_header_labelframe, text="Flags (DEC):", anchor="w")
        self.ff_label_flags_dec.place(x=5, y=5, width=70, height=20)
        self.ff_text_flags_dec = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.ff_text_flags_dec.place(x=105, y=5, width=120, height=20)
        self.ff_text_flags_dec.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Flags (HEX)
        self.ff_label_flags_hex = tk.Label(self.file_header_labelframe, text="Flags (HEX):", anchor="w")
        self.ff_label_flags_hex.place(x=235, y=5, width=70, height=20)
        self.ff_text_flags_hex = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.ff_text_flags_hex.place(x=310, y=5, width=120, height=20)
        self.ff_text_flags_hex.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Antialiased Flag
        self.ff_label_antialiased_flag = tk.Label(self.file_header_labelframe, text="Antialiased:", anchor="w")
        self.ff_label_antialiased_flag.place(x=5, y=35, width=70, height=20)
        self.ff_text_antialiased_flag = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.ff_text_antialiased_flag.place(x=105, y=35, width=120, height=20)
        self.ff_text_antialiased_flag.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Dropshadow Flag
        self.ff_label_dropshadow_flag = tk.Label(self.file_header_labelframe, text="Dropshadow:", anchor="w")
        self.ff_label_dropshadow_flag.place(x=5, y=65, width=80, height=20)
        self.ff_text_dropshadow_flag = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.ff_text_dropshadow_flag.place(x=105, y=65, width=120, height=20)
        self.ff_text_dropshadow_flag.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Outline Flag
        self.ff_label_outline_flag = tk.Label(self.file_header_labelframe, text="Outline:", anchor="w")
        self.ff_label_outline_flag.place(x=5, y=95, width=80, height=20)
        self.ff_text_outline_flag = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.ff_text_outline_flag.place(x=105, y=95, width=120, height=20)
        self.ff_text_outline_flag.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # VRAM Flag
        self.ff_label_vram_flag = tk.Label(self.file_header_labelframe, text="VRAM:", anchor="w")
        self.ff_label_vram_flag.place(x=5, y=125, width=80, height=20)
        self.ff_text_vram_flag = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.ff_text_vram_flag.place(x=105, y=125, width=120, height=20)
        self.ff_text_vram_flag.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Baseline Flag
        self.ff_label_baseline_flag = tk.Label(self.file_header_labelframe, text="Baseline:", anchor="w")
        self.ff_label_baseline_flag.place(x=5, y=155, width=80, height=20)
        self.ff_text_baseline_flag = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.ff_text_baseline_flag.place(x=105, y=155, width=180, height=20)
        self.ff_text_baseline_flag.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Orientation Flag
        self.ff_label_orientation_flag = tk.Label(self.file_header_labelframe, text="Orientation:", anchor="w")
        self.ff_label_orientation_flag.place(x=235, y=35, width=80, height=20)
        self.ff_text_orientation_flag = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.ff_text_orientation_flag.place(x=310, y=35, width=120, height=20)
        self.ff_text_orientation_flag.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Direction Flag
        self.ff_label_direction_flag = tk.Label(self.file_header_labelframe, text="Direction:", anchor="w")
        self.ff_label_direction_flag.place(x=235, y=65, width=80, height=20)
        self.ff_text_direction_flag = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.ff_text_direction_flag.place(x=310, y=65, width=120, height=20)
        self.ff_text_direction_flag.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Encoding Flag
        self.ff_label_encoding_flag = tk.Label(self.file_header_labelframe, text="Encoding:", anchor="w")
        self.ff_label_encoding_flag.place(x=235, y=95, width=80, height=20)
        self.ff_text_encoding_flag = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.ff_text_encoding_flag.place(x=310, y=95, width=120, height=20)
        self.ff_text_encoding_flag.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Format Flag
        self.ff_label_format_flag = tk.Label(self.file_header_labelframe, text="Format:", anchor="w")
        self.ff_label_format_flag.place(x=235, y=125, width=80, height=20)
        self.ff_text_format_flag = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.ff_text_format_flag.place(x=310, y=125, width=120, height=20)
        self.ff_text_format_flag.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))
