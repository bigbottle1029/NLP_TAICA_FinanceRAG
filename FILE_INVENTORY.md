# 檔案清單與用途說明

## 📁 核心檔案 (必須保留)

### 1. **advanced_rag_architecture.py** ⭐
- **用途**: 完整的 Hybrid RAG 系統實作
- **包含**: QueryProcessor, HybridRetriever, AdvancedReranker, FinanceRAGSystem
- **狀態**: 可運行，已測試
- **保留原因**: 這是我們的核心創新實作

### 2. **analyze_dataset.py** ⭐
- **用途**: 分析 FinDER 資料集，生成統計報告
- **輸出**: analysis_report.md
- **狀態**: 可運行，已測試
- **保留原因**: 用於簡報中的資料介紹部分

### 3. **baseline_demo.py** ⭐
- **用途**: 官方 Baseline 實作 (純 Dense Retrieval)
- **狀態**: 需要安裝 financerag 庫才能運行
- **保留原因**: 用於對比實驗，展示 Baseline 方法

### 4. **requirements.txt** ⭐
- **用途**: Python 依賴套件清單
- **保留原因**: 環境安裝必需

---

## 📄 文檔檔案 (必須保留)

### 5. **README.md** ⭐
- **用途**: 專案主文檔，技術架構說明
- **保留原因**: GitHub/報告必備

### 6. **PRESENTATION_SUMMARY.md** ⭐
- **用途**: 簡報大綱，回答所有報告問題
- **保留原因**: 簡報腳本

### 7. **analysis_report.md** ⭐
- **用途**: FinDER 資料集分析結果
- **保留原因**: 簡報數據來源

### 8. **DATA_DOWNLOAD.md** ⭐
- **用途**: 資料下載指南
- **保留原因**: 說明如何取得競賽資料

---

## 🗑️ 可刪除的檔案 (測試/中間產物)

### 9. **comparison_analysis.py** ❌
- **用途**: Baseline vs Advanced 對比測試
- **問題**: 使用 Dummy Data，不是真實資料
- **建議**: 刪除 (功能已整合到 advanced_rag_architecture.py)

### 10. **simple_check.py** ❌
- **用途**: 簡化版測試腳本
- **問題**: 也是用 Dummy Data
- **建議**: 刪除

### 11. **inspect_dataset.py** ❌
- **用途**: Debug 用，檢查資料集結構
- **建議**: 刪除 (功能已被 analyze_dataset.py 取代)

### 12. **load_real_data.py** ❌
- **用途**: 載入資料並儲存樣本
- **問題**: 功能已整合到 analyze_dataset.py
- **建議**: 刪除

### 13. **splitter_benchmark_reference.py** ⚠️
- **用途**: Text Splitter 實驗參考程式碼
- **建議**: 保留 (作為第二組 Kaggle Code 的參考)

---

## 📝 輸出檔案 (可刪除)

### 14. **output.txt** ❌
- **用途**: 測試輸出
- **建議**: 刪除

### 15. **simple_output.txt** ❌
- **用途**: 測試輸出
- **建議**: 刪除

### 16. **comparison_output.txt** ❌
- **用途**: 測試輸出
- **建議**: 刪除

### 17. **comparison_output_clean.txt** ❌
- **用途**: 測試輸出
- **建議**: 刪除

---

## 📂 目錄

### 18. **FinanceRAG/** ⚠️
- **用途**: 官方 FinanceRAG 庫的 Git Clone
- **建議**: 可刪除 (我們不直接使用，只參考架構)

---

## 總結

### 必須保留 (10 個)
1. advanced_rag_architecture.py
2. analyze_dataset.py
3. baseline_demo.py
4. splitter_benchmark_reference.py
5. requirements.txt
6. README.md
7. PRESENTATION_SUMMARY.md
8. analysis_report.md
9. DATA_DOWNLOAD.md

### 建議刪除 (8 個)
1. comparison_analysis.py
2. simple_check.py
3. inspect_dataset.py
4. load_real_data.py
5. output.txt
6. simple_output.txt
7. comparison_output.txt
8. comparison_output_clean.txt
9. FinanceRAG/ (目錄)
