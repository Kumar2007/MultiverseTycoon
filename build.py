#!/usr/bin/env python3
"""
Build script for Multiverse Tycoon
Creates a distribution package for Windows, macOS, and Linux
"""

import os
import platform
import shutil
import sys
import zipfile

def print_separator():
    print("="*80)

# Configure the build
APP_NAME = "MultiVerseTycoon"
MAIN_SCRIPT = "multiverse_tycoon.py"

# Files to include in the distribution
INCLUDE_FILES = [
    "multiverse_tycoon.py",
    "currency.py",
    "achievements.py",
    "heists.py", 
    "minigames.py",
    "generated-icon.png",
    "README.md"
]

# Create the distribution folder
dist_dir = "dist"
if not os.path.exists(dist_dir):
    os.makedirs(dist_dir)

# Create the build folder
build_dir = os.path.join(dist_dir, APP_NAME)
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)  # Remove existing build directory
os.makedirs(build_dir)

# Create save directory
save_dir = os.path.join(build_dir, "saves")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    print("Created 'saves' directory for game save files")

# Determine the platform
system = platform.system()
print_separator()
print(f"Creating distribution package for Multiverse Tycoon ({system})")
print_separator()

# Copy all required files to the build directory
print("Copying game files...")
for file in INCLUDE_FILES:
    if os.path.exists(file):
        shutil.copy(file, build_dir)
        print(f"  - Copied {file}")
    else:
        print(f"  - Warning: {file} not found, skipping")

# Create the platform-specific runner scripts in the build directory
if system == "Windows" or True:  # Include Windows files for all platforms
    # Create Windows batch file
    with open(os.path.join(build_dir, "run_game.bat"), "w") as batch_file:
        batch_file.write("@echo off\n")
        batch_file.write("echo Starting Multiverse Tycoon...\n")
        batch_file.write("python multiverse_tycoon.py\n")
        batch_file.write("pause\n")
    print("Created Windows batch file")

    # Create a more detailed Windows README
    with open(os.path.join(build_dir, "README_WINDOWS.txt"), "w") as readme:
        readme.write("MULTIVERSE TYCOON - WINDOWS INSTRUCTIONS\n")
        readme.write("====================================\n\n")
        readme.write("Requirements:\n")
        readme.write("- Python 3.6 or higher must be installed\n")
        readme.write("- Dependencies: None (standard library only)\n\n")
        readme.write("To run the game:\n")
        readme.write("1. Double-click run_game.bat\n")
        readme.write("   OR\n")
        readme.write("2. Open a command prompt in this folder and type:\n")
        readme.write("   python multiverse_tycoon.py\n\n")
        readme.write("Enjoy your multiverse business adventures!\n")

if system == "Darwin" or True:  # Include macOS files for all platforms
    # Create macOS/Linux shell script
    with open(os.path.join(build_dir, "run_game.sh"), "w") as shell_file:
        shell_file.write("#!/bin/bash\n")
        shell_file.write("echo \"Starting Multiverse Tycoon...\"\n")
        shell_file.write("python3 multiverse_tycoon.py\n")
    
    # Make the shell script executable
    os.chmod(os.path.join(build_dir, "run_game.sh"), 0o755)
    print("Created macOS/Linux shell script")

    # Create a more detailed macOS README
    with open(os.path.join(build_dir, "README_MACOS.txt"), "w") as readme:
        readme.write("MULTIVERSE TYCOON - MACOS INSTRUCTIONS\n")
        readme.write("==================================\n\n")
        readme.write("Requirements:\n")
        readme.write("- Python 3.6 or higher must be installed\n")
        readme.write("- Dependencies: None (standard library only)\n\n")
        readme.write("To run the game:\n")
        readme.write("1. Open Terminal in this folder\n")
        readme.write("2. Type: chmod +x run_game.sh (first time only)\n")
        readme.write("3. Type: ./run_game.sh\n")
        readme.write("   OR\n")
        readme.write("4. Type: python3 multiverse_tycoon.py\n\n")
        readme.write("Enjoy your multiverse business adventures!\n")

if system == "Linux" or True:  # Include Linux files for all platforms
    # Linux README already created with the macOS one if using run_game.sh
    # Create a more detailed Linux README
    with open(os.path.join(build_dir, "README_LINUX.txt"), "w") as readme:
        readme.write("MULTIVERSE TYCOON - LINUX INSTRUCTIONS\n")
        readme.write("==================================\n\n")
        readme.write("Requirements:\n")
        readme.write("- Python 3.6 or higher must be installed\n")
        readme.write("- Dependencies: None (standard library only)\n\n")
        readme.write("To run the game:\n")
        readme.write("1. Open Terminal in this folder\n")
        readme.write("2. Type: chmod +x run_game.sh (first time only)\n")
        readme.write("3. Type: ./run_game.sh\n")
        readme.write("   OR\n")
        readme.write("4. Type: python3 multiverse_tycoon.py\n\n")
        readme.write("Enjoy your multiverse business adventures!\n")

# Create zip archive of the build directory
zip_filename = f"{APP_NAME}_{system}.zip"
zip_path = os.path.join(dist_dir, zip_filename)

print(f"Creating distribution package: {zip_filename}")
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(build_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, dist_dir)
            zipf.write(file_path, arcname)

print_separator()
print(f"Distribution package created: {zip_path}")
print("This package can be distributed to users on various platforms.")
print("Users will need to have Python installed to run the game.")
print_separator()

print("Distribution package contents:")
for root, dirs, files in os.walk(build_dir):
    level = root.replace(build_dir, '').count(os.sep)
    indent = ' ' * 4 * level
    print(f"{indent}{os.path.basename(root)}/")
    sub_indent = ' ' * 4 * (level + 1)
    for file in files:
        print(f"{sub_indent}{file}")

print_separator()
print("To distribute the game:")
print(f"1. Share the {zip_filename} file with your users")
print("2. Users should extract the zip file")
print("3. Windows users can run run_game.bat")
print("4. macOS/Linux users can run run_game.sh")
print_separator()