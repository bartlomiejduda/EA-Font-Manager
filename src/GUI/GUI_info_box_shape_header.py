import tkinter as tk

from src.GUI.right_clicker import RightClicker


class GuiShapeHeaderInfoBox(tk.Frame):
    def __init__(self, parent, gui_main):
        super().__init__(parent)

        # shape header box
        self.file_header_labelframe = tk.LabelFrame(parent, text="")
        self.file_header_labelframe.place(x=5, y=5, width=475, height=215)

        # Record ID
        self.sh_label_record_id = tk.Label(self.file_header_labelframe, text="Record ID:", anchor="w")
        self.sh_label_record_id.place(x=5, y=5, width=60, height=20)
        self.sh_text_record_id = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.sh_text_record_id.place(x=105, y=5, width=105, height=20)
        self.sh_text_record_id.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Next Binary Attachment Offset
        self.sh_label_next_binary_attachment_offset = tk.Label(
            self.file_header_labelframe, text="Next Bin. Offset:", anchor="w"
        )
        self.sh_label_next_binary_attachment_offset.place(x=5, y=35, width=90, height=20)
        self.sh_text_next_binary_attachment_offset = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.sh_text_next_binary_attachment_offset.place(x=105, y=35, width=105, height=20)
        self.sh_text_next_binary_attachment_offset.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Image Width
        self.sh_label_image_width = tk.Label(self.file_header_labelframe, text="Image Width:", anchor="w")
        self.sh_label_image_width.place(x=5, y=65, width=90, height=20)
        self.sh_text_image_width = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.sh_text_image_width.place(x=105, y=65, width=105, height=20)
        self.sh_text_image_width.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Image Height
        self.sh_label_image_height = tk.Label(self.file_header_labelframe, text="Image Height:", anchor="w")
        self.sh_label_image_height.place(x=5, y=95, width=90, height=20)
        self.sh_text_image_height = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.sh_text_image_height.place(x=105, y=95, width=105, height=20)
        self.sh_text_image_height.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Center X
        self.sh_label_center_x = tk.Label(self.file_header_labelframe, text="Center X:", anchor="w")
        self.sh_label_center_x.place(x=235, y=5, width=90, height=20)
        self.sh_text_center_x = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.sh_text_center_x.place(x=310, y=5, width=120, height=20)
        self.sh_text_center_x.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Center Y
        self.sh_label_center_y = tk.Label(self.file_header_labelframe, text="Center Y:", anchor="w")
        self.sh_label_center_y.place(x=235, y=35, width=90, height=20)
        self.sh_text_center_y = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.sh_text_center_y.place(x=310, y=35, width=120, height=20)
        self.sh_text_center_y.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Shape X
        self.sh_label_shape_x = tk.Label(self.file_header_labelframe, text="Shape X:", anchor="w")
        self.sh_label_shape_x.place(x=235, y=65, width=90, height=20)
        self.sh_text_shape_x = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.sh_text_shape_x.place(x=310, y=65, width=120, height=20)
        self.sh_text_shape_x.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Shape Y
        self.sh_label_shape_y = tk.Label(self.file_header_labelframe, text="Shape Y:", anchor="w")
        self.sh_label_shape_y.place(x=235, y=95, width=90, height=20)
        self.sh_text_shape_y = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.sh_text_shape_y.place(x=310, y=95, width=120, height=20)
        self.sh_text_shape_y.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Extra Fields Below

        # Image Type
        self.sh_label_image_type = tk.Label(self.file_header_labelframe, text="Image Type:", anchor="w")
        self.sh_label_image_type.place(x=5, y=125, width=90, height=20)
        self.sh_text_image_type = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.sh_text_image_type.place(x=105, y=125, width=325, height=20)
        self.sh_text_image_type.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Mipmaps Count
        self.sh_label_mipmaps = tk.Label(self.file_header_labelframe, text="Mipmaps:", anchor="w")
        self.sh_label_mipmaps.place(x=5, y=155, width=90, height=20)
        self.sh_text_mipmaps = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.sh_text_mipmaps.place(x=105, y=155, width=105, height=20)
        self.sh_text_mipmaps.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Image compression
        self.sh_label_image_comp = tk.Label(self.file_header_labelframe, text="IMG Comp:", anchor="w")
        self.sh_label_image_comp.place(x=235, y=155, width=90, height=20)
        self.sh_text_image_comp = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.sh_text_image_comp.place(x=310, y=155, width=120, height=20)
        self.sh_text_image_comp.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Swizzle Flag
        self.sh_label_flag_swizzle = tk.Label(self.file_header_labelframe, text="Swizzle Flag:", anchor="w")
        self.sh_label_flag_swizzle.place(x=5, y=185, width=90, height=20)
        self.sh_text_flag_swizzle = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.sh_text_flag_swizzle.place(x=105, y=185, width=105, height=20)
        self.sh_text_flag_swizzle.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))

        # Image BPP
        self.sh_label_image_bpp = tk.Label(self.file_header_labelframe, text="Image bpp:", anchor="w")
        self.sh_label_image_bpp.place(x=235, y=185, width=90, height=20)
        self.sh_text_image_bpp = tk.Text(
            self.file_header_labelframe,
            bg=self.file_header_labelframe["bg"],
            state="disabled",
        )
        self.sh_text_image_bpp.place(x=310, y=185, width=120, height=20)
        self.sh_text_image_bpp.bind("<Button-3>", lambda event, arg=self: RightClicker(arg, event))
