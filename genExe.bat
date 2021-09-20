pyinstaller -F RandomDrawMain.py -w --onefile -i cover.ico
copy dist\RandomDrawMain.exe .
rd /s /Q build dist