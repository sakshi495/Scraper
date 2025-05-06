import asyncio
from extractor import extract_alibaba_products
from key_attributes import main as extract_detailed_attributes

async def main():
    print("\n=== Starting Extraction Process ===")
    
    # Run both functions concurrently
    await asyncio.gather(
        extract_alibaba_products(),
        extract_detailed_attributes()
    )
    
    print("\n=== Completed ===")

if __name__ == "__main__":
    asyncio.run(main())



