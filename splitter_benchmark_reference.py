import pandas as pd
import os
import gzip
import json
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    Language,
)
from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from tqdm import tqdm
from typing import List, Dict, Optional
from sentence_transformers import CrossEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")
import logging
logging.disable(logging.CRITICAL)

# Configuration
DATA_DIR = "data"
PARENT_DIR = "./vectordbs"
CHAR_SIZES = [64, 128, 256, 368, 512]
RECURSIVE_SIZES = CHAR_SIZES
RECURSIVE_OVERLAP = 20

def load_corpus():
    records = []
    file_path = os.path.join(DATA_DIR, "financebench_corpus.jsonl.gz")
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return pd.DataFrame()
        
    with gzip.open(file_path, "rt", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            data["source_file"] = "financebench_corpus.jsonl.gz"
            records.append(data)
    
    df = pd.DataFrame(records)
    df.dropna(inplace=True)
    df.drop_duplicates('_id', inplace=True)
    return df

def rowdict_iter(df: pd.DataFrame):
    cols = list(df.columns)
    for vals in df.itertuples(index=False, name=None):
        yield dict(zip(cols, vals))

def _coerce_text(x: Optional[str]) -> str:
    if x is None:
        return ""
    if isinstance(x, float) and pd.isna(x):
        return ""
    return str(x)

def _emit_rows(base_row: Dict, splitter_name: str, chunk_size: int, chunk_overlap: int, chunks: List[str]) -> List[Dict]:
    return [
        {
            **base_row,
            "splitter": splitter_name,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "chunk_index": i,
            "chunk_text": ch,
        }
        for i, ch in enumerate(chunks)
    ]

def _chunk_all_rows_with_splitter(df: pd.DataFrame, splitter, splitter_name: str, size: int, overlap: int) -> List[Dict]:
    rows: List[Dict] = []
    for rd in rowdict_iter(df):
        base = {
            "_id": rd.get("_id"),
            "title": rd.get("title"),
            "source_file": rd.get("source_file"),
        }
        text = _coerce_text(rd.get("text", ""))
        if not text:
            continue
        chunks = splitter.split_text(text)
        rows.extend(_emit_rows(base, f"{splitter_name}_{size}", size, overlap, chunks))
    return rows

def make_all_chunks_with_docs(df: pd.DataFrame) -> pd.DataFrame:
    if df.index.name and df.index.name not in df.columns:
        df = df.reset_index()

    all_rows: List[Dict] = []
    
    with tqdm(total=2, desc="Chunking pipeline", ncols=100) as pbar:
        for size in CHAR_SIZES:
            s = CharacterTextSplitter(chunk_size=size, chunk_overlap=0)
            all_rows.extend(_chunk_all_rows_with_splitter(df, s, "character", size, 0))
        pbar.update(1)

        for size in RECURSIVE_SIZES:
            s = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=RECURSIVE_OVERLAP)
            all_rows.extend(_chunk_all_rows_with_splitter(df, s, "recursive", size, RECURSIVE_OVERLAP))
        pbar.update(1)

    chunks_df = pd.DataFrame(all_rows)
    cols = ["_id", "title", "source_file", "splitter", "chunk_size", "chunk_overlap", "chunk_index", "chunk_text"]
    chunks_df = chunks_df[[c for c in cols if c in chunks_df.columns] + [c for c in chunks_df.columns if c not in cols]]
    return chunks_df

# ... (Rest of the logic for Vector DB creation and Evaluation would go here)
# This file serves as a reference for the splitting logic.
