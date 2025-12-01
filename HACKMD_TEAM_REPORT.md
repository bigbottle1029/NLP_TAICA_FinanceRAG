# ICAIF-24 Finance RAG Challenge - 專案進度報告

> **GitHub Repository**: https://github.com/bigbottle1029/NLP_TAICA_FinanceRAG
> 
> **更新時間**: 2025-12-01
> 

---

## 📌 專案概述

我們正在參加 [ICAIF-24 Finance RAG Challenge](https://www.kaggle.com/competitions/icaif-24-finance-rag-challenge/overview)，目標是建立一個高效能的金融領域 RAG (Retrieval-Augmented Generation) 系統。

### 🎯 核心目標
- 開發能夠精準檢索金融文檔的 RAG 系統
- 整合第一名和第二名的優秀策略
- 在 FinDER 資料集上達到高準確率

---

## ✅ 已完成的工作

### 1. 📚 資料集分析
- ✅ 成功載入 **FinDER 資料集** (5,703 個樣本)
- ✅ 分析資料特性與挑戰
- ✅ 識別四大關鍵挑戰:
  - 數字精準度要求
  - 時間敏感性 (FY2020 vs FY2021)
  - 金融術語與縮寫
  - 多步驟推理需求

**詳細分析**: 請見 `analysis_report.md`

### 2. 🔍 Kaggle Codes 分析
已深入分析兩組重要的 Kaggle 程式碼:

#### Code 1: Official Baseline
- **架構**: Dense Retrieval (e5-large-v2) + CrossEncoder Reranking
- **優點**: 語意理解能力強
- **缺點**: 無法精準匹配關鍵字和數字

#### Code 2: FinanceBench Text Splitter
- **發現**: CharacterTextSplitter 比 RecursiveCharacterTextSplitter 更適合金融文檔
- **原因**: 保持表格與結構化數據的完整性

### 3. 💡 系統架構設計
設計並實作了 **Hybrid RAG Architecture**，整合冠亞軍策略:

```
Query → Query Span Extraction → Hybrid Retrieval → Multi-Stage Reranking → Top 10
         (2nd Place)              (1st Place)        (1st & 2nd Place)
```

**核心創新**:
1. **Query Span Extraction**: 提取實體、指標、時間等關鍵約束
2. **Hybrid Retrieval**: 結合 Dense (語意) + Sparse (關鍵字) 檢索
3. **Multi-Stage Reranking**: 兩階段精排

### 4. 💻 程式碼實作
已完成以下核心程式:

| 檔案 | 功能 | 狀態 |
|------|------|------|
| `advanced_rag_architecture.py` | Hybrid RAG 系統 | ✅ 完成 |
| `analyze_dataset.py` | 資料集分析 | ✅ 完成 |
| `baseline_demo.py` | Baseline 實作 | ✅ 完成 |
| `splitter_benchmark_reference.py` | Text Splitter 參考 | ✅ 完成 |

### 5. 📄 文檔撰寫
完成以下文檔:

- ✅ `README.md` - 完整專案說明
- ✅ `PRESENTATION_SUMMARY.md` - 簡報大綱 (10-15分鐘)
- ✅ `DATA_DOWNLOAD.md` - 資料下載指南
- ✅ `analysis_report.md` - 資料分析報告

---

## 🏗️ 系統架構詳解

### 架構圖
```
┌─────────────┐
│   Query     │  "What was Apple's revenue in FY2020?"
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│  Query Span Extraction      │  → ['Apple', 'revenue', 'FY2020']
│  (2nd Place Strategy)       │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  Hybrid Retrieval           │
│  ├─ Dense (bge-m3)          │  → Semantic Understanding
│  └─ Sparse (BM25)           │  → Exact Keyword Matching
│  (1st Place Strategy)       │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  Multi-Stage Reranking      │
│  ├─ Stage 1: Top 200        │  → Lightweight Reranker
│  └─ Stage 2: Top 10         │  → Precision Reranker
└──────┬──────────────────────┘
       │
       ▼
┌─────────────┐
│  Top 10     │
│  Results    │
└─────────────┘
```

### 技術細節

#### 1. Query Span Extraction
```python
# 目前實作: Regex + 啟發式規則
spans = re.findall(r'\b[A-Z][a-zA-Z]*\b|\b\d{4}\b|\bFY\d{2,4}\b', query)

# 未來升級: LLM-based Extraction
# 使用 GPT-4o 或本地 LLM 進行更精準的實體提取
```

#### 2. Hybrid Retrieval
```python
# 融合公式
Score_final = α × Norm(Score_dense) + (1-α) × Norm(Score_BM25)

# α = 0.5 (預設值，可調整)
# α = 1.0 → 純向量檢索
# α = 0.0 → 純關鍵字檢索
```

---

## 📊 初步測試結果

### 測試場景
設計了「陷阱查詢」來驗證系統優勢:

#### Test Case 1: 時間約束
- **Query**: "What was Apple's revenue in FY2020?"
- **挑戰**: 區分 FY2020 vs FY2021
- **Baseline**: 可能混淆年份 ❌
- **Advanced**: 正確匹配 FY2020 ✅

#### Test Case 2: 實體區分
- **Query**: "fixed asset turnover ratio for Tesla 2019"
- **挑戰**: 區分 Tesla vs Apple
- **Baseline**: 可能混淆公司 ❌
- **Advanced**: 正確識別 Tesla ✅

---

## 🚀 下一步計畫

### 短期 (本週)
- [ ] 在完整 FinDER 資料集上運行評估
- [ ] 計算 NDCG@10, MAP@10, Recall@10 指標
- [ ] 調整 Hybrid Fusion 參數 (α)
- [ ] 準備簡報內容

### 中期 (下週)
- [ ] 測試不同的 Reranker 模型
  - jinaai/jina-reranker-v2
  - BAAI/bge-reranker-v2-m3
- [ ] 實作 ColBERT Late Interaction
- [ ] 優化 Query Span Extraction (考慮使用 LLM)

### 長期 (未來)
- [ ] Fine-tune Embedding Model on Financial Data
- [ ] 處理表格數據 (Table Extraction)
- [ ] 整合 LLM 進行 Answer Generation

---

## 📦 如何使用我的程式碼

### 1. Clone Repository
```bash
git clone https://github.com/bigbottle1029/NLP_TAICA_FinanceRAG.git
cd NLP_TAICA_FinanceRAG
```

### 2. 安裝依賴
```bash
pip install -r requirements.txt
```

### 3. 下載資料集
```bash
# 資料集會自動從 Hugging Face 下載
python analyze_dataset.py
```

### 4. 運行系統
```bash
# 測試 Hybrid RAG 系統
python advanced_rag_architecture.py
```

---

## 💬 討論與協作

### 需要組員協助的部分

#### 1. 資料預處理
- [ ] 測試不同的 Text Splitting 策略
- [ ] 處理表格數據的提取

#### 2. 模型實驗
- [ ] 測試不同的 Embedding Models
- [ ] 比較不同的 Reranker 效能

#### 3. 評估與分析
- [ ] 在其他資料集上測試 (FinanceBench, TATQA)
- [ ] 錯誤分析與 Case Study

#### 4. 簡報準備
- [ ] PPT 設計
- [ ] Demo 影片錄製

### 如何貢獻

1. **Fork** 或 **Clone** Repository
2. 建立新的 **Branch**: `git checkout -b feature/your-feature`
3. **Commit** 變更: `git commit -m "Add your feature"`
4. **Push** 到 GitHub: `git push origin feature/your-feature`
5. 建立 **Pull Request**

---

## 📚 參考資料

### 競賽相關
- [Competition Page](https://www.kaggle.com/competitions/icaif-24-finance-rag-challenge/overview)
- [FinDER Dataset](https://huggingface.co/datasets/Linq-AI-Research/FinDER)

### 技術文檔
- [BAAI/bge-m3 Model](https://huggingface.co/BAAI/bge-m3)
- [Jina Reranker](https://huggingface.co/jinaai/jina-reranker-v2-base-multilingual)

### 學習資源
- 1st Place Solution: Hybrid Search + ColBERT
- 2nd Place Solution: Query Expansion + Multi-Stage Reranking

---

## 🎯 總結

### 我們的優勢
1. ✅ **完整的系統架構**: 整合冠亞軍策略
2. ✅ **實作完成**: 可運行的程式碼
3. ✅ **詳細文檔**: 完整的技術說明
4. ✅ **資料分析**: 深入理解資料特性

### 挑戰與機會
- 🔄 需要在真實資料集上進行完整評估
- 🔄 可以進一步優化 Query Understanding (使用 LLM)
- 🔄 有機會 Fine-tune 模型以提升效能

---

## 📞 聯絡方式

- **GitHub**: https://github.com/bigbottle1029/NLP_TAICA_FinanceRAG

---

**最後更新**: 2025-12-01
**版本**: v1.0

歡迎組員提出問題、建議或直接貢獻程式碼！💪
