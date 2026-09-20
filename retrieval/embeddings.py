import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
DATA_FILE = "data/maintenance_records.csv"

df = pd.read_csv(DATA_FILE)
def create_search_text(row):
    return (
        f"Equipment: {row['equipment_type']}. "
        f"Complaint: {row['complaint']}. "
        f"Symptoms: {row['symptoms']}. "
        f"Previous action: {row['previous_action']}. "
        f"Root cause: {row['root_cause']}. "
        f"Resolution: {row['resolution']}. "
        f"Technician notes: {row['technician_notes']}."
    )
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model loaded successfully!")
search_texts = df.apply(create_search_text, axis=1).tolist()

embeddings = model.encode(
    search_texts,
    show_progress_bar=True
)

print("All embeddings created successfully!")
print("Number of embeddings:", len(embeddings))
print("Embedding size:", embeddings.shape[1])

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings.astype("float32"))

print("FAISS index created successfully!")
print("Number of vectors in index:", index.ntotal)
