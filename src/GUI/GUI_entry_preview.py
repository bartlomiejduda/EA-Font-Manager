import math
import tkinter as tk
from typing import Optional

from PIL import Image, ImageTk
from reversebox.common.logger import get_logger

from src.EA_Font.attachments.palette_entry import PaletteEntry

logger = get_logger(__name__)


# fmt: off

class GuiEntryPreview(tk.Frame):
    def __init__(self, parent, gui_main):
        super().__init__(parent)

        self.gui_main = gui_main
        self.preview_labelframe_width = 440
        self.preview_labelframe_height = 250
        self.canvas_height = self.preview_labelframe_height - 30
        self.canvas_width = self.preview_labelframe_width - 20
        self.preview_labelframe = tk.LabelFrame(parent, text="Preview")
        self.preview_labelframe.place(x=500, y=5, width=self.preview_labelframe_width, height=self.preview_labelframe_height)

        self.ph_img = None
        self.ea_dir = None
        self.canvas_image_id: Optional[int] = None
        self.red_rectangle_id: Optional[int] = None
        self.ratio: float = 1.0
        self.preview_instance: Optional[tk.Canvas] = None

    def init_image_preview_logic(self, ea_dir, item_iid):
        if not ea_dir.img_convert_data or len(ea_dir.img_convert_data) == 0:
            logger.error(f"Preview failed for {str(item_iid)}, because converted image data is empty!")
            return

        self.ea_dir = ea_dir

        try:
            pil_img = Image.frombuffer(
                "RGBA",
                (int(ea_dir.h_width), int(ea_dir.h_height)),
                ea_dir.img_convert_data,
                "raw",
                "RGBA",
                0,
                1,
            )

            # resize preview logic
            if pil_img.height >= pil_img.width:
                if pil_img.height > self.canvas_height:
                    self.ratio = self.canvas_height / pil_img.height
                    resized_height: int = int(pil_img.height * self.ratio)
                    resized_width: int = int(pil_img.width * self.ratio)
                    pil_img = pil_img.resize((resized_width, resized_height))
            else:
                if pil_img.width > self.canvas_width:
                    self.ratio = self.canvas_width / pil_img.width
                    resized_height: int = int(pil_img.height * self.ratio)
                    resized_width: int = int(pil_img.width * self.ratio)
                    pil_img = pil_img.resize((resized_width, resized_height))

            self.ph_img = ImageTk.PhotoImage(pil_img)

            self.preview_instance = tk.Canvas(
                self.preview_labelframe,
                bg="#595959",
                width=self.canvas_width,
                height=self.canvas_height,
            )
            self.canvas_image_id = self.preview_instance.create_image(
                int(self.canvas_width / 2),
                int(self.canvas_height / 2),
                anchor="center",
                image=self.ph_img,
            )
            self.preview_instance.place(x=5, y=5)

        except Exception as error:
            logger.error(f"Error occurred while generating preview for {str(item_iid)}... Error: {error}")

    def init_image_preview_not_supported_logic(self):
        preview_text = "Preview for this image type is not supported..."
        self.preview_instance = tk.Label(
            self.preview_labelframe,
            text=preview_text,
            anchor="nw",
            justify="left",
            wraplength=300,
        )
        self.preview_instance.place(x=5, y=5, width=285, height=130)

    def init_binary_preview_logic(self, bin_attachment):
        preview_hex_string = bin_attachment.raw_data.decode("utf8", "backslashreplace").replace("\000", ".")[
            0:200
        ]  # limit preview to 200 characters
        self.preview_instance = tk.Label(
            self.preview_labelframe,
            text=preview_hex_string,
            anchor="nw",
            justify="left",
            wraplength=300,
        )
        self.preview_instance.place(x=5, y=5, width=285, height=130)

    def init_palette_preview_logic(self, palette_entry: PaletteEntry):
        palette_width: int = palette_entry.h_width
        palette_height: int = palette_entry.h_height

        try:
            pil_img = Image.frombuffer(
                "RGBA",
                (math.ceil(palette_width / 2), math.ceil(palette_height / 2)),
                palette_entry.raw_data,
                "raw",
                "RGBA",
                0,
                1,
            )

            if pil_img.height > self.canvas_height:
                ratio = self.canvas_height / pil_img.height
                pil_img = pil_img.resize((int(pil_img.width * ratio), self.canvas_height))
            elif pil_img.height < 50:
                pil_img = pil_img.resize((int(pil_img.width * 6), int(pil_img.height * 6)))

            self.ph_img = ImageTk.PhotoImage(pil_img)

            self.preview_instance = tk.Canvas(
                self.preview_labelframe,
                bg="#595959",
                width=self.canvas_width,
                height=self.canvas_height,
            )
            self.preview_instance.create_image(
                self.canvas_width / 2,
                self.canvas_height / 2,
                anchor="center",
                image=self.ph_img,
            )
            self.preview_instance.place(x=5, y=5)

        except Exception as error:
            logger.error(f"Error occurred while generating preview palette... Error: {error}")

    def draw_red_rectangle(self, selected_row_data: list) -> None:
        if self.gui_main.ea_font_file.ff_format == 0:  # Character12
            width = selected_row_data[1]
            height = selected_row_data[2]
            u = selected_row_data[3]
            v = selected_row_data[4]
        else:
            raise Exception("Character format not supported!")

        if self.preview_instance and self.canvas_image_id:
            if self.red_rectangle_id:
                self.preview_instance.delete(self.red_rectangle_id)
            img_center_x, img_center_y = self.preview_instance.coords(self.canvas_image_id)
            img_x = int(img_center_x) - (self.ea_dir.h_width * self.ratio) // 2
            img_y = int(img_center_y) - (self.ea_dir.h_height * self.ratio) // 2

            rect_x = int(u * self.ratio) + img_x
            rect_y = int(v * self.ratio) + img_y
            rect_x2 = int((u + width) * self.ratio) + img_x
            rect_y2 = int((v + height) * self.ratio) + img_y

            self.red_rectangle_id = self.preview_instance.create_rectangle(rect_x, rect_y, rect_x2, rect_y2, fill="", outline="red")
