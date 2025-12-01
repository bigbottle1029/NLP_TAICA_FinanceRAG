import logging
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer, CrossEncoder
from rank_bm25 import BM25Okapi
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class RetrievalResult:
    doc_id: str
    score: float
    text: str
    metadata: Dict[str, Any]

class QueryProcessor:
    """
    Handles Query Expansion and Span/Keyword Extraction (2nd Place Strategy).
    """
    def __init__(self, llm_client=None):
        self.llm_client = llm_client # Placeholder for OpenAI/Local LLM client

    def extract_query_spans(self, query: str) -> List[str]:
        """
        Extracts specific spans/keywords from the query (e.g., 'FY2022', 'Boeing', 'tax rate').
        Matches the 2nd Place 'Keyword Extraction' / User's 'Query Span' requirement.
        
        Strategy:
        1. Use LLM if available (Best performance).
        2. Fallback to Regex/Heuristics (Baseline).
        """
        if self.llm_client:
            # TODO: Implement LLM call to extract entities
            # prompt = f"Extract financial entities, metrics, and time periods from: {query}"
            pass
        
        # Fallback Heuristic: Extract capitalized words, numbers, and specific financial terms
        # This is a basic implementation to demonstrate the concept.
        spans = re.findall(r'\b[A-Z][a-zA-Z]*\b|\b\d{4}\b|\bFY\d{2,4}\b', query)
        
        # Add specific financial keywords if present
        financial_terms = ["revenue", "profit", "margin", "tax", "asset", "liability", "turnover"]
        for term in financial_terms:
            if term in query.lower():
                spans.append(term)
                
        return list(set(spans))

    def expand_query(self, query: str) -> str:
        """
        Expands query using paraphrasing or HyDE.
        """
        # TODO: Implement expansion logic (e.g., generate a hypothetical answer)
        return query

class HybridRetriever:
    """
    Combines Dense (Vector) and Sparse (Keyword) retrieval (1st Place Strategy).
    """
    def __init__(self, embedding_model_name: str = 'BAAI/bge-m3'):
        logger.info(f"Loading embedding model: {embedding_model_name}")
        self.encoder = SentenceTransformer(embedding_model_name)
        self.bm25 = None
        self.corpus_texts = []
        self.corpus_ids = []
        self.corpus_embeddings = None

    def index_corpus(self, corpus: List[Dict[str, str]]):
        """
        Indexes corpus for both Dense and Sparse retrieval.
        corpus: List of dicts with 'id' and 'text' keys.
        """
        logger.info(f"Indexing {len(corpus)} documents...")
        self.corpus_ids = [doc['id'] for doc in corpus]
        self.corpus_texts = [doc['text'] for doc in corpus]

        # 1. Build BM25 Index (Sparse)
        tokenized_corpus = [doc.split(" ") for doc in self.corpus_texts]
        self.bm25 = BM25Okapi(tokenized_corpus)
        logger.info("BM25 Index built.")

        # 2. Create Embeddings (Dense)
        # Note: For large corpus, use batch encoding and save to disk/vector DB
        self.corpus_embeddings = self.encoder.encode(self.corpus_texts, convert_to_tensor=True, show_progress_bar=True)
        logger.info("Dense Embeddings created.")

    def retrieve(self, query: str, query_spans: List[str], top_k: int = 100, alpha: float = 0.5) -> List[RetrievalResult]:
        """
        Performs Hybrid Search:
        alpha: Weight for Dense Search (0.0 to 1.0). 1.0 = Pure Dense, 0.0 = Pure Sparse.
        """
        if not self.bm25 or self.corpus_embeddings is None:
            raise ValueError("Corpus not indexed!")

        # 1. Dense Retrieval
        query_embedding = self.encoder.encode(query, convert_to_tensor=True)
        # Cosine similarity
        from sentence_transformers.util import cos_sim
        dense_scores = cos_sim(query_embedding, self.corpus_embeddings)[0].cpu().numpy()

        # 2. Sparse Retrieval (BM25)
        # Enhance query with extracted spans for BM25
        bm25_query = query + " " + " ".join(query_spans)
        tokenized_query = bm25_query.split(" ")
        sparse_scores = self.bm25.get_scores(tokenized_query)

        # Normalize scores (Min-Max normalization for simple fusion)
        def normalize(scores):
            if np.max(scores) == np.min(scores):
                return scores
            return (scores - np.min(scores)) / (np.max(scores) - np.min(scores))

        dense_scores_norm = normalize(dense_scores)
        sparse_scores_norm = normalize(sparse_scores)

        # 3. Fusion (Weighted Sum)
        fused_scores = alpha * dense_scores_norm + (1 - alpha) * sparse_scores_norm

        # Get Top K
        top_indices = np.argsort(fused_scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append(RetrievalResult(
                doc_id=self.corpus_ids[idx],
                score=float(fused_scores[idx]),
                text=self.corpus_texts[idx],
                metadata={"dense_score": float(dense_scores[idx]), "sparse_score": float(sparse_scores[idx])}
            ))
            
        return results

class AdvancedReranker:
    """
    Implements Multi-Stage Reranking (2nd Place Strategy) or ColBERT (1st Place).
    """
    def __init__(self, model_name: str = 'cross-encoder/ms-marco-MiniLM-L-12-v2'):
        # Note: 1st place used ColBERT, 2nd place used jina-reranker-v2
        # Using a standard CrossEncoder here for demonstration. 
        # For ColBERT, we would need the 'ragatouille' library or similar.
        logger.info(f"Loading reranker model: {model_name}")
        self.reranker = CrossEncoder(model_name)

    def rerank(self, query: str, results: List[RetrievalResult], top_k: int = 10) -> List[RetrievalResult]:
        """
        Reranks the retrieved documents.
        """
        if not results:
            return []
            
        pairs = [[query, doc.text] for doc in results]
        scores = self.reranker.predict(pairs)
        
        # Update scores and resort
        for doc, score in zip(results, scores):
            doc.score = float(score)
            
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]

