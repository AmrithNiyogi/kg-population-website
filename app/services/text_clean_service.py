import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download("punkt")
nltk.download("stopwords")


stop_words = set(stopwords.words("english"))

def clean_text(text: str) -> str:
    text = text.lower()

    tokens = word_tokenize(text)

    cleaned_tokens = [
        word for word in tokens
        if word not in stop_words and word not in string.punctuation
    ]

    return " ".join(cleaned_tokens)
