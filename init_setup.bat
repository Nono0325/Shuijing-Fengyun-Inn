@echo off
echo [1/5] 正在建立虛擬環境...
python -m venv venv

echo [2/5] 正在啟動虛擬環境並安裝套件...
call venv\Scripts\activate
pip install -r requirements.txt

echo [3/5] 正在進行資料庫遷移...
python manage.py makemigrations
python manage.py migrate

echo [4/5] 正在填充種子資料與管理員...
python create_admin.py
python seed.py
python seed_events.py
python seed_portal.py
python create_default_template.py

echo [5/5] 啟動開發伺服器...
echo 網站已啟動，請訪問: http://127.0.0.1:8000
python manage.py runserver
pause
