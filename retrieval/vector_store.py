from retrieval.embeddings import model, index, df
import faiss


def search_similar_cases(index, query_embedding, top_k=5):
    query_embedding = query_embedding.astype("float32").reshape(1, -1)

    distances, indices = index.search(query_embedding, top_k)

    return distances[0], indices[0]
def retrieve_cases(complaint, top_k=5):
    query_embedding = model.encode(complaint)

    distances, indices = search_similar_cases(
        index,
        query_embedding,
        top_k
    )

    results = df.iloc[indices].copy()
    results["distance"] = distances

    return results