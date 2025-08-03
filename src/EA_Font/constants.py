"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import PIL.Image

# fmt: off
PALETTE_TYPES = (33, 34, 35, 36, 41, 42, 44, 45, 46, 47, 48, 49, 50, 58, 59)
CONVERT_IMAGES_SUPPORTED_TYPES = [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 20, 22, 24, 25, 30, 33, 34, 35, 36, 42, 59, 64,
                                  65, 66, 67, 88, 89, 90, 91, 92, 93, 96, 97, 98, 100, 101, 104, 109, 115, 119, 120,
                                  121, 122, 123, 125, 126, 127, 130, 131, 192, 193, 194, 237, 248, 251]

IMPORT_IMAGES_SUPPORTED_TYPES = [1, 2, 3, 4, 5, 22, 64, 65, 66, 88, 89, 90, 91, 92, 93, 96, 97, 98,
                                 109, 120, 121, 123, 125, 126, 127, 130, 131, 192, 193, 194, 237, 248, 251, 255]

OLD_SHAPE_ALLOWED_SIGNATURES = (
    "FNTF",  # PC games
    "FNTP",  # PS1 games
    "FNTS",  # PS2 games
    "FNTX",  # XBOX games
    "FNTM",  # PSP games
    "FNTG",  # WII/Gamecube games
    "FNTA",  # Game Boy Advance games
)

NEW_SHAPE_ALLOWED_SIGNATURES = ()  # TODO

mipmaps_resampling_mapping: dict = {
    "nearest": PIL.Image.Resampling.NEAREST,
    "box": PIL.Image.Resampling.BOX,
    "bilinear": PIL.Image.Resampling.BILINEAR,
    "hamming": PIL.Image.Resampling.HAMMING,
    "bicubic": PIL.Image.Resampling.BICUBIC,
    "lanczos": PIL.Image.Resampling.LANCZOS
}

baseline_flags_mapping: dict = {
    0: "Roman (english)",
    1: "Ideographic (Kanji)",
    2: "Hanging (Arabic)"
}

orientation_flags_mapping: dict = {
    0: "Horizontal",
    1: "Vertical"
}

direction_flags_mapping: dict = {
    0: "Left-To-Right",
    1: "Right-To-Left"
}

encoding_flags_mapping: dict = {
    0: "ASCII",
    1: "Unicode",
    2: "Shift-JIS",
    3: "Reserved"
}

format_flags_mapping: dict = {
    0: "Character12",
    1: "Character16",
}
