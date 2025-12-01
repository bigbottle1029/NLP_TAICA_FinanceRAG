# ========================================
# GitHub 快速上傳腳本
# ========================================
# 
# 使用方法:
# 1. 先在 GitHub 上建立新的 Repository
# 2. 修改下面的 YOUR_USERNAME 和 YOUR_REPO_NAME
# 3. 執行此腳本: .\upload_to_github.ps1
#

# ========================================
# 請修改這裡！
# ========================================
$GITHUB_USERNAME = "YOUR_USERNAME"        # 例如: "johndoe"
$REPO_NAME = "ICAIF-24-Finance-RAG"       # Repository 名稱

# ========================================
# 以下不需要修改
# ========================================

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  GitHub 上傳腳本 - Finance RAG Project" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# 檢查是否已修改使用者名稱
if ($GITHUB_USERNAME -eq "YOUR_USERNAME") {
    Write-Host "❌ 錯誤: 請先修改腳本中的 GITHUB_USERNAME 和 REPO_NAME！" -ForegroundColor Red
    Write-Host ""
    Write-Host "請編輯 upload_to_github.ps1 檔案，將:" -ForegroundColor Yellow
    Write-Host '  $GITHUB_USERNAME = "YOUR_USERNAME"' -ForegroundColor Yellow
    Write-Host "改為您的 GitHub 使用者名稱，例如:" -ForegroundColor Yellow
    Write-Host '  $GITHUB_USERNAME = "johndoe"' -ForegroundColor Green
    Write-Host ""
    exit 1
}

$REPO_URL = "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

Write-Host "📋 設定資訊:" -ForegroundColor Yellow
Write-Host "   GitHub 使用者: $GITHUB_USERNAME"
Write-Host "   Repository: $REPO_NAME"
Write-Host "   URL: $REPO_URL"
Write-Host ""

# 確認
$confirm = Read-Host "確認要上傳到此 Repository 嗎? (y/n)"
if ($confirm -ne "y") {
    Write-Host "❌ 已取消上傳" -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "🚀 開始上傳..." -ForegroundColor Green
Write-Host ""

# 設定遠端 Repository
Write-Host "1. 設定遠端 Repository..." -ForegroundColor Cyan
git remote add origin $REPO_URL
if ($LASTEXITCODE -ne 0) {
    Write-Host "   ⚠️  遠端 Repository 已存在，嘗試更新..." -ForegroundColor Yellow
    git remote set-url origin $REPO_URL
}

# 設定分支名稱為 main
Write-Host "2. 設定主分支為 main..." -ForegroundColor Cyan
git branch -M main

# 推送到 GitHub
Write-Host "3. 推送到 GitHub..." -ForegroundColor Cyan
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "  ✅ 上傳成功！" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔗 您的 Repository 網址:" -ForegroundColor Cyan
    Write-Host "   $REPO_URL" -ForegroundColor White
    Write-Host ""
    Write-Host "📝 下次更新檔案時，請執行:" -ForegroundColor Yellow
    Write-Host "   git add ." -ForegroundColor White
    Write-Host '   git commit -m "描述您的變更"' -ForegroundColor White
    Write-Host "   git push" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Red
    Write-Host "  ❌ 上傳失敗" -ForegroundColor Red
    Write-Host "================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "可能的原因:" -ForegroundColor Yellow
    Write-Host "1. Repository 不存在 - 請先在 GitHub 上建立 Repository"
    Write-Host "2. 沒有權限 - 請確認您有該 Repository 的寫入權限"
    Write-Host "3. 需要登入 - 第一次推送時需要輸入 GitHub 帳號密碼或 Token"
    Write-Host ""
    Write-Host "請參考 GITHUB_UPLOAD_GUIDE.md 取得詳細說明" -ForegroundColor Cyan
    Write-Host ""
}
