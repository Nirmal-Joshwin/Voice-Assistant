import os


def list_files(path="."):
    try:
        return ", ".join(os.listdir(path)[:10])
    except:
        return "Cannot access folder"


def file_details(file):
    try:
        return f"Size: {os.path.getsize(file)} bytes"
    except:
        return "File not found"


def open_file(file):
    try:
        os.startfile(file)
        return "Opening file"
    except:
        return "Cannot open file"