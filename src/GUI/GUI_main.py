"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import io
import os
import tkinter as tk
from configparser import ConfigParser
from dataclasses import fields
from tkinter import filedialog, messagebox

from reversebox.common.common import convert_int_to_hex_string
from reversebox.common.logger import get_logger
from reversebox.compression.compression_refpack import RefpackHandler

from src.EA_Font.constants import (
    NEW_SHAPE_ALLOWED_SIGNATURES,
    OLD_SHAPE_ALLOWED_SIGNATURES,
    baseline_flags_mapping,
    direction_flags_mapping,
    encoding_flags_mapping,
    format_flags_mapping,
    orientation_flags_mapping,
)
from src.EA_Font.ea_font_file import EAFontFile
from src.EA_Font.font_dto.character12_entry import Character12Entry
from src.GUI.about_window import AboutWindow
from src.GUI.GUI_characters_table import GuiCharactersTable
from src.GUI.GUI_entry_preview import GuiEntryPreview
from src.GUI.GUI_menu import GuiMenu
from src.GUI.GUI_tab_controller import GuiTabController

# default app settings
WINDOW_HEIGHT = 460
WINDOW_WIDTH = 950
MIN_WINDOW_HEIGHT = WINDOW_HEIGHT
MIN_WINDOW_WIDTH = WINDOW_WIDTH
MAX_WINDOW_HEIGHT = WINDOW_HEIGHT
MAX_WINDOW_WIDTH = WINDOW_WIDTH


logger = get_logger(__name__)


# fmt: off

