import os
import subprocess
from pathlib import Path
import nicegui

cmd = [
    'python',
    '-m', 'PyInstaller',
    'main.py', # your main file with ui.run()
    '--name', 'Ecig App', # name of your app
    '--onefile',
    '--splash', './static/aptiv.jpg',
    '--icon', './static/favicon.ico',
    #'--windowed', # prevent console appearing, only use with ui.run(native=True, ...)
    '--add-data', f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui'
]
subprocess.call(cmd)
