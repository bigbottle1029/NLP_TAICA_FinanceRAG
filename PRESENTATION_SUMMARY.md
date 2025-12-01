# ICAIF-24 Finance RAG Challenge - Presentation Summary

## 📊 1. 資料介紹 (Dataset Introduction)

### FinDER Dataset (Linq-AI-Research)
- **規模**: 5,703 個樣本
- **來源**: 10-K Reports (美國上市公司年度財務報告)
- **特徵**: 
  - `_id`: 文檔唯一識別碼
  - `text`: 財務文本內容
  - `category`: 文檔類別 (如 Company overview, Footnotes 等)
  - `answer`: 正確答案
  - `references`: 參考資料

### 資料特性
- **平均文本長度**: 76 字元 (這是經過預處理的片段)
- **最長文本**: 331 字元
- **數字密集度**: 幾乎所有文檔都包含數字 (99%+)
- **金融術語**: 高頻出現 revenue, margin, asset, liability 等專業詞彙

---

## 🔍 2. 分析兩組 Kaggle Codes

### Code 1: Baseline (Official FinanceRAG GitHub)
**架構**:
```
Query → Dense Retrieval (e5-large-v2) → CrossEncoder Reranking → Top 10
```

**優點**:
- 簡單易實作
- 語意理解能力強 (Semantic Search)

**缺點**:
- **無法精準匹配關鍵字**: 例如查詢 "Apple FY2020 revenue" 可能會檢索到 "Apple FY2021 revenue"
- **忽略實體與時間約束**: 純向量相似度無法區分 "2020" vs "2021"
- **對數字不敏感**: 無法確保檢索到的數字是正確的

### Code 2: FinanceBench Character vs Recursive TextSplitter
**核心發現**:
- **CharacterTextSplitter** 在金融文檔上表現更穩定 (準確率 72-76%)
- **RecursiveCharacterTextSplitter** 對 Chunk Size 敏感，小 Chunk 會導致準確率暴跌 (32%)

**原因**:
- 金融文檔包含大量表格與結構化數據
- Recursive Splitter 在切分時容易破壞表格結構
- Character Splitter 保持了更好的上下文完整性

---

## 💡 3. 資料困難點敘述 (Challenges)

### Challenge 1: 數字精準度 (Numerical Precision)
- **問題**: 財務數據必須 100% 精準，錯一個數字就全錯
- **案例**: "Revenue of $365 billion" vs "$274 billion" —— 語意相似但數字不同

### Challenge 2: 時間敏感性 (Temporal Constraints)
- **問題**: FY2020 vs FY2021 的數據完全不同
- **Baseline 失敗原因**: 純語意搜尋無法區分時間差異

### Challenge 3: 金融縮寫與術語 (Domain Jargon)
- **問題**: EBITDA, ROIC, P/E Ratio 等縮寫需要領域知識
- **問題**: "Margin" 可能指 Gross Margin, Operating Margin, 或 Net Margin

### Challenge 4: 多步驟推理 (Multi-Step Reasoning)
- **問題**: 需要從多個文檔中提取數據並計算
- **案例**: YoY Growth = (Revenue_2023 - Revenue_2022) / Revenue_2022

---

## 🚀 4. Key Content: 從 Kaggle Codes 學到什麼？

### 從 Baseline 學到:
1. **Dense Retrieval 是基礎**: SentenceTransformer 提供了強大的語意理解能力
2. **Reranking 很重要**: CrossEncoder 可以進一步提升精準度
3. **但單靠語意不夠**: 在金融領域需要結合關鍵字匹配

### 從 Text Splitter 實驗學到:
1. **預處理策略影響巨大**: 錯誤的切分會導致準確率下降 40%+
2. **CharacterTextSplitter 更適合金融文檔**: 保持結構完整性
3. **Chunk Size 需要謹慎調整**: 太小會丟失上下文，太大會影響檢索效率

---

## 💎 5. 我們的新想法 (New Idea)

### 核心創新: Hybrid RAG with Query Span Extraction

#### 創新點 1: Query Span Extraction (第二名策略)
**目的**: 從查詢中提取關鍵約束條件
```python
Query: "What was Apple's revenue in FY2020?"
Extracted Spans: ['Apple', 'revenue', 'FY2020']
```

**實作**:
- 目前使用 Regex + 啟發式規則
- 未來可升級為 LLM-based Extraction (GPT-4o)

#### 創新點 2: Hybrid Retrieval (第一名策略)
**公式**:
```
Score_final = α × Score_dense + (1-α) × Score_BM25
```

**優勢**:
- **Dense (向量)**: 捕捉語意相似度
- **Sparse (BM25)**: 確保關鍵字精準匹配 (如 "FY2020", "Apple")
- **Fusion**: 兩者結合，既有語意理解又有精準匹配

#### 創新點 3: Multi-Stage Reranking
1. **Stage 1**: 輕量級 Reranker (Top 200)
2. **Stage 2**: 精準 Reranker (Top 10)

---

## 📈 6. 初步結果 (Preliminary Results)

### 測試場景
我們設計了兩個「陷阱查詢」來測試 Baseline vs Advanced:

#### Test Case 1:
- **Query**: "What was Apple's revenue in FY2020?"
- **Corpus**: 包含 FY2020 和 FY2021 的 Apple revenue 文檔
- **Baseline**: 可能檢索到 FY2021 (因為語意相似)
- **Advanced**: 正確檢索到 FY2020 (因為 BM25 強制匹配 "FY2020")

#### Test Case 2:
- **Query**: "fixed asset turnover ratio for Tesla 2019"
- **Corpus**: 包含 Apple 和 Tesla 的 2019 數據
- **Baseline**: 可能混淆 Apple 和 Tesla
- **Advanced**: 正確區分 (Span Extraction 提取 "Tesla")

### 下一步: 真實資料集評估
- 已成功載入 FinDER 資料集 (5,703 樣本)
- 將在真實資料上運行 Baseline vs Advanced 比較
- 計算 NDCG@10, MAP@10, Recall@10 等指標

---

## 🎯 7. 結論與未來工作

### 已完成
- ✅ 建立 Hybrid RAG 架構
- ✅ 實作 Query Span Extraction
- ✅ 整合 BM25 + Dense Retrieval
- ✅ 載入真實競賽資料

### 進行中
- 🔄 在 FinDER 資料集上進行完整評估
- 🔄 調整 Hybrid Fusion 參數 (α)
- 🔄 測試不同的 Reranker 模型

### 未來優化
- 🔮 使用 LLM 進行 Query Understanding
- 🔮 Fine-tune Embedding Model on Financial Data
- 🔮 實作 ColBERT Late Interaction Reranking
- 🔮 處理表格數據 (Table Extraction)

---

## 📚 References
1. **Competition**: [ICAIF-24 Finance RAG Challenge](https://www.kaggle.com/competitions/icaif-24-finance-rag-challenge)
2. **Dataset**: [Linq-AI-Research/FinDER](https://huggingface.co/datasets/Linq-AI-Research/FinDER)
3. **1st Place Solution**: Hybrid Search + ColBERT
4. **2nd Place Solution**: Query Expansion + Multi-Stage Reranking
5. **Our Code**: [GitHub Repository](https://github.com/your-repo)
