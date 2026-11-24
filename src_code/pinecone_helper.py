from pinecone import Pinecone, ServerlessSpec
from src_code.embedding_helper import embedder

pc = Pinecone(api_key="pcsk_3MdazS_Kk11BxuZGRzbXSk1JgPD3rMpvxu1ahgiErBMHx8UXTPF8ZjKoZSxUGpyH6uDwCC")
index = pc.Index("medical-rag")

def write_to_pinecone(vectors, index = index):
    
    batch_size = 20

    for i in range(100, len(vectors), batch_size):
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





