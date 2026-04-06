# 🌊 水井村風雲客棧數位入口平台 (Standard USR Portal)

[![Deploy to Render](https://render.com/images/deploy-to-render.button.svg)](https://render.com/deploy)

本專案為「風雲客棧」數位入口平台，整合了在地故事、USR 成果、AIoT 科技應用以及活動報名系統。

## 📖 專案手冊與說明文件
為了方便您快速上手與維修，請參閱下列詳細手冊：
- [🛠️ **安裝與部署手冊 (Installation Manual)**](./安裝手冊_Installation_Manual.md) —— 適合技術人員、環境架設使用。
- [📝 **網站使用與維護手冊 (User Manual)**](./使用手冊_User_Manual.md) —— 適合日常營運、更新內容、管理報名使用。

## 🚀 快速開始 (一行指令安裝)

### 1. 全自動下載暨安裝 (The One-Liner)
如果您想直接下載並啟動，只需開啟終端機貼上這行：

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/Nono0325/Shuijing-Fengyun-Inn/main/install.ps1 | iex
```

**Linux / Mac / Git Bash:**
```bash
curl -sSL https://raw.githubusercontent.com/Nono0325/Shuijing-Fengyun-Inn/main/install.sh | bash
```

### 2. 雲端部署 (GitHub One-Click)
若您已將此專案上傳至您的 GitHub 帳號：
1. 點擊上方的 **Deploy to Render** 按鈕。
2. 登入 Render 並連結您的 GitHub 倉庫。
3. 平台將自動建立 **PostgreSQL 資料庫** 並完成 **Django 環境建置** 與 **靜態檔案收集**。

### 2. 本地開發環境 (One-Line Setup)
在專案根目錄開啟終端機，執行適合您系統的腳本：

**Windows (CMD/PowerShell):**
```cmd
init_setup.bat
```

**Linux / Mac / Git Bash:**
```bash
chmod +x init_setup.sh && ./init_setup.sh
```
*此腳本會自動完成：建立虛擬環境、安裝套件、資料庫遷移、填充種子資料、並啟動伺服器。*

---

## 🛠 精彩特色 (Feature Highlights)

本平台結合了多項為 USR 計畫量身打造的動態模組：

### 1. 深度入口功能
- **全站搜尋 (Global Search)**：導覽列設有快搜框，支援跨模型（故事、成果、課程、活動、科技）內容檢索。
- **三生共好展示**：在地人努力過程（故事牆）、師生 USR 表現、成果影片/新聞。
- **智慧科技導覽**：AIoT 監測系統說明、AR 互動導覽。

### 2. 智慧報名與回饋系統
- **多維度報名回饋 (Modals)**：
  - **成功通知**：自動生成包含 **QR Code 簽到憑證** 的彈窗，並支持 PNG 一鍵下載。
  - **候補登記**：報名額滿時自動轉為候補，並告知當前順位。
  - **重複提醒**：自動偵測重複報名並友好提示。
- **自動化後台管理**：
  - 支持 **Excel 匯出**與 **Word 簽到表套印**。
  - **QR Code 掃碼報到**：工作人員掃碼後即完成核銷（具備權限驗證）。

### 3. 進階安全加固 (Security)
- **IDOR 漏洞防護**：取消報名需通過手機/Email 雙因子驗證，防止惡意刪除他人紀錄。
- **輸入防護**：全站具備 XSS 過濾與輸入長度限制，防止資料庫洪水攻擊。
- **生產環境優化**：預設啟用 X-Frame-Options (Clickjacking) 與 XSS-Filter 防護標頭。

## 🔑 管理員資訊
- **後台網址**: `/admin/`
- **預設帳號**: `cmlin`
- **預設密碼**: `12345678`

---

## 📂 技術堆疊
- **Backend**: Django 6.0, SQLite (Local) / PostgreSQL (Cloud)
- **Frontend**: Bootstrap 5, WhiteNoise (Static serving)
- **Extra**: docxtpl (Word 範本), openpyxl (Excel 匯出)

---
*本專案為國立虎尾科技大學 USR 計畫社會實踐成果之數位化呈現。*
