# ICAIF-24 Finance RAG Challenge - Team Solution

## 🏆 Project Overview
This project develops a high-performance Retrieval-Augmented Generation (RAG) system for the [ICAIF-24 Finance RAG Challenge](https://www.kaggle.com/competitions/icaif-24-finance-rag-challenge/overview). Our solution integrates the engineering excellence of the **1st Place Solution** with the advanced query understanding strategies of the **2nd Place Solution** to handle complex financial queries with high precision.

---

## 📂 Project Structure

```
NLP_TAICA/
├── 📄 Core Implementation
│   ├── advanced_rag_architecture.py    # Our Hybrid RAG System (Main)
│   ├── baseline_demo.py                # Official Baseline for Comparison
│   ├── analyze_dataset.py              # Dataset Analysis Script
│   └── splitter_benchmark_reference.py # Text Splitter Experiments
│
├── 📋 Documentation
│   ├── README.md                       # This file
│   ├── PRESENTATION_SUMMARY.md         # Presentation Outline (10-15 min)
│   ├── analysis_report.md              # FinDER Dataset Analysis Results
│   ├── DATA_DOWNLOAD.md                # Data Download Instructions
│   └── FILE_INVENTORY.md               # File Purpose Descriptions
│
└── 📦 Configuration
    └── requirements.txt                # Python Dependencies
```

---

## 🏗️ System Architecture

We have designed a **Hybrid RAG Architecture** that addresses the specific challenges of financial data (e.g., exact number matching, specific time periods, and complex entity relationships).

### 1. Query Understanding (Pre-Retrieval)
*Inspired by the 2nd Place Solution*
*   **Query Span Extraction**: 
    *   **Goal**: To capture specific financial constraints that semantic search might miss.
    *   **Method**: Extracts **Entities** (e.g., "Apple", "TSLA"), **Metrics** (e.g., "Revenue", "ROIC"), and **Time Periods** (e.g., "FY2022", "Q3 2021").
    *   **Implementation**: Currently uses Regex/Heuristics; planned upgrade to LLM-based extraction.

### 2. Hybrid Retrieval
*Inspired by the 1st Place Solution*
*   **Dense Retrieval (Vector Search)**:
    *   **Model**: `BAAI/bge-m3` (State-of-the-art multilingual embedding model).
    *   **Purpose**: Captures semantic meaning and context.
*   **Sparse Retrieval (Keyword Search)**:
    *   **Model**: `BM25Okapi`.
    *   **Purpose**: Ensures exact matches for critical entities and numbers extracted during the Query Span phase.
*   **Fusion Strategy**:
    *   Scores from Dense and Sparse retrievers are normalized and combined using a **Weighted Sum** (alpha parameter).

### 3. Multi-Stage Reranking
*   **Stage 1 (Lightweight)**: 
    *   Reranks top-200 candidates.
    *   **Model**: `jinaai/jina-reranker-v2-base-multilingual` (Efficient and supports long context).
*   **Stage 2 (Precision)**: 
    *   Reranks top-10/20 candidates.
    *   **Model**: `Cross-Encoder` (e.g., `ms-marco-MiniLM-L-12-v2`) or `ColBERT` (Late Interaction).

---

## 🚀 Getting Started

### 1. Prerequisites
*   Python 3.10 or higher
*   GPU with CUDA support (Recommended for Embeddings and Reranking)

### 2. Installation
```bash
# Install dependencies
pip install -r requirements.txt
```

### 3. Download Dataset
Follow instructions in `DATA_DOWNLOAD.md` to download the FinDER dataset from Hugging Face.

### 4. Run Analysis
```bash
# Analyze FinDER dataset
python analyze_dataset.py

# This will generate: analysis_report.md
```

### 5. Run Advanced RAG System
```bash
# Test the Hybrid RAG system with dummy data
python advanced_rag_architecture.py
```

---

## 📊 Dataset: FinDER

### Overview
- **Source**: [Linq-AI-Research/FinDER](https://huggingface.co/datasets/Linq-AI-Research/FinDER)
- **Size**: 5,703 samples
- **Domain**: 10-K Reports (US Public Company Annual Filings)
- **Features**: 
  - `_id`: Document ID
  - `text`: Financial text content
  - `category`: Document category (e.g., Company overview, Footnotes)
  - `answer`: Ground truth answer
  - `references`: Reference materials

### Key Challenges
1. **Numerical Precision**: Financial data must be 100% accurate
2. **Temporal Constraints**: FY2020 vs FY2021 data are completely different
3. **Domain Jargon**: EBITDA, ROIC, P/E Ratio require domain knowledge
4. **Multi-Step Reasoning**: Requires extracting data from multiple documents and performing calculations

---

## 🔬 Technical Implementation Details

### Query Span Logic (`QueryProcessor`)
We currently use a heuristic approach to identify spans:
```python
# Extracts capitalized words (Entities) and Year patterns (Time)
spans = re.findall(r'\b[A-Z][a-zA-Z]*\b|\b\d{4}\b|\bFY\d{2,4}\b', query)
```
*Future Improvement*: Replace with an LLM call: `extract_entities(query) -> JSON`.

### Hybrid Search Logic (`HybridRetriever`)
We combine scores mathematically:
$$ Score_{final} = \alpha \cdot Norm(Score_{dense}) + (1-\alpha) \cdot Norm(Score_{bm25}) $$
*   **Alpha**: Controls the balance. 1.0 is pure Vector, 0.0 is pure Keyword. We default to 0.5.

---

## 📝 Key Learnings from Kaggle Codes

### From Baseline (Official FinanceRAG)
1. **Dense Retrieval is Foundation**: SentenceTransformer provides strong semantic understanding
2. **Reranking is Important**: CrossEncoder can further improve precision
3. **But Semantics Alone is Not Enough**: Financial domain requires keyword matching

### From Text Splitter Experiments (FinanceBench)
1. **Preprocessing Strategy Matters**: Wrong splitting can reduce accuracy by 40%+
2. **CharacterTextSplitter is Better for Financial Docs**: Maintains structural integrity
3. **Chunk Size Needs Careful Tuning**: Too small loses context, too large affects retrieval efficiency

---

## 💡 Our Innovation

### Core Innovation: Hybrid RAG with Query Span Extraction

#### Innovation 1: Query Span Extraction (2nd Place Strategy)
**Purpose**: Extract key constraints from queries
```python
Query: "What was Apple's revenue in FY2020?"
Extracted Spans: ['Apple', 'revenue', 'FY2020']
```

#### Innovation 2: Hybrid Retrieval (1st Place Strategy)
**Formula**:
```
Score_final = α × Score_dense + (1-α) × Score_BM25
```

**Advantages**:
- **Dense (Vector)**: Captures semantic similarity
- **Sparse (BM25)**: Ensures exact keyword matching (e.g., "FY2020", "Apple")
- **Fusion**: Combines both for semantic understanding AND exact matching

#### Innovation 3: Multi-Stage Reranking
1. **Stage 1**: Lightweight Reranker (Top 200)
2. **Stage 2**: Precision Reranker (Top 10)

---

## 📈 Roadmap

- [x] **Phase 1: Foundation**
    - [x] Setup Baseline (FinDER)
    - [x] Analyze Text Splitters
    - [x] Design Hybrid Architecture
    - [x] Load Real Dataset (FinDER)

- [x] **Phase 2: Core Implementation**
    - [x] Implement Hybrid Retriever (Dense + Sparse)
    - [x] Implement Basic Query Span Extraction
    - [x] Analyze FinDER Dataset

- [ ] **Phase 3: Evaluation & Optimization**
    - [ ] Run Full Evaluation on FinDER Dataset
    - [ ] Calculate NDCG@10, MAP@10, Recall@10
    - [ ] Tune Hybrid Fusion Parameter (α)
    - [ ] Test Different Reranker Models

- [ ] **Phase 4: Advanced Features**
    - [ ] **LLM Integration**: Use GPT-4o or Local LLM for Query Understanding
    - [ ] **Fine-tuning**: Fine-tune Embedding model on financial pairs
    - [ ] **Table Extraction**: Special handling for tabular data in financial reports
    - [ ] **ColBERT Integration**: Implement Late Interaction Reranking

---

## 📚 References
*   [Competition Overview](https://www.kaggle.com/competitions/icaif-24-finance-rag-challenge/overview)
*   **1st Place Solution**: Hybrid Search + ColBERT
*   **2nd Place Solution**: Query Expansion + Corpus Refinement
*   **Models**:
    *   Embedding: [BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)
    *   Reranker: [jina-reranker-v2](https://huggingface.co/jinaai/jina-reranker-v2-base-multilingual)
*   **Dataset**: [Linq-AI-Research/FinDER](https://huggingface.co/datasets/Linq-AI-Research/FinDER)

---

## 🎯 For Presentation

Please refer to `PRESENTATION_SUMMARY.md` for the complete presentation outline covering:
1. Dataset Introduction
2. Analysis of Two Kaggle Codes
3. Data Challenges
4. Our Solution
5. Preliminary Results
6. Future Work

---

## 👥 Team
- [Your Team Name]
- [Team Members]

## 📧 Contact
- [Your Email]
- [GitHub Repository]
