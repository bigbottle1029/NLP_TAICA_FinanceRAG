import logging
from sentence_transformers import CrossEncoder
from financerag.rerank import CrossEncoderReranker
from financerag.retrieval import DenseRetrieval, SentenceTransformerEncoder
from financerag.tasks import FinDER

def run_baseline():
    # Setup basic logging configuration
    logging.basicConfig(level=logging.INFO)

    # Step 2: Initialize FinDER Task
    print("Initializing FinDER Task...")
    finder_task = FinDER()

    # Step 3: Initialize DenseRetriever model
    print("Initializing Retrieval Model...")
    encoder_model = SentenceTransformerEncoder(
        model_name_or_path='intfloat/e5-large-v2',
        query_prompt='query: ',
        doc_prompt='passage: ',
    )

    retrieval_model = DenseRetrieval(
        model=encoder_model
    )

    # Step 4: Perform retrieval
    print("Performing Retrieval...")
    retrieval_result = finder_task.retrieve(
        retriever=retrieval_model
    )

    # Print a portion of the retrieval results
    print(f"Retrieved results for {len(retrieval_result)} queries. Here's an example of the top 5 documents for the first query:")
    for q_id, result in retrieval_result.items():
        print(f"\nQuery ID: {q_id}")
        sorted_results = sorted(result.items(), key=lambda x: x[1], reverse=True)
        for i, (doc_id, score) in enumerate(sorted_results[:5]):
            print(f"  Document {i + 1}: Document ID = {doc_id}, Score = {score}")
        break

    # Step 5: Initialize CrossEncoder Reranker
    print("Initializing Reranker...")
    reranker = CrossEncoderReranker(
        model=CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2')
    )

    # Step 6: Perform reranking
    print("Performing Reranking...")
    reranking_result = finder_task.rerank(
        reranker=reranker,
        results=retrieval_result,
        top_k=100,
        batch_size=32
    )

    # Print a portion of the reranking results
    print(f"Reranking results for {len(reranking_result)} queries. Here's an example of the top 5 documents for the first query:")
    for q_id, result in reranking_result.items():
        print(f"\nQuery ID: {q_id}")
        sorted_results = sorted(result.items(), key=lambda x: x[1], reverse=True)
        for i, (doc_id, score) in enumerate(sorted_results[:5]):
            print(f"  Document {i + 1}: Document ID = {doc_id}, Score = {score}")
        break

    # Step 7: Save results
    output_dir = './results'
    finder_task.save_results(output_dir=output_dir)
    print(f"Results have been saved to {output_dir}/FinDER/results.csv")

if __name__ == "__main__":
    run_baseline()
