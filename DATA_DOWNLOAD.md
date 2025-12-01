# Data Download Instructions

## Competition Datasets
The ICAIF-24 Finance RAG Challenge provides 7 financial datasets across two categories:

### 1. Passage Retrieval
- **FinDER**: Search Queries over 10-K Reports (Domain-specific jargon)
- **FinQABench**: Search Queries over 10-K Reports (Hallucination detection)
- **FinanceBench**: Natural Queries over public filings (10-K, Annual Reports)

### 2. Tabular and Text Retrieval
- **TATQA**: Natural Queries with numerical reasoning (Tables + Text)
- **FinQA**: Complex Natural Queries over Earnings Reports (Multi-step reasoning)
- **ConvFinQA**: Conversational Queries (Multi-turn Q&A)
- **MultiHiertt**: Multi-Hop Queries (Hierarchical tables + text)

## How to Download

### Option 1: From Official GitHub (Recommended)
```bash
# Clone the FinanceRAG repository
git clone https://github.com/linq-rag/FinanceRAG.git
cd FinanceRAG

# The data should be in the 'data' directory
# Structure: data/<task_name>/corpus.jsonl, queries.jsonl, qrels.tsv
```

### Option 2: From Kaggle Competition Page
1. Go to: https://www.kaggle.com/competitions/icaif-24-finance-rag-challenge/data
2. Download the dataset files
3. Extract to `./data/` directory

## Expected Directory Structure
```
NLP_TAICA/
├── data/
│   ├── FinDER/
│   │   ├── corpus.jsonl
│   │   ├── queries.jsonl
│   │   └── qrels.tsv
│   ├── FinanceBench/
│   ├── FinQA/
│   └── ... (other tasks)
├── advanced_rag_architecture.py
└── README.md
```

## Next Steps
Once data is downloaded, we will:
1. Load real corpus and queries
2. Run Baseline vs Advanced comparison on actual financial documents
3. Generate performance metrics (NDCG@10, MAP@10, Recall@10)
