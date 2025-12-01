# GitHub 上傳指南

## 📋 前置準備

### 1. 確認 Git 已安裝
```bash
git --version
```
如果沒有安裝，請到 [Git 官網](https://git-scm.com/) 下載安裝。

### 2. 設定 Git 使用者資訊 (首次使用)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## 🚀 上傳步驟

### 方法 1: 建立新的 GitHub Repository (推薦)

#### Step 1: 在 GitHub 上建立新 Repository
1. 登入 [GitHub](https://github.com)
2. 點擊右上角 `+` → `New repository`
3. 填寫資訊:
   - **Repository name**: `ICAIF-24-Finance-RAG` (或您喜歡的名稱)
   - **Description**: `Hybrid RAG System for ICAIF-24 Finance RAG Challenge`
   - **Public** or **Private**: 選擇 Public (如果要公開) 或 Private
   - ❌ **不要勾選** "Initialize this repository with a README" (我們已經有了)
4. 點擊 `Create repository`

#### Step 2: 在本地初始化 Git
打開 PowerShell 或 CMD，切換到專案目錄:
```bash
cd C:\Users\user\Desktop\NLP_TAICA
```

初始化 Git:
```bash
git init
```

#### Step 3: 添加所有檔案
```bash
git add .
```

#### Step 4: 提交變更
```bash
git commit -m "Initial commit: Hybrid RAG system for Finance RAG Challenge"
```

#### Step 5: 連接到 GitHub Repository
將下面的 `YOUR_USERNAME` 和 `YOUR_REPO_NAME` 替換成您的 GitHub 使用者名稱和 Repository 名稱:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

例如:
```bash
git remote add origin https://github.com/johndoe/ICAIF-24-Finance-RAG.git
```

#### Step 6: 推送到 GitHub
```bash
git branch -M main
git push -u origin main
```

第一次推送時，會要求您登入 GitHub 帳號。

---

### 方法 2: 使用現有的 Repository

如果您已經有一個 Repository，只需要:

```bash
cd C:\Users\user\Desktop\NLP_TAICA
git init
git add .
git commit -m "Initial commit: Hybrid RAG system"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

---

## 🔄 後續更新

當您修改檔案後，要更新到 GitHub:

```bash
# 1. 查看變更
git status

# 2. 添加變更的檔案
git add .

# 3. 提交變更
git commit -m "描述您的變更內容"

# 4. 推送到 GitHub
git push
```

---

## 📝 常用 Git 指令

```bash
# 查看狀態
git status

# 查看提交歷史
git log --oneline

# 查看遠端 Repository
git remote -v

# 拉取最新變更 (如果有其他人協作)
git pull

# 建立新分支
git checkout -b feature-name

# 切換分支
git checkout main
```

---

## ⚠️ 注意事項

### 1. 不要上傳大檔案
`.gitignore` 已經設定好，以下檔案不會被上傳:
- 資料集檔案 (`.jsonl`, `.csv`, `.gz`)
- 模型檔案 (`.pt`, `.pth`, `.bin`)
- Python cache (`__pycache__/`)
- 虛擬環境 (`venv/`, `.venv/`)

### 2. 敏感資訊
如果有 API Keys 或密碼，**絕對不要** commit 到 GitHub！
可以使用環境變數或 `.env` 檔案 (並加入 `.gitignore`)。

### 3. 檔案大小限制
GitHub 單一檔案限制 100MB。如果有大檔案，請使用 Git LFS 或不要上傳。

---

## 🎯 完成後

上傳成功後，您的 Repository 會包含:
- ✅ 完整的程式碼
- ✅ 詳細的 README.md
- ✅ 簡報大綱 (PRESENTATION_SUMMARY.md)
- ✅ 資料分析報告 (analysis_report.md)

您可以在簡報的第一頁加上 GitHub 連結:
```
GitHub Repository: https://github.com/YOUR_USERNAME/YOUR_REPO_NAME
```

---

## 🆘 遇到問題？

### 問題 1: 推送時要求登入
- 使用 GitHub Personal Access Token (PAT) 而非密碼
- 到 GitHub Settings → Developer settings → Personal access tokens → Generate new token

### 問題 2: 推送被拒絕 (rejected)
```bash
git pull --rebase origin main
git push
```

### 問題 3: 想要撤銷上一次 commit
```bash
git reset --soft HEAD~1
```

---

## 📚 更多資源
- [Git 官方文檔](https://git-scm.com/doc)
- [GitHub 指南](https://guides.github.com/)
- [Git 教學 (中文)](https://gitbook.tw/)
