rmdir /s build /Q
rmdir /s dist /Q
del *.spec

python -m PyInstaller adbm.py ^
    --name adbm ^
    --distpath "C:/Program Files"