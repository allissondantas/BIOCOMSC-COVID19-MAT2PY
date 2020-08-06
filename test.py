import os
import platform
import subprocess


path = os.getcwd()
path = path+'/reports_pdf/brasil/risk-pt/Cases'

def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


open_file(path)