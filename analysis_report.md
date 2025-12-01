# FinDER Dataset Analysis Report

## Dataset Overview
- **Total Samples**: 5703
- **Features**: _id, text, reasoning, category, references, answer, type

## Key Challenges in Financial RAG

### 1. Numerical Precision
Financial documents contain critical numerical data (revenue, margins, ratios) that must be retrieved with exact precision.

### 2. Multi-Step Reasoning
- 0 samples require multi-step reasoning
- Example: Calculate YoY growth = (Revenue_2023 - Revenue_2022) / Revenue_2022

### 3. Domain-Specific Jargon
- Abbreviations: EBITDA, ROIC, P/E Ratio
- Context-dependent terms: 'Margin' can mean gross margin, operating margin, or net margin

### 4. Long Documents
- Average document length: 76 characters
- Max document length: 331 characters

## Why Baseline Approaches Fail

1. **Pure Semantic Search**: May retrieve documents about 'Apple revenue' when query asks for 'Apple FY2020 revenue', missing the year constraint.
2. **No Query Understanding**: Cannot distinguish between 'revenue' and 'revenue growth rate'.
3. **Weak on Exact Matches**: Struggles with specific entity names or fiscal periods.

## Our Solution: Hybrid RAG

1. **Query Span Extraction**: Extract entities (Apple), metrics (revenue), time (FY2020)
2. **Hybrid Retrieval**: Combine semantic similarity (Dense) + exact keyword matching (BM25)
3. **Multi-Stage Reranking**: Refine results with cross-encoder models

