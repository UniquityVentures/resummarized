import torch
from typing import List
from sentence_transformers import SentenceTransformer

device = "cuda" if torch.cuda.is_available() else "cpu"


model_id = "google/embeddinggemma-300M"
model = None

def gen_embedding(sentence: str) -> List[float]:
    global model
    if model is None:
        model = SentenceTransformer(model_id, device=device)
    return model.encode(sentence, prompt_name="query")
