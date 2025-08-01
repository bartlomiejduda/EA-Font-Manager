"""
Copyright © 2025  Bartłomiej Duda
License: GPL-3.0 License
"""

import sys

from cx_Freeze import Executable, setup

from src.main import VERSION_NUM

base = None
if sys.platform == "win32":
    base = "Win32GUI"


executables = [
    Executable(
        "src/main.py",
        copyright="Copyright (C) 2025 Bartlomiej Duda",
        base=base,
        icon="src/data/img/ea_icon.ico",
        target_name="EA-Font-Manager-" + VERSION_NUM + ".exe",
    )
]

build_exe_options: dict = {
    "build_exe": "build_final/EA_Font_Manager",
    "packages": [],
    "includes": [],
    "excludes": [],
    "include_files": [],
}

options: dict = {"build_exe": build_exe_options}

setup(
    name="EA-Font-Manager " + VERSION_NUM,
    version=VERSION_NUM[1:],
    description="Tool for managing EA fonts",
    options=options,
    executables=executables,
)
