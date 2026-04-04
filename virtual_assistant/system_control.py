import os
import subprocess
import ctypes

def increase_volume():
    os.system("powershell (new-object -com wscript.shell).SendKeys([char]175)")
    return "Volume increased"


def decrease_volume():
    os.system("powershell (new-object -com wscript.shell).SendKeys([char]174)")
    return "Volume decreased"


def mute_volume():
    os.system("powershell (new-object -com wscript.shell).SendKeys([char]173)")
    return "Muted"


def set_brightness(level):
    os.system(f"powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})")
    return f"Brightness set to {level}"

def set_volume(level):
    try:
        level = int(level)

        # Windows volume range: 0–100 → convert to 0–65535
        vol = int((level / 100) * 65535)

        ctypes.windll.winmm.waveOutSetVolume(0, vol | (vol << 16))

        return f"Volume set to {level}"
    except:
        return "Failed to set volume"

def open_app(app):
    apps = {
        "chrome": "start chrome",
        "notepad": "notepad",
        "calculator": "calc"
    }

    if app in apps:
        subprocess.Popen(apps[app], shell=True)
        return f"Opening {app}"

    return "App not found"