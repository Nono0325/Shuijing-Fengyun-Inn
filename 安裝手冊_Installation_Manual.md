# 水井村風雲客棧 - 系統安裝與環境部署手冊 (Installation Manual)

本文件將引導系統管理員或開發者，從零開始在新的電腦環境中架設「水井村風雲客棧」網站系統。

---

## 壹、 基礎環境要求

在開始安裝之前，請確保您的電腦已安裝下列軟體：
1. **Python 3.12+**: [下載位址](https://www.python.org/downloads/) (建議安裝時勾選 "Add Python to PATH")。
2. **Git** (選配): 用於複製原始碼。
3. **Microsoft Word**: 用於設計或編輯簽到表範本。

---

## 貳、 安裝步驟 (Windows 環境)

### 1. 取得專案原始碼 (快速方式)
您可以直接使用「超·一行指令」自動下載並初始化：
**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/Nono0325/Shuijing-Fengyun-Inn/main/install.ps1 | iex
```

或是手動將專案資料夾 (例如 `Nono`) 複製到您的電腦桌面上，或使用 Git 複製。

### 2. 建立虛擬環境 (Virtual Environment)
開啟 PowerShell 或 CMD，進入專案目錄 (`cd C:\Users\user\Desktop\Nono`)，執行：
```powershell
python -m venv venv
```

### 3. 啟動虛擬環境
```powershell
.\venv\Scripts\activate
```

### 4. 安裝必要套件
本系統依賴多個第三方庫（如 Django, Pillow, docxtpl 等），請執行：
```powershell
pip install -r requirements.txt
```

### 5. 初始化資料庫 (Migrations)
建立資料表結構：
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 6. 建立最高管理員帳號
執行下列指令並依照提示設定您的帳號、Email 與密碼：
```powershell
python manage.py createsuperuser
```

---

## 參、 系統初始資料填充 (Optional)

為了讓網站一開始就有測試資料（如值班人員、課程預覽），請執行：

### 1. 注入基礎種子資料 (Seeding)
```powershell
python seed.py          # 基礎維護與導覽資料
python seed_events.py   # 活動列表測試資料
python seed_portal.py   # 故事牆、USR成果與科技應用資料
```

### 2. 產製預設 Word 簽到表範本
這是匯出簽到表功能正常運作的關鍵步驟：
```powershell
python create_default_template.py
```

---

## 肆、 啟動與訪問

### 啟動開發伺服器
```powershell
python manage.py runserver
```

### 訪問網址
* **前台大廳**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **管理後台**: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## 伍、 常見問題排除

1. **圖片無法顯示**: 請確保 `media` 資料夾存在且具有寫入權限。
2. **Word 匯出失敗**: 請檢查「管理後台 > 簽到表版型範本」是否已上傳至少一份 `.docx` 檔案。
3. **Email 寄送不見**: 目前測試環境設定為控制台發信，請在執行 `runserver` 的終端機視窗查看信件內容。若要正式發信，請修改 `settings.py` 的 SMTP 設定。

---

> [!NOTE]
> 關於日常營運操作（如新增課程、編輯內容），請參閱另一個檔案：[使用手冊_User_Manual.md](./使用手冊_User_Manual.md)。
