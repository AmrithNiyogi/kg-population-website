from .controllers.pipeline_controller import router as web_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

env_file = os.getenv("ENV_FILE", ".env")  
load_dotenv(env_file)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app.include_router(web_router, prefix="/web", tags=["Web-Ingestion-APIs"])


# if __name__ == "__main__":
#     # Replace this with any URL you want to process
#     test_url = "https://en.wikipedia.org/wiki/Artificial_intelligence"

#     print("\n[🔁] Starting Web KG Pipeline...")
#     run_pipeline(test_url)
#     print("[✅] Pipeline completed.\n")







