# How to install arkide-desktop:

- Clone the repository
```bash
git clone https://github.com/arc360alt/ArkIDE-Desktop.git
```
- CD into ArkIDE Desktop
```bash
cd ArkIDE-Desktop
```
#### Create and go into a venv:
-  Linux:
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
- Windows:
``python -m venv venv`` Then run:
* **Command Prompt:**
  ```bash
  venv\Scripts\activate.bat
  ```
* **PowerShell:**
  ```bash
  .\venv\Scripts\Activate.ps1
  ```
- Install the requiered packages:
```bash
pip install PyQt5 PyQtWebEngine
```
- Run ArkIDE
```bash
python desktop.py
```

# Limitations:
- For some reason the Extra Extentions are just gone, so your going to have to import them yourself instead of clicking on them inside of the extention gallery
- Save button on linux is quite buggy, you need to manualy save it evrey time. Dont know why.
- Pro tip: When avalible, USE THE WEB VERSION, this app sucks tbh its so broken, I'll fix it at some point.