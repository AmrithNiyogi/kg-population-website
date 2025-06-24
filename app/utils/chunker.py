from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..configs.settings import settings


def get_text_chunks(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""]
    )
    return splitter.split_text(text)
