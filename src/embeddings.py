from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
DIMENSION = 384

_model = None 

"""
'_model' and '_get_model' are internal implementation. Don't use it directly.

"""

def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def generate_embeddings(text: str) -> list:
    model = _get_model()
    embedding = model.encode(text, normalize_embeddings = True) # normalize_embeddings = True: makes all vectors the same scale
    return embedding.tolist()