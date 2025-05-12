@echo off
echo Starting Multiverse Tycoon...
if exist "dist\MultiVerseTycoon.exe" (
    "dist\MultiVerseTycoon.exe"
) else (
    echo MultiVerseTycoon.exe not found in dist directory.
    echo Please build the game first by running: python build.py
)
pause