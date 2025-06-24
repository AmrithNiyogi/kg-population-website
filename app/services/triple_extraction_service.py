from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from ..models.triples_model import Triple
from ..configs.settings import settings
from langfuse import Langfuse
import json

llm = AzureChatOpenAI(
    azure_deployment=settings.AZURE_DEPLOYMENT_NAME,
    api_version="2025-01-01-preview",
    temperature=0.7,
    azure_endpoint=settings.AZURE_OPENAI_API_BASE,
    api_key=settings.AZURE_OPENAI_API_KEY,
)

def extract_triples_from_text(text: str) -> list[Triple]:
    langfuse = Langfuse(
        host=settings.LANGFUSE_HOST,
        secret_key=settings.LANGFUSE_SECRET_KEY,
        public_key=settings.LANGFUSE_PUBLIC_KEY
    )

    result = langfuse.get_prompt("PDFIngestionPrompt")

    prompt = result.compile(text=text)

    response = llm.invoke(prompt)

    try:
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:].strip("` \n")  # remove markdown code fencing
        triples = json.loads(content)
        return [Triple(**t) for t in triples]  # ✅ Ensure correct type
    except Exception as e:
        print("[extract_triples] Error parsing triples:", e)
        print("[extract_triples] Raw response:", response.content)
        return []

