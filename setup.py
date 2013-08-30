#!/usr/bin/env python2.7

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "numpy", "scipy", "wx"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "deterriblesquareify",
        version = "0.1",
        description = "Deterriblesquareify TEM images",
        options = {"build_exe": build_exe_options},
        executables = [Executable("deterriblesquareify.py", base=base)])
