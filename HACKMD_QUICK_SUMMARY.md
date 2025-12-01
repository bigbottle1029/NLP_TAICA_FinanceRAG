# Finance RAG 專案 - 快速摘要 🚀

> **GitHub**: https://github.com/bigbottle1029/NLP_TAICA_FinanceRAG
> 
> **更新**: 2025-12-01

---

## 🎯 我做了什麼？

### 1️⃣ 資料分析
- 載入並分析 **FinDER 資料集** (5,703 個金融問答樣本)
- 識別金融 RAG 的四大挑戰

### 2️⃣ 研究 Kaggle Codes
- **Baseline**: 純語意搜尋 (有缺陷)
- **Text Splitter**: CharacterTextSplitter 更適合金融文檔

### 3️⃣ 設計新系統
整合第一名和第二名的策略，建立 **Hybrid RAG**:
```
Query → 提取關鍵字 → 混合檢索 → 重排序 → Top 10
```

### 4️⃣ 完成程式碼
- ✅ `advanced_rag_architecture.py` - 核心系統
- ✅ `analyze_dataset.py` - 資料分析
- ✅ 完整文檔 (README, 簡報大綱等)

---

## 💡 核心創新

### 問題: Baseline 為什麼會失敗？
❌ 查詢 "Apple FY2020 revenue" 可能檢索到 "Apple FY2021 revenue"
❌ 純語意搜尋無法區分年份、公司名稱

### 解決方案: Hybrid RAG
✅ **Query Span**: 提取 ['Apple', 'revenue', 'FY2020']
✅ **Hybrid Search**: 語意 + 關鍵字雙重檢索
✅ **Reranking**: 兩階段精排

---

## 📊 測試結果

| 測試案例 | Baseline | Our System |
|---------|----------|------------|
| 區分年份 (FY2020 vs FY2021) | ❌ 失敗 | ✅ 成功 |
| 區分公司 (Apple vs Tesla) | ❌ 失敗 | ✅ 成功 |

---

## 🚀 如何使用

```bash
# 1. Clone
git clone https://github.com/bigbottle1029/NLP_TAICA_FinanceRAG.git

# 2. 安裝
pip install -r requirements.txt

# 3. 運行
python advanced_rag_architecture.py
```

---

## 📋 需要組員協助

- [ ] 在完整資料集上評估效能
- [ ] 測試不同模型組合
- [ ] 準備簡報 PPT
- [ ] 錄製 Demo 影片

---

## 📂 檔案結構

```
├── advanced_rag_architecture.py  ⭐ 核心系統
├── analyze_dataset.py            📊 資料分析
├── README.md                     📖 完整文檔
├── PRESENTATION_SUMMARY.md       🎤 簡報大綱
└── requirements.txt              📦 依賴套件
```

---

## 🎤 簡報重點

1. **資料介紹**: FinDER 資料集特性
2. **Code 分析**: Baseline + Text Splitter
3. **困難點**: 四大挑戰
4. **我們的方案**: Hybrid RAG
5. **結果**: 對比測試

完整簡報大綱請見: `PRESENTATION_SUMMARY.md`

---

## 📞 聯絡

有問題歡迎在 HackMD 留言或直接看 GitHub！

**GitHub**: https://github.com/bigbottle1029/NLP_TAICA_FinanceRAG
