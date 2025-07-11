import pandas as pd
from pathlib import Path
def scrape_quotes(page):
    print("🔍 Scraping quotes...")

    quotes_data = []

    # Navigate to the quotes page
    page.goto("https://quotes.toscrape.com")

    # Select all quote blocks
    quote_blocks = page.query_selector_all(".quote")

    for quote in quote_blocks:
        text = quote.query_selector(".text").inner_text()
        author = quote.query_selector(".author").inner_text()
        tags = [tag.inner_text() for tag in quote.query_selector_all(".tag")]
        tags_str = ", ".join(tags)
        
        quotes_data.append((text, author, tags_str))

    print(f"✅ Scraped {len(quotes_data)} quotes.")

  # Save to CSV in output folder relative to this script
    output_dir = Path(r"C:\Users\ASUS\Prototype\rpa-prototype\output")
    output_dir.mkdir(exist_ok=True)  # Create folder if not exists
    csv_path = output_dir / "quotes.csv"

    df = pd.DataFrame(quotes_data, columns=["Text", "Author", "Tags"])
    df.to_csv(csv_path, index=False)
    print(f"📁 Saved to {csv_path}")

    return quotes_data
