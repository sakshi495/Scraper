import os
import json
from crawl4ai import JsonCssExtractionStrategy, LLMConfig
from config import BASE_DIR, GROQ_API_KEY

os.makedirs(f"{BASE_DIR}/tmp", exist_ok=True)

SCHEMA_FILE = BASE_DIR / "tmp" / "schema.json"

def load_or_generate_schema(sample_html: str, query: str) -> dict:
    if SCHEMA_FILE.exists():
        with open(SCHEMA_FILE, "r") as f:
            return json.load(f)
    
    schema = JsonCssExtractionStrategy.generate_schema(
        html=sample_html,
        llm_config=LLMConfig(provider="groq/llama3-8b-8192", api_token=GROQ_API_KEY),
        query=query,
    )
    
    SCHEMA_FILE.parent.mkdir(exist_ok=True)
    with open(SCHEMA_FILE, "w") as f:
        json.dump(schema, f, indent=2)
    
    return schema
