import json
from typing import List
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CrawlResult, JsonCssExtractionStrategy
from schema_utils import load_or_generate_schema
from config import BASE_DIR

async def extract_alibaba_products():
    sample_html = """<div class="traffic-card-gallery" data-product_id="1601326906180" ...>
  <a href="https://www.alibaba.com/product-detail/OLED-13-3-Inch-Portable-Monitor_1601326906180.html" class="product-image ..." ...>
    <div class="il-relative" role="region" aria-roledescription="carousel">
      <div class="il-overflow-hidden">
        <div class="il-flex" style="transform: translate3d(0px, 0px, 0px);">
          <div role="group" aria-roledescription="slide" class="...">
            <img fetchpriority="high" src="//s.alicdn.com/@sc04/kf/H0b4322c62b2047349751a34a8e27796fI.jpg_300x300.jpg" loading="eager">
        </div>
      </div>
  </a>

  <div class="il-flex il-flex-1 il-flex-col il-justify-start">
    <a class="product-title ...">
      <h2 style="display: inline;">
        21-inch HD Slim Touch Tablet PC 64G/512G SSD 2.48GHz Windows 7/8/10 Industrial Tablet PC
      </h2>
    </a>
    <div class="il-mb-[0.125rem] il-text-xl il-font-bold il-flex il-items-start" data-component="ProductPrice">
        $281.00-291.00
    </div>
    <div class="il-text-sm il-text-secondary-foreground" data-component="ProductMoq">
        Min. Order: 1 set
    </div>
    ...
  </div>
</div>"""  # Use your full HTML snippet
    query = (
        "From https://www.alibaba.com/showroom/laptop.html, extract product image URL, title, URL, price, and MOQ."
    )
    schema = load_or_generate_schema(sample_html, query)

    extraction_strategy = JsonCssExtractionStrategy(schema)
    config = CrawlerRunConfig(extraction_strategy=extraction_strategy)

    urls = []
    for i in range(1, 17):
      urls.append(f"https://www.alibaba.com/showroom/laptop_{i}.html" )

    async with AsyncWebCrawler() as crawler:
        
      all_data = []
      for i,url in enumerate(urls):
        print(f"Processing URL:{i}:{url}")
        results: List[CrawlResult] = await crawler.arun(url, config=config)

        for result in results:
            # print(f"URL: {result.url} - Success: {result.success}")
            if result.success:
                data = json.loads(result.extracted_content)
                for item in data:
                    item['Source_URL']= url
                    item["page_number"] = i+1
                    image_url = item.get("image") or item.get("image_url") or item.get("product_image")
                    if image_url:
                        if not image_url.startswith(("http:", "https:")):
                            item["image_url"] = "https:" + image_url
                        else:
                            item["image_url"] = image_url

                    else:
                        item["image_url"] = None  # or some default value if needed
                all_data.extend(data)

                output_path = BASE_DIR / "tmp" / "extracted_data_details.json"
                with open(output_path, "w") as f:
                    json.dump(all_data, f, indent=2)
                print(json.dumps(all_data, indent=2))