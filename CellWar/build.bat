@echo off
color 2
pyinstaller  --onefile --noconsole --log-level INFO gui.py
RMDIR /S /Q Build
del gui.spec
ren dist\gui.exe Cell.exe