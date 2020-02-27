# Imports
import os
from typing import List

import pysftp
import yaml

# Get configuration from setting file
with open('config/settings.yml') as file:
    settings = yaml.full_load(file)

# Pass security
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None


def upload_folder(sftp: pysftp.Connection, from_computer: str, to_server: str, is_last: bool = False, step: int = 1,
                  blanks: List[bool] = None) -> None:
    """
    Copy a file or a folder
    :param sftp: The sftp connection
    :param from_computer: The file or folder to copy
    :param to_server: The folder to copy the file/folder inside
    :param is_last: The boolean that say if it is the last file/folder
    :param step: The number of space to space printing
    :param blanks: List of booleans that say if the repository is empty
    """

    if blanks is None:
        blanks = [False]
    if len(blanks) <= step // 4:
        blanks.append(False)

    # Print space and tree before folder

    for i in range(step // 4):
        if blanks[i]:
            print(' ' * 4, end="")
        else:
            print('|   ', end="")
    if is_last:
        print('└───', end="")
        blanks[step // 4] = True
    else:
        print('├───', end="")

    # Change current name
    to_server += '/' + from_computer.split('/')[-1]

    # Check the type of the path
    if os.path.isfile(from_computer):
        # We are in case of a file, so we can upload it
        sftp.put(from_computer, to_server)
        print(f" File '{from_computer.split('/')[-1]}' uploaded")

    else:
        # We are in case of a folder
        sftp.execute(f"mkdir {to_server}")
        print(f" Folder '{from_computer.split('/')[-1]}' created")

        index = 1
        for item in os.listdir(from_computer):
            upload_folder(sftp, f"{from_computer}/{item}", to_server, len(os.listdir(from_computer)) == index, step + 4,
                          blanks)
            index += 1
        blanks[step // 4] = False


# Connect
with pysftp.Connection(host=settings['hostname'],
                       username=settings['username'],
                       password=settings['password'],
                       cnopts=cnopts) as sftp:
    print("Connection succesfully stablished.")

    # Change directory
    directory = 'test'  # TODO Thing to change the name to real test
    print(f"Change directory to {directory}.")
    sftp.cwd(directory)

    # Clean folder
    print(f"\nRemove all folders and files in {directory} folder.")
    sftp.execute(f"rm {sftp.pwd}/* -r")

    # Create WEB-INF/classes folder
    print("\nCreating WEB-INF and classes folder")
    sftp.execute(f"mkdir {sftp.pwd}/WEB-INF")

    # Uploading classes folder
    print("\nUploading classes folder")
    name = f"{settings['project_folder']}/build"
    upload_folder(sftp, name + "/classes", f"{sftp.pwd}/WEB-INF", len(os.listdir(name)) == 1)

    # Uploading all the files and subfolders under the project WebContent folder, excluding the META-INF subfolder
    print("\nUploading folder in WebContent/ (excluding META-INF/)")
    for item in os.listdir(f"{settings['project_folder']}/WebContent"):
        if item != "META-INF":
            name = f"{settings['project_folder']}/WebContent"
            upload_folder(sftp, name + f"/{item}", sftp.pwd, len(os.listdir(name)) == 2)

    # Uploading web.xml to refresh monitoring
    print("\nUploading web.xml to refresh monitoring")
    upload_folder(sftp, f"{settings['project_folder']}/WebContent/WEB-INF/web.xml", f"{sftp.pwd}/WEB-INF", True)

    # End :)
    print("\nUploading complete")
