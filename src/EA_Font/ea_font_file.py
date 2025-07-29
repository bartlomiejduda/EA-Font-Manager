"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import os
import struct
import traceback
from typing import Optional, Union

from reversebox.common.logger import get_logger
from reversebox.compression.compression_refpack import RefpackHandler
from reversebox.io_files.bytes_helper_functions import get_bits

from src.EA_Font.attachments.comment_entry import CommentEntry
from src.EA_Font.attachments.hot_spot_entry import HotSpotEntry
from src.EA_Font.attachments.img_name_entry import ImgNameEntry
from src.EA_Font.attachments.metal_bin_entry import MetalBinEntry
from src.EA_Font.attachments.palette_entry import PaletteEntry
from src.EA_Font.attachments.unknown_entry import UnknownEntry
from src.EA_Font.common_ea_dir import (
    get_palette_info_dto_from_dir_entry,
    handle_image_swizzle_logic,
    is_image_compressed,
    is_image_swizzled,
)
from src.EA_Font.constants import (
    CONVERT_IMAGES_SUPPORTED_TYPES,
    OLD_SHAPE_ALLOWED_SIGNATURES,
    PALETTE_TYPES,
)
from src.EA_Font.data_read import get_string, get_uint8, get_uint16, get_uint32
from src.EA_Font.dir_entry import DirEntry
from src.EA_Font.dto import PaletteInfoDTO
from src.EA_Font.ea_image_decoder import decode_image_data_by_entry_type
from src.EA_Font.font_dto.character12_entry import Character12Entry
from src.EA_Font.font_dto.character16_entry import Character16Entry

logger = get_logger(__name__)


