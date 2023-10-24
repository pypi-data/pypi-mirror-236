"""make input and output file path legal"""

import os


def check_inpath(folder_path: str):
    """return legal folder path, end with '/'."""
    folder_path = folder_path.replace("\\", "/")
    if folder_path[-1] != "/":
        folder_path = folder_path + "/"
    if os.path.exists(folder_path) == False:
        raise FileNotFoundError("cannot find folder: " + folder_path)
    return folder_path


def check_infile(file_path: str):
    """return legal flie path."""
    if os.path.exists(file_path) == False:
        raise FileNotFoundError("cannot find file: " + file_path)
    return file_path


def check_outpath(folder_path: str, overwriting: bool = True, creating: bool = True):
    """Create a folder if it not exist. Return legal folder path."""
    folder_path = folder_path.replace("\\", "/")
    if folder_path[-1] != "/":
        folder_path = folder_path + "/"
    if os.path.exists(folder_path) == True:
        if overwriting == False:
            raise FileExistsError("file existed: " + folder_path)

    else:
        print("not exists path: " + str(folder_path))
        if creating == False:
            if input("create this folder? (y/n)") == "y":
                os.makedirs(folder_path)
            else:
                raise FileNotFoundError("cannot find folder: " + folder_path)
    return folder_path


def check_outfile(file_path: str, overwriting: bool = True, creating: bool = True):
    """Create a folder if it not exist. Return legal file path."""
    file_path = file_path.replace("\\", "/")
    folder_path = os.path.dirname(file_path)
    if os.path.exists(file_path) == True:
        if overwriting == False:
            raise FileExistsError("file existed: " + file_path)
    folder_path = check_outpath(folder_path, overwriting=True, creating=creating)

    return file_path
