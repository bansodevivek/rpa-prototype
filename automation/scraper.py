import pandas as pd

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

    # # Export to CSV
    # df = pd.DataFrame(quotes_data)
    # df.to_csv("quotes.csv", index=False)
    # print("📁 Saved to quotes.csv")

    return quotes_data
