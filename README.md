# 🌊 水井村風雲客棧數位入口平台 (Standard USR Portal)

[![Deploy to Render](https://render.com/images/deploy-to-render.button.svg)](https://render.com/deploy)

本專案為「風雲客棧」數位入口平台，整合了在地故事、USR 成果、AIoT 科技應用以及活動報名系統。

## 🚀 快速開始 (一行指令部署)

### 1. 雲端部署 (GitHub One-Click)
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

## 🛠 功能特色
- **三生共好展示**：在地人努力過程（故事牆）、師生 USR 表現、成果影片/新聞。
- **智慧科技導覽**：AIoT 監測系統說明、AR 互動導覽。
- **活動體驗系統**：包含「不蒜花」、「OTTO 機器人」等工作坊展示與線上報名。
- **自動化後台**：
  - 具備**候補機制**的報名系統。
  - 支持 **Excel 匯出**與 **Word 簽到表套印**。
  - **QR Code 掃碼報到**（限管理員）。

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
