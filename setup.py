import sys
import os
from cx_Freeze import setup, Executable

# Increase recursion depth just in case
sys.setrecursionlimit(5000)

app_name = "JXRConverter"
version = "1.4"
description = "JXR to PNG Auto-Converter"

# Build options
build_exe_options = {
    "excludes": ["tkinter", "unittest", "email", "http", "html", "xml", "pydoc"],
    "packages": ["os", "sys", "logging", "PyQt5", "subprocess", "threading", "queue", "json", "pathlib", "datetime", "shutil", "socket", "watchdog"],
    "include_files": [
        ("jxr_to_png.exe", "jxr_to_png.exe"),
        ("hdrfix.exe", "hdrfix.exe")
    ]
}

# Add conditional check for executables to avoid failure if they are not strictly present in build environment
if not os.path.exists("jxr_to_png.exe"):
    build_exe_options["include_files"] = [f for f in build_exe_options["include_files"] if f[0] != "jxr_to_png.exe"]
    print("Warning: jxr_to_png.exe not found.")
if not os.path.exists("hdrfix.exe"):
    build_exe_options["include_files"] = [f for f in build_exe_options["include_files"] if f[0] != "hdrfix.exe"]
    print("Warning: hdrfix.exe not found.")


# Base is "gui" for Windows GUI applications (hides the console) in modern cx_Freeze
base = "gui" if sys.platform == "win32" else None

# MSI specific options
bdist_msi_options = {
    "add_to_path": False,
    "initial_target_dir": rf"[ProgramFilesFolder]\{app_name}",
    # If you have an icon, you can add it here. Need a .ico file
}

# The executable definition
executables = [
    Executable(
        "main.py", 
        base=base, 
        target_name=f"{app_name}.exe",
        # icon="icon.ico" # Add icon if you have one
    )
]

setup(
    name=app_name,
    version=version,
    description=description,
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=executables
)