class FinanceRAGSystem:
    def __init__(self):
        self.query_processor = QueryProcessor()
        # Using BAAI/bge-m3 as it supports dense, sparse, and colbert-style (multi-vector)
        # But here we treat it as a dense model for simplicity in this hybrid setup
        self.retriever = HybridRetriever(embedding_model_name='BAAI/bge-m3') 
        self.reranker = AdvancedReranker(model_name='cross-encoder/ms-marco-MiniLM-L-12-v2')

    def index_data(self, corpus: List[Dict[str, str]]):
        self.retriever.index_corpus(corpus)

    def answer(self, query: str) -> List[RetrievalResult]:
        # 1. Process Query
        spans = self.query_processor.extract_query_spans(query)
        # expanded_query = self.query_processor.expand_query(query)
        
        print(f"Original Query: {query}")
        print(f"Extracted Spans: {spans}")
        
        # 2. Retrieve (Hybrid)
        # Pass extracted spans to boost sparse retrieval
        retrieved_docs = self.retriever.retrieve(query, query_spans=spans, top_k=200)
        
        # 3. Rerank
        top_docs = self.reranker.rerank(query, retrieved_docs, top_k=10)
        
        return top_docs

if __name__ == "__main__":
    # Dummy Data for Testing
    dummy_corpus = [
        {"id": "doc1", "text": "Apple Inc. reported a revenue of $365 billion in FY2021."},
        {"id": "doc2", "text": "Boeing's revenue decreased significantly due to the pandemic."},
        {"id": "doc3", "text": "The fixed asset turnover ratio for Apple in 2019 was 3.5."},
        {"id": "doc4", "text": "Microsoft's cloud business grew by 20%."},
    ]
    
    system = FinanceRAGSystem()
    system.index_data(dummy_corpus)
    
    # Example Query
    q = "What is the FY2019 fixed asset turnover ratio for Apple?"
    results = system.answer(q)
    
    print("\nTop Results:")
    for r in results:
        print(f"[{r.score:.4f}] {r.text}")
