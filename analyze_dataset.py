"""
Analyze Real FinDER Dataset for Presentation
This script loads the actual FinDER dataset and performs analysis to answer:
1. Dataset characteristics
2. Challenges in financial RAG
3. Comparison of Baseline vs Advanced approaches
"""
import os
os.environ["TQDM_DISABLE"] = "1"

from datasets import load_dataset
import json
import re
from collections import Counter

def analyze_finder_dataset():
    """
    Analyze FinDER dataset structure and characteristics.
    """
    print("="*60)
    print("FINDER DATASET ANALYSIS")
    print("="*60)
    
    # Load dataset
    print("\n1. Loading Dataset...")
    dataset = load_dataset("Linq-AI-Research/FinDER")
    train_data = dataset['train']
    
    print(f"   Total samples: {len(train_data)}")
    print(f"   Features: {train_data.column_names}")
    
    # Analyze text lengths
    print("\n2. Text Length Analysis...")
    text_lengths = [len(sample['text']) for sample in train_data]
    print(f"   Average text length: {sum(text_lengths)/len(text_lengths):.0f} characters")
    print(f"   Min length: {min(text_lengths)}")
    print(f"   Max length: {max(text_lengths)}")
    
    # Analyze categories
    print("\n3. Category Distribution...")
    categories = [sample['category'] for sample in train_data if sample['category']]
    category_counts = Counter(categories)
    for cat, count in category_counts.most_common(10):
        print(f"   {cat}: {count}")
    
    # Analyze reasoning types
    print("\n4. Reasoning Types...")
    reasoning_types = []
    for sample in train_data:
        if sample['reasoning'] and isinstance(sample['reasoning'], list):
            for step in sample['reasoning']:
                if isinstance(step, dict) and 'type' in step:
                    reasoning_types.append(step['type'])
    
    if reasoning_types:
        reasoning_counts = Counter(reasoning_types)
        for rtype, count in reasoning_counts.most_common():
            print(f"   {rtype}: {count}")
    else:
        print("   No reasoning type information available")
    
    # Identify challenges
    print("\n5. Financial RAG Challenges Identified...")
    
    # Challenge 1: Numerical reasoning
    num_with_numbers = sum(1 for s in train_data if re.search(r'\d+', s['text']))
    print(f"   - Documents with numbers: {num_with_numbers}/{len(train_data)} ({num_with_numbers/len(train_data)*100:.1f}%)")
    
    # Challenge 2: Multi-step reasoning
    num_multistep = sum(1 for s in train_data if isinstance(s['reasoning'], list) and len(s['reasoning']) > 1)
    print(f"   - Multi-step reasoning required: {num_multistep}/{len(train_data)} ({num_multistep/len(train_data)*100:.1f}%)")
    
    # Challenge 3: Financial jargon
    financial_terms = ['revenue', 'EBITDA', 'margin', 'asset', 'liability', 'equity', 'ROI', 'ROIC']
    num_with_jargon = sum(1 for s in train_data if any(term.lower() in s['text'].lower() for term in financial_terms))
    print(f"   - Documents with financial jargon: {num_with_jargon}/{len(train_data)} ({num_with_jargon/len(train_data)*100:.1f}%)")
    
    # Sample examples
    print("\n6. Sample Examples...")
    for i in range(min(3, len(train_data))):
        sample = train_data[i]
        print(f"\n   Example {i+1}:")
        print(f"   ID: {sample['_id']}")
        print(f"   Text: {sample['text'][:150]}...")
        print(f"   Category: {sample['category']}")
        if isinstance(sample['reasoning'], list):
            print(f"   Reasoning steps: {len(sample['reasoning'])}")
    
    return train_data

def save_analysis_report(train_data, output_file="./analysis_report.md"):
    """
    Save analysis results to a markdown file for presentation.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# FinDER Dataset Analysis Report\n\n")
        f.write("## Dataset Overview\n")
        f.write(f"- **Total Samples**: {len(train_data)}\n")
        f.write(f"- **Features**: {', '.join(train_data.column_names)}\n\n")
        
        f.write("## Key Challenges in Financial RAG\n\n")
        f.write("### 1. Numerical Precision\n")
        f.write("Financial documents contain critical numerical data (revenue, margins, ratios) that must be retrieved with exact precision.\n\n")
        
        f.write("### 2. Multi-Step Reasoning\n")
        num_multistep = sum(1 for s in train_data if isinstance(s['reasoning'], list) and len(s['reasoning']) > 1)
        f.write(f"- {num_multistep} samples require multi-step reasoning\n")
        f.write("- Example: Calculate YoY growth = (Revenue_2023 - Revenue_2022) / Revenue_2022\n\n")
        
        f.write("### 3. Domain-Specific Jargon\n")
        f.write("- Abbreviations: EBITDA, ROIC, P/E Ratio\n")
        f.write("- Context-dependent terms: 'Margin' can mean gross margin, operating margin, or net margin\n\n")
        
        f.write("### 4. Long Documents\n")
        text_lengths = [len(sample['text']) for sample in train_data]
        f.write(f"- Average document length: {sum(text_lengths)/len(text_lengths):.0f} characters\n")
        f.write(f"- Max document length: {max(text_lengths)} characters\n\n")
        
        f.write("## Why Baseline Approaches Fail\n\n")
        f.write("1. **Pure Semantic Search**: May retrieve documents about 'Apple revenue' when query asks for 'Apple FY2020 revenue', missing the year constraint.\n")
        f.write("2. **No Query Understanding**: Cannot distinguish between 'revenue' and 'revenue growth rate'.\n")
        f.write("3. **Weak on Exact Matches**: Struggles with specific entity names or fiscal periods.\n\n")
        
        f.write("## Our Solution: Hybrid RAG\n\n")
        f.write("1. **Query Span Extraction**: Extract entities (Apple), metrics (revenue), time (FY2020)\n")
        f.write("2. **Hybrid Retrieval**: Combine semantic similarity (Dense) + exact keyword matching (BM25)\n")
        f.write("3. **Multi-Stage Reranking**: Refine results with cross-encoder models\n\n")
    
    print(f"\nAnalysis report saved to {output_file}")

if __name__ == "__main__":
    train_data = analyze_finder_dataset()
    save_analysis_report(train_data)
