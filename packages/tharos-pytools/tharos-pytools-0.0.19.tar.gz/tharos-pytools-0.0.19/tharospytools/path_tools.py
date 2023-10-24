"Tools to manipulate paths"
from os.path import exists, isdir
from pathlib import Path


def path_allocator(
    path_to_validate: str,
    particle: str | None = None,
    default_name: str = 'file',
    always_yes: bool = True
) -> str:
    """Checks if a file exists in this place, and arborescence exists.
    If not, creates the arborescence

    Args:
        path_to_validate (str): a string path to the file
        particle (str | None, optional): file extension. Defaults to None.
        default_name (str): a name if name is empty
        always_yes (bool, optional): if file shall be erased by default. Defaults to True.

    Returns:
        str: the path to the file, with extension
    """
    if ('/') in path_to_validate:
        if isdir(path_to_validate) and not path_to_validate.endswith('/'):
            path_to_validate = path_to_validate + '/'
        folder_path, sep, file_name = path_to_validate.rpartition('/')
    else:
        folder_path = ""
        sep = ""
        file_name = path_to_validate
    if file_name == "":
        file_name = default_name
    if particle and not file_name.endswith(particle):
        file_name = file_name+particle
    full_path: str = folder_path+sep+file_name
    if not always_yes and exists(full_path):
        if not input('File already exists. Do you want to write over it? (y/n): ').lower().strip() == 'y':
            raise OSError("File already exists. Aborting.")
    if folder_path != "":
        Path(folder_path).mkdir(parents=True, exist_ok=True)
    return full_path
