set FLASK_APP=sicklist.py
set FLASK_DEBUG=1
set FLASK_CONFIG=development
REM set DEV_DATABASE_URL=mysql+pymysql://sicklistuser:111@localhost:3306/devsicklist
set DEV_DATABASE_URL=postgresql://sicklistuser:111@localhost/devsicklist
start cmd.exe /K .\venv\Scripts\activate.bat