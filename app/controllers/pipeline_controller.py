from ..services.scrapy_service import scrape_url
from ..services.bs4_service import extract_text_from_html
from ..services.text_clean_service import clean_text
from ..services.mongo_service import store_in_mongodb
from ..services.triple_extraction_service import extract_triples_from_text
from ..services.neo4j_service import store_triples_in_neo4j
from ..services.embedding_service import embed_and_store
from ..models.document_model import Document
from fastapi import APIRouter
from ..utils.logging_utils import setup_logger

router = APIRouter()

logger = setup_logger(__name__)

router = APIRouter()
logger = setup_logger(__name__)

@router.post("/execute-pipeline")
def run_pipeline(url: str):
    print(f"[+] Running KG Pipeline for: {url}")

    # Step 1: Scrape HTML
    html = scrape_url(url)
    if not html:
        print("[-] Failed to fetch HTML content.")
        return {"error": "Failed to scrape URL."}

    # Step 2: Extract raw text
    raw_text = extract_text_from_html(html)
    
    # Step 3: Clean text
    clean = clean_text(raw_text)

    # Step 4: Embed & store in FAISS (or memory)
    # vector_id = embed_and_store(clean)  # <- Updated function
    vector_id = None

    # Step 5: Store document in MongoDB
    document = Document(
        url=url,
        raw_text=raw_text,
        clean_text=clean,
        vector_id=None  # May just be a string like "webkg_index.faiss"
    )
    store_in_mongodb(document)

    # Step 6: Extract triples
    triples = extract_triples_from_text(clean)

    # Step 7: Store triples in Neo4j
    store_triples_in_neo4j(triples, url)

    # Step 8: Done
    print(f"[✓] Pipeline complete for: {url}")
    return {"status": "Pipeline executed successfully", "url": url}
