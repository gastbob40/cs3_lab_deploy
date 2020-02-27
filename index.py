# Imports
import os

import pysftp
import yaml

# Get configuration from setting file
with open('config/settings.yml') as file:
    settings = yaml.full_load(file)

# Pass security
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None


def upload_folder(sftp: pysftp.Connection, from_computer: str, to_server: str, step: int = 1) -> None:
    """
    Copy a file or a folder
    :param sftp: The sftp connection
    :param from_computer: The file or folder to copy
    :param to_server: The folder to copy the file/folder inside
    :param step: The number of space to space printing
    """

    print(' ' * step, end="")
    to_server += '/' + from_computer.split('/')[-1]

    # Check the type of the path
    if os.path.isfile(from_computer):
        # We are in case of a file, so we can upload it
        sftp.put(from_computer, to_server)
        print(f" - File '{from_computer.split('/')[-1]}' uploaded")

    else:
        # We are in case of a folder
        sftp.execute(f"mkdir {to_server}")
        print(f" - Folder '{from_computer.split('/')[-1]}' created")

        for item in os.listdir(from_computer):
            upload_folder(sftp, f"{from_computer}/{item}", to_server, step + 3)


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
    print(f"Remove all folders and files in {directory} folder.")
    sftp.execute(f"rm {sftp.pwd}/* -r")

    # Create WEB-INF/classes folder
    print("Creating WEB-INF and classes folder")
    sftp.execute(f"mkdir {sftp.pwd}/WEB-INF")

    # Uploading classes folder
    print("Uploading classes folder")
    upload_folder(sftp, f"{settings['project_folder']}/build/classes", f"{sftp.pwd}/WEB-INF")

    # Uploading all the files and subfolders under the project WebContent folder, excluding the META-INF subfolder
    print("Uploading folder in WebContent/ (excluding META-INF/)")
    for item in os.listdir(f"{settings['project_folder']}/WebContent"):
        if item != "META-INF":
            upload_folder(sftp, f"{settings['project_folder']}/WebContent/{item}", sftp.pwd)

    # Uploading web.xml to refresh monitoring
    print("Uploading web.xml to refresh monitoring")
    upload_folder(sftp, f"{settings['project_folder']}/WebContent/WEB-INF/web.xml", f"{sftp.pwd}/WEB-INF")

    # End :)
    print("Uploading complete")
