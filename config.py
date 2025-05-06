import os
from pathlib import Path
from dotenv import load_dotenv
from crawl4ai import CrawlerRunConfig, BrowserConfig
import random

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

