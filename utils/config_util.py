import random
from crawl4ai import BrowserConfig, CrawlerRunConfig
from utils.js_util import JS_CODE

PROXY_POOL = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
]

BROWSER_CONFIG = BrowserConfig(
    user_agent=random.choice(USER_AGENTS),
    viewport_width=1920,
    viewport_height=1080,
    # proxy=random.choice(PROXY_POOL)
)

CRAWLER_CONFIG = CrawlerRunConfig(
        js_code=JS_CODE,  # Apply our JavaScript for dynamic content handling
        cache_mode="force_cache",  # Cache responses to speed up development and reduce server load
        page_timeout=90000,  # 90 seconds timeout to allow all JavaScript to execute fully
    )
    