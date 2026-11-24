from functools import lru_cache

from src_code.utils import create_search_text


@lru_cache(maxsize=1)
def _load_model(model_name):
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(model_name)


def embedder(query, model_name = "all-MiniLM-L6-v2"):
    model = _load_model(model_name)
    embedding = model.encode(query).tolist()
    return embedding
    
    
def embed_helper(data):

    vectors = []

    for doc in data:

        doc_id = str(doc["_id"])
        search_text = create_search_text(doc)
        embedding = embedder(search_text)
        metadata = {
            "text": search_text,
            "patient_name":doc.get("patient_name", ""),
            "hospital":doc.get("hospital", "")
        }

        vectors.append(
            (
                doc_id,
                embedding,
                metadata
            )
        )
    
    
    return vectors



