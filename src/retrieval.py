import time
from src.memory_store import search_memory

SIMILARITY_THRESHOLD = 0.45
RECENCY_WEIGHT = 0.15

def retrieve_context(index, query: str, top_k: int = 5) -> str:
    memories = search_memory(index, query, top_k = top_k)

    # filter by similarity threshold
    filtered = [m for m in memories if m["similarity"] >= SIMILARITY_THRESHOLD]

    if not memories:
        return ""

    # applying recency weighting
    now = time.time()
    for m in filtered:
        hours_since = (now - m.get("timestamp", now)) / 3600
        recency_factor = 1 / (1 + hours_since)
        m["final_score"] = m["similarity"] + (RECENCY_WEIGHT * recency_factor)

    # sort by final score
    filtered.sort(key=lambda m: m["final_score"], reverse=True)
    lines = []
    for mem in memories:
        role_label = "User" if mem["role"] == "user" else "Assistant"
        lines.append(f"[{role_label}]: {mem['text']}")

    return "\n".join(lines)

def build_prompt(context: str, query: str) -> str:
    if context:
        return (
            f"Relevant past memories:\n{context}\n\n"
            f"Current message:\n{query}\n\n"
            "Answer while considering the past context above.")
    else:
        return f"User message:\n{query}\n\nAnswer helpfully."