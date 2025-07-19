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