class EAManGui:
    def __init__(self, master, in_version_num, in_main_directory):
        logger.info("GUI init...")
        self.master = master
        self.VERSION_NUM = in_version_num
        self.MAIN_DIRECTORY = in_main_directory
        master.title("EA FONT MANAGER " + in_version_num)
        master.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        master.maxsize(MAX_WINDOW_WIDTH, MAX_WINDOW_HEIGHT)
        master.resizable(width=0, height=0)
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.tree_rclick_popup = None
        self.icon_path = self.MAIN_DIRECTORY + "\\data\\img\\ea_icon.ico"
        self.checkmark_path = self.MAIN_DIRECTORY + "\\data\\img\\checkmark.png"
        self.checkmark_image = None
        self.current_mipmaps_resampling = tk.StringVar(value="nearest")
        self.ea_font_file: EAFontFile = EAFontFile()

        try:
            self.master.iconbitmap(self.icon_path)
        except tk.TclError:
            logger.error(f"Can't load the icon file from {self.icon_path}")

        self.allowed_filetypes = [
            (
                "EA Font files",
                ["*.ffn", "*.pfn", "*.xfn", "*.mfn", "*.sfn",],
            ),
            ("All files", ["*.*"]),
        ]

        self.allowed_import_image_filetypes = [
            (
                "Image files",
                ["*.dds", "*.png", "*.bmp"],
            ),
            ("All files", ["*.*"]),
        ]

        self.ea_image_id = 0
        self.opened_ea_images_count = 0
        self.opened_ea_images = []

        # main frame
        self.main_frame = tk.Frame(master, bg="#f0f0f0")
        self.main_frame.place(x=0, y=0, relwidth=1, relheight=1)

        # gui objects
        self.entry_preview = GuiEntryPreview(self.main_frame, self)
        self.tab_controller = GuiTabController(self.main_frame, self)
        self.character_table = GuiCharactersTable(self.main_frame, self)
        self.menu = GuiMenu(self.master, self)
        self.loading_label = None

        # user config
        self.user_config = ConfigParser()
        self.user_config_file_name: str = "config.ini"
        self.user_config.add_section("config")
        self.user_config.set("config", "save_directory_path", "")
        self.user_config.set("config", "open_directory_path", "")
        if not os.path.exists(self.user_config_file_name):
            with open(self.user_config_file_name, "w") as configfile:
                self.user_config.write(configfile)

        self.user_config.read(self.user_config_file_name)
        try:
            self.current_save_directory_path = self.user_config.get("config", "save_directory_path")
            self.current_open_directory_path = self.user_config.get("config", "open_directory_path")
        except Exception as error:
            logger.error(f"Error while loading user config: {error}")
            self.current_save_directory_path = ""
            self.current_open_directory_path = ""

    ######################################################################################################
    #                                             methods                                                #
    ######################################################################################################

    def quit_program(self):
        logger.info("Quit GUI...")
        self.master.destroy()

    def open_file(self):
        try:
            in_file = filedialog.askopenfile(
                filetypes=self.allowed_filetypes, mode="rb", initialdir=self.current_open_directory_path
            )
            if not in_file:
                return
            try:
                selected_directory = os.path.dirname(in_file.name)
            except Exception:
                selected_directory = ""
            self.current_open_directory_path = selected_directory  # set directory path from history
            self.user_config.set(
                "config", "open_directory_path", selected_directory
            )  # save directory path to config file
            with open(self.user_config_file_name, "w") as configfile:
                self.user_config.write(configfile)
            in_file_path = in_file.name
            in_file_name = in_file_path.split("/")[-1]
        except Exception as error:
            logger.error(f"Failed to open file! Error: {error}")
            messagebox.showwarning("Warning", "Failed to open file!")
            return

        self.ea_font_file: EAFontFile = EAFontFile()

        # Refpack check
        sign: bytes = in_file.read(2)
        if sign == b"\x10\xFB":
            in_file.seek(0)
            in_file_data: bytes = in_file.read()
            in_file = io.BytesIO(
                RefpackHandler().decompress_data(in_file_data)
            )  # convert on-disk file to memory file with decompressed data
            self.ea_font_file.is_total_f_data_compressed = True
        in_file.seek(0)
        check_result = self.ea_font_file.check_file_signature(in_file)

        # save data for later export
        self.ea_font_file.total_f_data = in_file.read()
        in_file.seek(0)

        if check_result[0] != "OK":
            error_msg = "ERROR: " + str(check_result[0]) + "\n" + str(check_result[1]) + "\n\n" + "File not supported!"
            messagebox.showwarning("Warning", error_msg)
            return

        logger.info(f"Loading file {in_file_name}...")

        # Parse EA Font File
        self.ea_font_file.parse_file_header(in_file, in_file_path, in_file_name)
        self.ea_font_file.parse_font_flags()
        self.ea_font_file.parse_directory(in_file)
        self.ea_font_file.parse_bin_attachments(in_file)
        self.ea_font_file.convert_images(self)
        self.ea_font_file.parse_character_table(in_file)

        # image preview logic START
        try:
            self.entry_preview.preview_instance.destroy()
        except Exception:
            pass

        if self.ea_font_file.dir_entry_list[0].is_img_convert_supported:
            self.entry_preview.init_image_preview_logic(self.ea_font_file.dir_entry_list[0], "preview_item_iid")

        else:
            self.entry_preview.init_image_preview_not_supported_logic()
        # image preview logic END

        # set text for header
        if self.ea_font_file.fh_sign in OLD_SHAPE_ALLOWED_SIGNATURES:
            # set file header fields
            self.set_text_in_box(self.tab_controller.file_header_info_box.fh_text_sign, self.ea_font_file.fh_sign)
            self.set_text_in_box(self.tab_controller.file_header_info_box.fh_text_total_f_size, self.ea_font_file.fh_total_f_size)
            self.set_text_in_box(self.tab_controller.file_header_info_box.fh_text_version, self.ea_font_file.fh_file_version)
            self.set_text_in_box(self.tab_controller.file_header_info_box.fh_text_number_of_characters, self.ea_font_file.fh_num_of_characters)
            self.set_text_in_box(self.tab_controller.file_header_info_box.fh_text_font_flags, self.ea_font_file.fh_font_flags)
            self.set_text_in_box(self.tab_controller.file_header_info_box.fh_text_char_info_offset, self.ea_font_file.fh_char_info_offset)
            self.set_text_in_box(self.tab_controller.file_header_info_box.fh_text_center_x, self.ea_font_file.fh_center_x)
            self.set_text_in_box(self.tab_controller.file_header_info_box.fh_text_center_y, self.ea_font_file.fh_center_y)
            self.set_text_in_box(self.tab_controller.file_header_info_box.fh_text_ascent, self.ea_font_file.fh_ascent)
            self.set_text_in_box(self.tab_controller.file_header_info_box.fh_text_descent, self.ea_font_file.fh_descent)
            self.set_text_in_box(self.tab_controller.file_header_info_box.fh_text_kerning_table_offset, self.ea_font_file.fh_kerning_table_offset)
            self.set_text_in_box(self.tab_controller.file_header_info_box.fh_text_shape_header_offset, self.ea_font_file.fh_shape_header_offset)

            # set shape header fields
            self.set_text_in_box(self.tab_controller.shape_header_info_box.sh_text_record_id, self.ea_font_file.dir_entry_list[0].h_record_id)
            self.set_text_in_box(self.tab_controller.shape_header_info_box.sh_text_next_binary_attachment_offset, self.ea_font_file.dir_entry_list[0].h_size_of_the_block)
            self.set_text_in_box(self.tab_controller.shape_header_info_box.sh_text_image_width, self.ea_font_file.dir_entry_list[0].h_width)
            self.set_text_in_box(self.tab_controller.shape_header_info_box.sh_text_image_height, self.ea_font_file.dir_entry_list[0].h_height)
            self.set_text_in_box(self.tab_controller.shape_header_info_box.sh_text_center_x, self.ea_font_file.dir_entry_list[0].h_center_x)
            self.set_text_in_box(self.tab_controller.shape_header_info_box.sh_text_center_y, self.ea_font_file.dir_entry_list[0].h_center_y)
            self.set_text_in_box(self.tab_controller.shape_header_info_box.sh_text_shape_x, self.ea_font_file.dir_entry_list[0].h_default_x_position)
            self.set_text_in_box(self.tab_controller.shape_header_info_box.sh_text_shape_y, self.ea_font_file.dir_entry_list[0].h_default_y_position)

            self.set_text_in_box(self.tab_controller.shape_header_info_box.sh_text_image_type, self.ea_font_file.dir_entry_list[0].get_entry_type())
            self.set_text_in_box(self.tab_controller.shape_header_info_box.sh_text_mipmaps, self.ea_font_file.dir_entry_list[0].h_mipmaps_count)
            self.set_text_in_box(self.tab_controller.shape_header_info_box.sh_text_image_comp, self.ea_font_file.dir_entry_list[0].h_is_image_compressed_masked)
            self.set_text_in_box(self.tab_controller.shape_header_info_box.sh_text_flag_swizzle, self.ea_font_file.dir_entry_list[0].h_flag2_swizzled)
            self.set_text_in_box(self.tab_controller.shape_header_info_box.sh_text_image_bpp, self.ea_font_file.dir_entry_list[0].h_image_bpp)

            # set font flags fields
            self.set_text_in_box(self.tab_controller.font_flags_info_box.ff_text_flags_dec, self.ea_font_file.fh_font_flags)
            self.set_text_in_box(self.tab_controller.font_flags_info_box.ff_text_flags_hex, convert_int_to_hex_string(self.ea_font_file.fh_font_flags))
            self.set_text_in_box(self.tab_controller.font_flags_info_box.ff_text_antialiased_flag, self.get_text_for_bool_flag(self.ea_font_file.ff_antialiased))
            self.set_text_in_box(self.tab_controller.font_flags_info_box.ff_text_dropshadow_flag, self.get_text_for_bool_flag(self.ea_font_file.ff_dropshadow))
            self.set_text_in_box(self.tab_controller.font_flags_info_box.ff_text_outline_flag, self.get_text_for_bool_flag(self.ea_font_file.ff_outline))
            self.set_text_in_box(self.tab_controller.font_flags_info_box.ff_text_vram_flag, self.get_text_for_bool_flag(self.ea_font_file.ff_vram))
            self.set_text_in_box(self.tab_controller.font_flags_info_box.ff_text_baseline_flag, self.get_text_for_baseline_flag(self.ea_font_file.ff_baseline))
            self.set_text_in_box(self.tab_controller.font_flags_info_box.ff_text_orientation_flag, self.get_text_for_orientation_flag(self.ea_font_file.ff_orientation))
            self.set_text_in_box(self.tab_controller.font_flags_info_box.ff_text_direction_flag, self.get_text_for_direction_flag(self.ea_font_file.ff_direction))
            self.set_text_in_box(self.tab_controller.font_flags_info_box.ff_text_encoding_flag, self.get_text_for_encoding_flag(self.ea_font_file.ff_encoding))
            self.set_text_in_box(self.tab_controller.font_flags_info_box.ff_text_format_flag, self.get_text_for_format_flag(self.ea_font_file.ff_format))

        elif self.ea_font_file.fh_sign in NEW_SHAPE_ALLOWED_SIGNATURES:
            raise Exception("New shapes not supported yet!")
        else:
            raise Exception("Not supported signature!")

        # set character table
        if self.ea_font_file.ff_format == 0:  # Character12
            self.character_table.character_table.headers(["Char Index", "Width", "Height", "U", "V", "Advance", "X-Offset", "Y-Offset", "NumKern"])
            self.character_table.character_table.column_width(0, 120)  # char index

            char_data = [[chr(getattr(char12, f.name)) if f.name == "index" else getattr(char12, f.name) for f in fields(Character12Entry)]
                    for char12 in self.ea_font_file.character_entry_list]
            self.character_table.character_table.set_sheet_data(char_data)

        elif self.ea_font_file.ff_format == 1:  # Character16
            self.character_table.character_table.headers(["Char Index", "Width", "Height", "U", "V", "AdvanceY", "X-Offset", "Y-Offset", "NumKern", "KernIndex", "AdvanceX"])
        else:
            raise Exception("Unknown format flag value!")

        in_file.close()
        return  # file opened successfully

    def show_about_window(self):
        if not any(isinstance(x, tk.Toplevel) for x in self.master.winfo_children()):
            AboutWindow(self)

    @staticmethod
    def set_text_in_box(in_box, in_text):
        in_box.config(state="normal")
        in_box.delete("1.0", tk.END)
        in_box.insert(tk.END, in_text)
        in_box.config(state="disabled")

    @staticmethod
    def get_text_for_bool_flag(flag_value: int) -> str:
        if flag_value == 0:
            return "false"
        elif flag_value == 1:
            return "true"
        else:
            raise Exception("Not supported flag value!")

    @staticmethod
    def get_text_for_baseline_flag(flag_value: int) -> str:
        return baseline_flags_mapping[flag_value]

    @staticmethod
    def get_text_for_orientation_flag(flag_value: int) -> str:
        return orientation_flags_mapping[flag_value]

    @staticmethod
    def get_text_for_direction_flag(flag_value: int) -> str:
        return direction_flags_mapping[flag_value]

    @staticmethod
    def get_text_for_encoding_flag(flag_value: int) -> str:
        return encoding_flags_mapping[flag_value]

    @staticmethod
    def get_text_for_format_flag(flag_value: int) -> str:
        return format_flags_mapping[flag_value]

    @staticmethod
    def close_toplevel_window(wind):
        wind.destroy()
