How to install arkide-desktop:

- Clone the repository
``git clone https://github.com/arc360alt/ArkIDE-Desktop.git``
- CD into ArkIDE Desktop
``cd ArkIDE-Desktop``
- Create and go into a venv:
#### Linux:
``python3 -m venv venv``
``source venv/bin/activate``
#### Windows:
``python -m venv venv``
* **Command Prompt:**
  ```bash
  venv\Scripts\activate.bat
  ```
* **PowerShell:**
  ```bash
  .\venv\Scripts\Activate.ps1
  ```
- Install the requiered packages:
``pip install PyQt5 PyQtWebEngine``
- Run ArkIDE ``python desktop.py``