class EAFontFile:
    def __init__(self):

        # file header fields
        self.fh_sign: Optional[str] = None
        self.fh_total_f_size: Optional[int] = None
        self.fh_file_version: Optional[int] = None
        self.fh_num_of_characters: Optional[int] = None
        self.fh_font_flags: Optional[int] = None
        self.fh_center_x: Optional[int] = None
        self.fh_center_y: Optional[int] = None
        self.fh_ascent: Optional[int] = None
        self.fh_descent: Optional[int] = None
        self.fh_char_info_offset: Optional[int] = None
        self.fh_kerning_table_offset: Optional[int] = None
        self.fh_shape_header_offset: Optional[int] = None

        # font flags fields
        self.ff_antialiased: Optional[int] = None
        self.ff_dropshadow: Optional[int] = None
        self.ff_outline: Optional[int] = None
        self.ff_vram: Optional[int] = None
        self.ff_baseline: Optional[int] = None
        self.ff_orientation: Optional[int] = None
        self.ff_direction: Optional[int] = None
        self.ff_encoding: Optional[int] = None
        self.ff_format: Optional[int] = None

        # data fields
        self.num_of_entries: int = 1
        self.dir_entry_id: int = 0
        self.dir_entry_list: list[DirEntry] = []
        self.character_entry_list: list[Union[Character12Entry, Character16Entry]] = []

        # local fields
        self.total_f_data: Optional[bytes] = None
        self.is_total_f_data_compressed: bool = False
        self.f_name = None
        self.f_path = None
        self.f_endianess = None
        self.f_dir_endianess = None
        self.f_endianess_desc = None
        self.f_size = None

    def check_file_signature(self, in_file) -> tuple:
        try:
            # checking signature
            back_offset = in_file.tell()
            sign = get_string(in_file, 4)
            in_file.seek(back_offset)
            if len(sign) == 0:
                error_msg = "File is empty. No data to read!"
                logger.info(error_msg)
                return "FILE_IS_EMPTY", error_msg
            if sign not in OLD_SHAPE_ALLOWED_SIGNATURES:
                error_msg = f'File signature "{sign}" is not supported'
                logger.info(error_msg)
                return "SIGN_NOT_SUPPORTED", error_msg

            return "OK", ""

        except Exception as error:
            error_msg = f"Can't read file signature or size! Error: {error}"
            logger.error(error_msg)
            return "CANT_READ_ERROR", error_msg

    def _set_big_endianess(self):
        self.f_endianess = ">"
        self.f_endianess_desc = "big"

    def _set_little_endianess(self):
        self.f_endianess = "<"
        self.f_endianess_desc = "little"

    def parse_file_header(self, in_file, in_file_path, in_file_name) -> None:
        self.f_path = in_file_path
        self.f_name = in_file_name
        self.f_size = os.path.getsize(self.f_path)
        self._set_little_endianess()

        self.fh_sign = get_string(in_file, 4)
        self.fh_total_f_size = get_uint32(in_file, self.f_endianess)
        self.fh_file_version = get_uint16(in_file, self.f_endianess)
        self.fh_num_of_characters = get_uint16(in_file, self.f_endianess)
        self.fh_font_flags = get_uint32(in_file, self.f_endianess)
        self.fh_center_x = get_uint8(in_file, self.f_endianess)
        self.fh_center_y = get_uint8(in_file, self.f_endianess)
        self.fh_ascent = get_uint8(in_file, self.f_endianess)
        self.fh_descent = get_uint8(in_file, self.f_endianess)
        self.fh_char_info_offset = get_uint32(in_file, self.f_endianess)
        self.fh_kerning_table_offset = get_uint32(in_file, self.f_endianess)
        self.fh_shape_header_offset = get_uint32(in_file, self.f_endianess)
        return  # header has been parsed

    def parse_font_flags(self) -> None:
        self.ff_antialiased = get_bits(self.fh_font_flags, 1, 0)
        self.ff_dropshadow = get_bits(self.fh_font_flags, 1, 1)
        self.ff_outline = get_bits(self.fh_font_flags, 1, 2)
        self.ff_vram = get_bits(self.fh_font_flags, 1, 3)
        self.ff_baseline = get_bits(self.fh_font_flags, 2, 8)
        self.ff_orientation = get_bits(self.fh_font_flags, 1, 10)
        self.ff_direction = get_bits(self.fh_font_flags, 1, 11)
        self.ff_encoding = get_bits(self.fh_font_flags, 2, 16)
        self.ff_format = get_bits(self.fh_font_flags, 1, 18)

    def parse_character_table(self, in_file) -> None:
        in_file.seek(self.fh_char_info_offset)
        if self.ff_format == 0:  # Character12
            for i in range(self.fh_num_of_characters):
                self.character_entry_list.append(
                    Character12Entry(
                        index=get_uint16(in_file, self.f_endianess),
                        width=get_uint8(in_file, self.f_endianess),
                        height=get_uint8(in_file, self.f_endianess),
                        u=get_uint16(in_file, self.f_endianess),
                        v=get_uint16(in_file, self.f_endianess),
                        advance=get_uint8(in_file, self.f_endianess),
                        x_offset=get_uint8(in_file, self.f_endianess),
                        y_offset=get_uint8(in_file, self.f_endianess),
                        num_kern=get_uint8(in_file, self.f_endianess) if self.fh_file_version >= 200 else None,
                    )
                )
        elif self.ff_format == 1:  # Character16
            pass
        else:
            raise Exception("Not supported format flag!")

    # ATTENTION! This function has been rewritten to match font files logic.
    # There should be only one dir entry for each font file.
    def parse_directory(self, in_file) -> bool:
        # creating directory entries

        in_file.seek(self.fh_shape_header_offset)
        for i in range(self.num_of_entries):
            self.dir_entry_id += 1
            entry_id = "img_id" + "_direntry_" + str(self.dir_entry_id)
            entry_start_offset = in_file.tell()
            entry_tag = "entry_tag_" + str(self.dir_entry_id)
            ea_dir_entry = DirEntry(entry_id, entry_tag, entry_start_offset)
            self.dir_entry_list.append(ea_dir_entry)  # dir entry is now initialized and can be added to the list

        self.dir_entry_list.sort(key=lambda d_entry: d_entry.start_offset)

        # updating end offset for each entry
        # and parsing DIR entry data
        entry_num = 0
        for i in range(self.num_of_entries):
            ea_dir_entry = self.dir_entry_list[i]
            entry_num += 1

            # set end offset for DIR entry
            if entry_num == self.num_of_entries:
                ea_dir_entry.end_offset = self.fh_total_f_size
            else:
                ea_dir_entry.end_offset = self.dir_entry_list[i + 1].start_offset

            in_file.seek(ea_dir_entry.start_offset)
            self.parse_dir_entry_header_and_data(in_file, ea_dir_entry)

        return True  # directory has been parsed

    def parse_dir_entry_header_and_data(self, in_file, ea_dir_entry) -> bool:
        ea_dir_entry.set_entry_header(in_file, self.f_endianess, self.fh_sign)  # read entry header and set all values

        ea_dir_entry.set_raw_data(
            in_file,
            ea_dir_entry.start_offset + ea_dir_entry.header_size,
            ea_dir_entry.end_offset,
        )  # read raw entry data and set values

        if self.fh_sign in OLD_SHAPE_ALLOWED_SIGNATURES:
            ea_dir_entry.set_is_image_compressed_masked(in_file)
        ea_dir_entry.set_img_end_offset()  # this value is known only after reading data

        return True

    def parse_bin_attachments(self, in_file) -> bool:
        for i in range(self.num_of_entries):
            ea_dir_entry = self.dir_entry_list[i]

            if (
                ea_dir_entry.if_next_entry_exist_flag is False
                and ea_dir_entry.start_offset + ea_dir_entry.h_size_of_the_block == ea_dir_entry.end_offset
            ):
                pass  # no binary attachments for this DIR entry
            else:
                # there are some binary attachments (1 or more)
                bin_att_id_count = 0
                in_file.seek(
                    ea_dir_entry.start_offset + ea_dir_entry.h_size_of_the_block
                )  # seek to offset of the first bin attachment

                # logic for entries with no attachments
                if in_file.tell() + ea_dir_entry.header_size >= ea_dir_entry.end_offset:
                    continue  # no more binary attachments for this DIR entry

                while 1:
                    bin_att_start_offset = in_file.tell()
                    bin_att_id_count += 1
                    bin_att_id = ea_dir_entry.id + "_binattach_" + str(bin_att_id_count)

                    bin_att_rec_id = struct.unpack(self.f_endianess + "B", in_file.read(1))[0]
                    in_file.seek(bin_att_start_offset)

                    if bin_att_rec_id == 105:
                        bin_att_entry = MetalBinEntry(bin_att_id, bin_att_start_offset)
                    elif bin_att_rec_id == 111:
                        bin_att_entry = CommentEntry(bin_att_id, bin_att_start_offset)
                    elif bin_att_rec_id == 112:
                        bin_att_entry = ImgNameEntry(bin_att_id, bin_att_start_offset)
                    elif bin_att_rec_id == 124:
                        bin_att_entry = HotSpotEntry(bin_att_id, bin_att_start_offset)
                    elif bin_att_rec_id in PALETTE_TYPES:
                        bin_att_entry = PaletteEntry(bin_att_id, bin_att_start_offset)
                    else:
                        bin_att_entry = UnknownEntry(bin_att_id, bin_att_start_offset)
                        logger.warning(f"Unknown bin attachment entry ({str(hex(bin_att_rec_id))})!")

                    bin_att_entry.set_tag(bin_att_rec_id)
                    bin_att_entry.set_entry_header(in_file, self.f_endianess, self.fh_sign)
                    bin_att_start_offset = in_file.tell()
                    bin_att_entry.set_raw_data(in_file, bin_att_start_offset, ea_dir_entry.end_offset)

                    bin_att_entry.start_offset = bin_att_start_offset
                    bin_att_entry.end_offset = in_file.tell()

                    ea_dir_entry.bin_attachments_list.append(bin_att_entry)  # binary attachment is now parsed
                    # and can be added to the list

                    if bin_att_entry.end_offset >= ea_dir_entry.end_offset:
                        break  # no more binary attachments for this DIR entry

        return True

    def convert_images(self, gui_main) -> bool:
        for i in range(self.num_of_entries):
            ea_dir_entry = self.dir_entry_list[i]
            entry_type = ea_dir_entry.h_record_id

            if entry_type not in CONVERT_IMAGES_SUPPORTED_TYPES:
                logger.warning(
                    f'Warning! Image "{ea_dir_entry.tag}" with entry type {str(entry_type)} is not supported for image conversion! Skipping!'
                )
                continue

            logger.info(
                f'Starting conversion for image {str(i+1)}, img_type={str(entry_type)}, img_tag="{ea_dir_entry.tag}"...'
            )
            ea_dir_entry.is_img_convert_supported = True
            self.convert_image_data_for_export_and_preview(ea_dir_entry, entry_type, gui_main)
            logger.info(
                f'Finished conversion for image {str(i + 1)}, img_type={str(entry_type)}, img_tag="{ea_dir_entry.tag}"...'
            )
        return True

    def convert_image_data_for_export_and_preview(self, ea_dir_entry: DirEntry, entry_type: int, gui_main) -> bool:
        image_data: bytes = ea_dir_entry.raw_data

        # decompress logic
        if is_image_compressed(entry_type):
            image_data = RefpackHandler().decompress_data(image_data)

        entry_type = entry_type & 0x7F

        # unswizzling logic
        if is_image_swizzled(ea_dir_entry):
            image_data = handle_image_swizzle_logic(
                image_data, entry_type, ea_dir_entry.h_width, ea_dir_entry.h_height, self.fh_sign, False
            )

        # palette info logic
        palette_info_dto: PaletteInfoDTO = get_palette_info_dto_from_dir_entry(ea_dir_entry, self)

        # decoding logic
        try:
            ea_dir_entry.img_convert_data = decode_image_data_by_entry_type(
                entry_type, image_data, palette_info_dto, ea_dir_entry
            )
        except Exception as error:
            logger.error(f"Error while decoding EA image! Error: {error}")
            logger.error(traceback.format_exc())
            return False

        if not ea_dir_entry.img_convert_data:
            logger.error("Decoded image data is empty!")
            return False

        return True
