from bs4 import BeautifulSoup

def extract_text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for element in soup(["script", "style", "noscript", "iframe"]):
        element.extract()

    text = soup.get_text(separator=" ")
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    cleaned = " ".join(chunk for chunk in chunks if chunk)

    return cleaned
