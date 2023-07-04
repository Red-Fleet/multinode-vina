import os

def generateFilePath(file_dir: str, file_name: str, append_int: int = 0)-> str:
    """ generates path of file that is not present at given location(file_dir) 
    by appending (append_int) at the end of file name

    Args:
        file_dir (str): directory of file
        file_name (str): name of file to be saved at 'file_dir' location
        append_int (int): 0=> do not append anything in file name initially

    Returns:
        str: final file name
    """
    new_file_path = ""
    if append_int == 0: new_file_path = os.path.join(file_dir, file_name)
    else:
        filename_without_extension, file_extension = os.path.splitext(os.path.join(file_dir, file_name))
        new_file_path = os.path.join(file_dir, filename_without_extension + "(" + str(append_int) + ")" + file_extension)
    
    # if file name already exists then generate new name
    if os.path.isfile(new_file_path) == True:
        return generateFilePath(file_dir, file_name, append_int+1)
    else:
        return new_file_path