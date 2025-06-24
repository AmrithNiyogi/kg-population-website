from neo4j import GraphDatabase
from ..models.triples_model import Triple
from ..configs.settings import settings


driver = GraphDatabase.driver(settings.NEO4J_URL, auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD))
print("[Neo4j] Connected:", driver.verify_connectivity())


def store_triples_in_neo4j(triples: list[Triple], source_url: str):
    with driver.session() as session:
        for triple in triples:
            session.write_transaction(_create_triple, triple, source_url)


def _create_triple(tx, triple: Triple, url: str):
    relation = _sanitize_label(triple.predicate)
    url_label = _sanitize_label(url)

    print(f"[Neo4j] Creating triple: ({triple.subject})-[{relation}]->({triple.object}), URL: {url}")

    query = f"""
    MERGE (s:Entity:{url_label} {{name: $subject}})
      ON CREATE SET s.source_url = $url
    MERGE (o:Entity:{url_label} {{name: $object}})
      ON CREATE SET o.source_url = $url
    MERGE (s)-[r:{relation}]->(o)
    """

    tx.run(query, subject=triple.subject, object=triple.object, url=url)


def _sanitize_label(label: str) -> str:
    # Converts URL to a safe label: https://example.com → HTTPS_EXAMPLE_COM
    return ''.join(e.upper() if e.isalnum() else '_' for e in label)
