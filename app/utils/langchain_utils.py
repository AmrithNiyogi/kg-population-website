# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.vectorstores import Redis
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from ..configs.settings import settings
from redis import Redis

def get_embedding_model():
    embedding_model = AzureOpenAIEmbedding(
        deployment_name=settings.AZURE_EMBEDDING_DEPLOYMENT_NAME,
        api_key=settings.AZURE_OPENAI_API_KEY,
        azure_endpoint=settings.AZURE_OPENAI_API_BASE,
        api_version="2025-01-01"
    )
    return embedding_model
def get_vector_store(index_name: str, texts: list[str], embedding_model=None):
    if embedding_model is None:
        embedding_model = get_embedding_model()

    return Redis.from_texts(
        texts=texts,
        embedding=embedding_model,
        redis_url=settings.REDIS_URL,
        index_name=index_name
    )