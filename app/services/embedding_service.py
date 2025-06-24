# from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from langchain_openai import AzureOpenAIEmbeddings
import numpy as np
from sklearn.neighbors import NearestNeighbors
from ..utils.chunker import get_text_chunks
from ..configs.settings import settings

# In-memory storage
chunk_texts = []
chunk_embeddings = []

# Initialize embedding model once
embed_model = AzureOpenAIEmbeddings(         # your Azure deployment name
    model="sangria_embedding_3_small",                            # valid model name
    api_key=settings.AZURE_OPENAI_API_KEY,
    azure_endpoint=settings.AZURE_OPENAI_API_BASE
)

def embed_and_store(text: str) -> str:
    chunks = get_text_chunks(text)

    for chunk in chunks:
        embedding = embed_model.embed_query(chunk)  # returns a list[float]
        chunk_texts.append(chunk)
        chunk_embeddings.append(np.array(embedding))  # ensure numpy array

    return f"Stored {len(chunks)} chunks in memory."


def search_similar(query: str, top_k=3):
    if not chunk_embeddings:
        return ["No embeddings stored yet."]

    query_embedding = np.array(embed_model.embed_query(query))

    knn = NearestNeighbors(n_neighbors=min(top_k, len(chunk_embeddings)), metric='cosine')
    knn.fit(chunk_embeddings)
    distances, indices = knn.kneighbors([query_embedding])

    return [chunk_texts[i] for i in indices[0]]

