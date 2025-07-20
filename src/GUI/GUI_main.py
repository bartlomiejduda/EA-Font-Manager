"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import io
import os
import subprocess
import tkinter as tk
import traceback
from configparser import ConfigParser
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Optional

from PIL import Image, ImageTk
from reversebox.common.common import get_file_extension, get_file_extension_uppercase
from reversebox.common.logger import get_logger
from reversebox.compression.compression_refpack import RefpackHandler
from reversebox.image.pillow_wrapper import PillowWrapper

from src.EA_Font import ea_image_main
from src.EA_Font.attachments.palette_entry import PaletteEntry
from src.EA_Font.constants import (
    CONVERT_IMAGES_SUPPORTED_TYPES,
    IMPORT_IMAGES_SUPPORTED_TYPES,
    NEW_SHAPE_ALLOWED_SIGNATURES,
    OLD_SHAPE_ALLOWED_SIGNATURES,
    PALETTE_TYPES,
)
from src.EA_Font.dto import EncodeInfoDTO
from src.EA_Font.ea_image_encoder import encode_ea_image
from src.EA_Font.ea_image_main import EAImage
from src.GUI.GUI_tab_controller import GuiTabController
from src.GUI.about_window import AboutWindow
from src.GUI.GUI_entry_preview import GuiEntryPreview
from src.GUI.GUI_menu import GuiMenu

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

        ea_img: EAImage = ea_image_main.EAImage()
        sign: bytes = in_file.read(2)
        if sign == b"\x10\xFB":
            in_file.seek(0)
            in_file_data: bytes = in_file.read()
            in_file = io.BytesIO(
                RefpackHandler().decompress_data(in_file_data)
            )  # convert on-disk file to memory file with decompressed data
            ea_img.is_total_f_data_compressed = True
        in_file.seek(0)
        check_result = ea_img.check_file_signature_and_size(in_file)

        # save data for later export
        ea_img.total_f_data = in_file.read()
        in_file.seek(0)

        if check_result[0] != "OK":
            error_msg = "ERROR: " + str(check_result[0]) + "\n" + str(check_result[1]) + "\n\n" + "File not supported!"
            messagebox.showwarning("Warning", error_msg)
            return

        logger.info(f"Loading file {in_file_name}...")

        self.ea_image_id += 1
        self.opened_ea_images_count += 1
        ea_img.set_ea_image_id(self.ea_image_id)
        self.opened_ea_images.append(ea_img)

        ea_img.parse_header(in_file, in_file_path, in_file_name)
        ea_img.parse_directory(in_file)

        # check if there are any bin attachments
        # and add them to the list if found
        ea_img.parse_bin_attachments(in_file)

        # convert all supported images
        # in the ea_img file
        try:
            logger.info("Starting processing with convert_images function")
            self.loading_label = tk.Label(self.main_frame, text="Loading... Please wait.", font=("Arial", 14))
            if ea_img.total_f_size > 200000:
                self.loading_label.place(x=0, y=0, relwidth=1, relheight=1)
                self.loading_label.update()
            ea_img.convert_images(self)
            self.loading_label.destroy()
        except Exception as error:
            logger.error(f"Error while converting images! Error: {error}")
            logger.error(traceback.format_exc())

            # set text for header
            if ea_img.sign in OLD_SHAPE_ALLOWED_SIGNATURES:
                self.set_text_in_box(self.tab_controller.file_header_info_box.fh_text_sign, ea_img.sign)
                self.set_text_in_box(self.tab_controller.file_header_info_box.fh_text_f_size, ea_img.total_f_size)
                self.set_text_in_box(self.tab_controller.file_header_info_box.fh_text_obj_count, ea_img.num_of_entries)
                self.set_text_in_box(self.tab_controller.file_header_info_box.fh_text_dir_id, ea_img.format_version)
                self._execute_old_shape_tab_logic()
            elif ea_img.sign in NEW_SHAPE_ALLOWED_SIGNATURES:
                self.set_text_in_box(self.tab_controller.shape_header_info_box.fh_text_sign, ea_img.sign)
                self.set_text_in_box(self.tab_controller.shape_header_info_box.fh_text_f_size, ea_img.total_f_size)
                self.set_text_in_box(self.tab_controller.shape_header_info_box.fh_text_obj_count, ea_img.num_of_entries)
                self.set_text_in_box(self.tab_controller.shape_header_info_box.fh_text_header_and_toc_size, ea_img.header_and_toc_size)
                self._execute_new_shape_tab_logic()

            # set text for the first entry
            if ea_img.sign in OLD_SHAPE_ALLOWED_SIGNATURES:
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_rec_type, ea_img.dir_entry_list[0].get_entry_type())
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_size_of_the_block, ea_img.dir_entry_list[0].h_size_of_the_block)
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_mipmaps_count, ea_img.dir_entry_list[0].h_mipmaps_count)
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_width, ea_img.dir_entry_list[0].h_width)
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_height, ea_img.dir_entry_list[0].h_height)
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_center_x, ea_img.dir_entry_list[0].h_center_x)
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_center_y, ea_img.dir_entry_list[0].h_center_y)
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_left_x, ea_img.dir_entry_list[0].h_default_x_position)
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_top_y, ea_img.dir_entry_list[0].h_default_y_position)
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_entry_header_offset, ea_img.dir_entry_list[0].h_entry_header_offset)
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_data_offset, ea_img.dir_entry_list[0].raw_data_offset)
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_data_size, ea_img.dir_entry_list[0].raw_data_size)
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_entry_end_offset, ea_img.dir_entry_list[0].h_entry_end_offset)
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_entry_record_id_masked, ea_img.dir_entry_list[0].h_record_id_masked)
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_entry_img_compression_masked, ea_img.dir_entry_list[0].h_is_image_compressed_masked)
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_entry_flag1_referenced, ea_img.dir_entry_list[0].h_flag1_referenced)
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_entry_flag2_swizzled, ea_img.dir_entry_list[0].h_flag2_swizzled)
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_entry_flag3_transposed, ea_img.dir_entry_list[0].h_flag3_transposed)
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_entry_flag4_reserved, ea_img.dir_entry_list[0].h_flag4_reserved)
                self.set_text_in_box(self.tab_controller.entry_header_info_box.eh_text_entry_image_bpp, ea_img.dir_entry_list[0].h_image_bpp)
                self._execute_old_shape_tab_logic()
            elif ea_img.sign in NEW_SHAPE_ALLOWED_SIGNATURES:
                self.set_text_in_box(self.tab_controller.new_shape_entry_header_info_box.eh_text_rec_type, ea_img.dir_entry_list[0].get_entry_type())
                self.set_text_in_box(self.tab_controller.new_shape_entry_header_info_box.eh_text_size_of_the_block, ea_img.dir_entry_list[0].h_size_of_the_block)
                self.set_text_in_box(self.tab_controller.new_shape_entry_header_info_box.eh_text_width, ea_img.dir_entry_list[0].h_width)
                self.set_text_in_box(self.tab_controller.new_shape_entry_header_info_box.eh_text_height, ea_img.dir_entry_list[0].h_height)
                self.set_text_in_box(self.tab_controller.new_shape_entry_header_info_box.eh_text_left_x, ea_img.dir_entry_list[0].h_default_x_position)
                self.set_text_in_box(self.tab_controller.new_shape_entry_header_info_box.eh_text_top_y, ea_img.dir_entry_list[0].h_default_y_position)
                self.set_text_in_box(self.tab_controller.new_shape_entry_header_info_box.eh_text_entry_image_bpp, ea_img.dir_entry_list[0].h_image_bpp)
                self.set_text_in_box(self.tab_controller.new_shape_entry_header_info_box.eh_text_mipmaps_count, ea_img.dir_entry_list[0].new_shape_number_of_mipmaps)
                self.set_text_in_box(self.tab_controller.new_shape_entry_header_info_box.eh_text_flags_int, ea_img.dir_entry_list[0].new_shape_flags)
                self.set_text_in_box(self.tab_controller.new_shape_entry_header_info_box.eh_text_flags_hex_str, ea_img.dir_entry_list[0].new_shape_flags_hex_str)
                self.set_text_in_box(self.tab_controller.new_shape_entry_header_info_box.eh_text_entry_header_offset, ea_img.dir_entry_list[0].h_entry_header_offset)
                self.set_text_in_box(self.tab_controller.new_shape_entry_header_info_box.eh_text_data_offset, ea_img.dir_entry_list[0].raw_data_offset)
                self.set_text_in_box(self.tab_controller.new_shape_entry_header_info_box.eh_text_entry_end_offset, ea_img.dir_entry_list[0].h_entry_end_offset)
                self.set_text_in_box(self.tab_controller.new_shape_entry_header_info_box.eh_text_data_size, ea_img.dir_entry_list[0].raw_data_size)
                self.set_text_in_box(self.tab_controller.new_shape_entry_header_info_box.eh_text_entry_flag_new_format, ea_img.dir_entry_list[0].new_shape_flag_new_format)
                self.set_text_in_box(self.tab_controller.new_shape_entry_header_info_box.eh_text_entry_flag_compressed, ea_img.dir_entry_list[0].new_shape_flag_compressed)
                self.set_text_in_box(self.tab_controller.new_shape_entry_header_info_box.eh_text_entry_flag_swizzled, ea_img.dir_entry_list[0].new_shape_flag_swizzled)
                self._execute_new_shape_tab_logic()

        self.tree_view.tree_man.add_object(ea_img)
        in_file.close()

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
    def close_toplevel_window(wind):
        wind.destroy()

# fmt: on
