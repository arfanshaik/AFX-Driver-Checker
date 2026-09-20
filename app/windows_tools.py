import os
import platform
import subprocess

def open_device_manager():
    if platform.system() != "Windows":
        return False, "Device Manager is available only on Windows."
    try:
        subprocess.Popen(["devmgmt.msc"], shell=True)
        return True, "Device Manager opened."
    except Exception as exc:
        return False, str(exc)

def open_windows_update():
    if platform.system() != "Windows":
        return False, "Windows Update is available only on Windows."
    try:
        os.startfile("ms-settings:windowsupdate")
        return True, "Windows Update opened."
    except Exception as exc:
        return False, str(exc)
