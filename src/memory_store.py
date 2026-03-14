import uuid
import time
from endee import Endee, Precision
from src.embeddings import generate_embeddings, DIMENSION

INDEX_NAME = "memoria_memory"

def get_client():
    return Endee()

def ensure_index(client):
    indexes = client.list_indexes()
    existing = list(indexes)

    if INDEX_NAME not in existing:
        try:
            print(f"[memoria] Creating index {INDEX_NAME}...")
            client.create_index(
                name=INDEX_NAME,
                dimension=DIMENSION,
                space_type="cosine",
                precision=Precision.INT8)
        except Exception:
            print(f"[memoria] Index already exists, continuing...")

    time.sleep(1)
    return client.get_index(INDEX_NAME)

# adding to memory
def add_memory(index, role: str, text: str) -> str:
    memory_id = str(uuid.uuid4())
    embedding = generate_embeddings(text)
    index.upsert([
        {
            "id": memory_id,
            "vector": embedding,
            "meta": {
                "role": role,
                "text": text,
                "timestamp": time.time()
            }
        }
    ])
    return memory_id

# search in memory
def search_memory(index, query: str, top_k: int = 5) -> list:
    query_vector = generate_embeddings(query)
    results = index.query(vector=query_vector, top_k=top_k, ef=128)
    memories = []
    for item in results:
        meta = item.get("meta", {})
        memories.append({
            "id": item["id"],
            "role": meta.get("role", "unknown"),
            "text": meta.get("text", ""),
            "similarity": item.get("similarity", 0.0),
            "timestamp": meta.get("timestamp", 0)
        })
    return memories

# delete from memory
def delete_memory(index, text: str, threshold: float = 0.75) -> int:
    query_vector = generate_embeddings(text)
    results = index.query(vector=query_vector, top_k=10, ef=128)
    deleted = 0
    for item in results:
        if item.get("similarity", 0) >= threshold:
            index.delete_vector(item["id"])
            deleted += 1
    return deleted