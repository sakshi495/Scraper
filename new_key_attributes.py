import asyncio
from pathlib import Path
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

from config import BASE_DIR
from utils.file_utils import load_urls_from_json, save_json
from utils.html_utils import extract_product_info, extract_attributes
from utils.js_snippets import JS_SCROLL_AND_EXPAND
from utils.config_constants import BROWSER_CONFIG

# Output directory
OUTPUT_DIR = BASE_DIR / "output_key_attributes"
OUTPUT_DIR.mkdir(exist_ok=True)

# Crawler configuration
CRAWLER_CONFIG = CrawlerRunConfig(
    js_code=JS_SCROLL_AND_EXPAND,
    cache_mode="force_cache",
    page_timeout=90000,
)

async def crawl_url(crawler, url: str) -> dict:
    try:
        result = await crawler.arun(url, config=CRAWLER_CONFIG)
        if not result.success or not result.html:
            return {url: {"error": "Failed or no HTML"}}

        soup = BeautifulSoup(result.html, "html.parser")
        if soup.select_one('punish-component') or 'captcha' in result.html.lower():
            return {url: {"error": "Captcha detected"}}

        product_info = extract_product_info(soup)
        attributes = extract_attributes(soup)
        product_id = url.split("_")[-1].split(".")[0]
        filename = f"alibaba_product_{product_id}.json"

        save_json({"url": url, "product_info": product_info, "attributes": attributes}, OUTPUT_DIR / filename)
        return {url: {"product_info": product_info, "attributes": attributes}}

    except Exception as e:
        return {url: {"error": str(e)}}

async def process_urls_concurrently(urls: list[str]):
    results = {}

    async with AsyncWebCrawler(config=BROWSER_CONFIG) as crawler:
        semaphore = asyncio.Semaphore(5)

        async def crawl_with_limit(url):
            async with semaphore:
                return await crawl_url(crawler, url)

        tasks = [crawl_with_limit(url) for url in urls]
        results_list = await asyncio.gather(*tasks)

        for result in results_list:
            results.update(result)

        save_json(results, OUTPUT_DIR / "combined_results_new.json")
        return results

async def main():
    file_path = BASE_DIR / "tmp" / "extracted_data_details.json"
    urls = load_urls_from_json(file_path)
    results = await process_urls_concurrently(urls)

    for url, data in results.items():
        product_id = url.split("_")[-1].split(".")[0]
        status = "Error" if "error" in data else f"{len(data.get('attributes', {}))} attributes"
        print(f"• {product_id}: {status}")
