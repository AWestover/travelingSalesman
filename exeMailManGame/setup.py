import cx_Freeze
import os
import pygame
import numpy as np
import sys


base = None
if sys.platform == 'win32':
    base = "Win32GUI"

my_executables = [cx_Freeze.Executable("traveling_mailman.py", base=base, icon="PythonImagesAndVideos/mail_icon.ico")]


os.environ['TCL_LIBRARY'] = r'C:\Program Files\Python35\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Program Files\Python35\tcl\tk8.6'

build_options = {
    "build_exe": {
        "packages": ["pygame", "tkinter"],
        "includes": ['numpy.core._methods', 'numpy.lib.format'],
        "include_files": ["PythonImagesAndVideos/mail_icon.ico", "PythonImagesAndVideos/"]
    }
}


description = "In this game you must find the most efficient route to safely deliver your mail or you will lose your job to the robots!"

cx_Freeze.setup(
    name="The Traveling Mailman",
    options=build_options,
    description=description,
    executables=my_executables,
    version="1.1",
    author="Alek Westover"
)
