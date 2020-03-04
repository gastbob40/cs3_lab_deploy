# CS3 Lab Deploy

![CSULA](https://img.shields.io/badge/CSULA-project-brightgreen)
![python](https://img.shields.io/badge/Language-Python-blueviolet)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## About

CS3 Lab Deploy is a python program to simplify the deployment of Java EE Website.

CS3 Lab Deploy is a project by [gastbob40](https://github.com/gastbob40).

## Requirements

You will need this element for the proper working of the project.

- [Python 3](https://www.python.org/downloads/)


## Getting started

1. **First, you will have to clone the project.**

```shell
git clone https://github.com/gastbob40/cs3_lab_deploy
```

2. **Create a `virtual environment`, in order to install dependencies locally.** For more information about virtual environments, [click here](https://docs.python.org/3/library/venv.html).

```shell
python -m venv venv
```

3. **Activate the virtual environment**

Linux/macOS:

```shell
# Using bash/zsh
source venv/bin/activate
# Using fish
. venv/bin/activate.fish
# Using csh/tcsh
source venv/bin/activate.csh
``` 

Windows:

```
# cmd.exe
venv\Scripts\activate.bat
# PowerShell
venv\Scripts\Activate.ps1
```


4. **Finally, install the dependencies**

````shell
pip install -r requirements.txt
````

5. **Configure CS3 Lab Deploy**. This is necessary to use the program. Check the next section for instructions.

6. **Run `python index.py` to launch CS3 Lab Deploy.** Also make sure that the venv is activated when you launch the program (you should see `venv` to the left of your command prompt).

## Configuration

The `config` folder contains all the data of the program configuration.

### settings.default.yml

This file contain all data about sftp connection. This file looks like this:
 
```yaml
hostname: ~           # This is the hostname of the sftp server
username: ~           # This is your username in the server
password: ~           # This is your password in the server
project_folder: ~     # This is the place of the project on YOUR computer
folder_to_deploy: ~   # This is the place to deploy the project on the server
```

You must fill in the file and rename it to `settings.yml`