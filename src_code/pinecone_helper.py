import os

from dotenv import load_dotenv

load_dotenv()

from src_code.env import load_project_env

load_project_env()

from pinecone import Pinecone, ServerlessSpec

from src_code.embedding_helper import embedder

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "medical-rag")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY environment variable is not set.")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

def write_to_pinecone(vectors, index = index):
    
    batch_size = 20

    for i in range(0, len(vectors), batch_size):
        index.upsert(vectors=vectors[i:i + batch_size])

    print("All documnent uploaded to pinecone")
    
    return True
    
def retrival_from_pinecone(query, index = index):
    
    query_embedding = embedder(query)
    
    result = index.query(vector=query_embedding, top_k=5, include_metadata = True)
        # result = [i for i in result.matches[i].metadata]
    metadata_list = []

    for match in result.matches:
        metadata_list.append(match.metadata)
    return metadata_list

# pc.create_index(
#     name="medical-rag",
#     dimension=384,
#     metric="cosine",
#     spec=ServerlessSpec(
#         cloud="aws",
#         region="us-east-1"
#     )
# )





