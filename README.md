# EA-Font-Manager
Program for handling FFN, PFN, XFN, MFN and SFN fonts from EA games

List of functionalities:
 - Parsing EA Font files
 - Preview for font images
 - Decoding and viewing font flags
 - Viewing character table
 - Exporting font images as DDS, PNG or BMP


This program **<ins>is still in development stage</ins>**.
It may not support all existing font types yet.

<img src="src\data\img\usage.png">

# Dependencies

* **[ReverseBox](https://github.com/bartlomiejduda/ReverseBox)**


# Building on Windows

1. Download and install  **[Python 3.11.6](https://www.python.org/downloads/release/python-3116/)**. Remember to add Python to PATH during installation
2. Download project's source code and save it in "EA-Font-Manager-main" directory
3. Go to the directory containing source code
   - ```cd EA-Font-Manager-main```
4. Create virtualenv and activate it
   - ```python -m venv my_env```
   - ```.\my_env\Scripts\activate.bat```
5. Install all libraries from requirements.txt file
   - ```pip install -r requirements.txt```
6. Add project's directory to PYTHONPATH environment variable
   - ```set PYTHONPATH=C:\Users\user\Desktop\EA-Font-Manager-main```
7. Run the src\main.py file
   - ```python src\main.py```


# Font formats support table

| Game Title                                      | Preview/Export support  | Import support     |
|-------------------------------------------------|-------------------------|--------------------|
| EA Sports Cricket 07 (PC)                       | <center>❌</center>      | <center>❌</center> |
| FA Premier League 2000 (PS1)                    | <center>✔️ / ❌</center> | <center>❌</center> |
| FIFA 97 (PC)                                    | <center>❌</center>      | <center>❌</center> |
| Medal of Honor: European Assault (Xbox Classic) | <center>❌</center>      | <center>❌</center> |
| NBA Live 07 (Xbox Classic)                      | <center>❌</center>      | <center>❌</center> |
| Need For Speed 2 (PS1)                          | <center>✔️ / ❌</center> | <center>❌</center> |
| Need For Speed 2 BETA (PC)                      | <center>❌</center>      | <center>❌</center> |
| Need For Speed: High Stakes (PC)                | <center>❌</center>      | <center>❌</center> |
| Need For Speed: Hot Pursuit 2 (PC)              | <center>✔️ / ❌</center> | <center>❌</center> |
| Need For Speed III: Hot Pursuit (PC)            | <center>❌</center>      | <center>❌</center> |
| Need For Speed: Porsche Unleashed (PC)          | <center>❌</center>      | <center>❌</center> |
| Need For Speed: Undercover (PSP)                | <center>❌</center>      | <center>❌</center> |
| SSX 1 (PS2)                                     | <center>✔️ / ❌</center> | <center>❌</center> |
| SSX 3 (PS2)                                     | <center>✔️ / ❌</center> | <center>❌</center> |
| SSX On Tour (PS2)                               | <center>❌</center>      | <center>❌</center> |
| SSX Tricky (PS2)                                | <center>✔️ / ❌</center> | <center>❌</center> |
| Triple Play 2002 (PS2)                          | <center>✔️ / ❌</center> | <center>❌</center> |


# Badges
![GitHub](https://img.shields.io/github/license/bartlomiejduda/EA-Font-Manager?style=plastic)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub repo size](https://img.shields.io/github/repo-size/bartlomiejduda/EA-Font-Manager?style=plastic)
![GitHub all releases](https://img.shields.io/github/downloads/bartlomiejduda/EA-Font-Manager/total)
![GitHub last commit](https://img.shields.io/github/last-commit/bartlomiejduda/EA-Font-Manager?style=plastic)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/bartlomiejduda/EA-Font-Manager?style=plastic)
