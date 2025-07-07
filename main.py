# main.py

from automation.login import login
from automation.scraper import scrape_quotes
from database.db_handler import init_db, insert_quotes

def main():
    print("🟢 main.py starting...")

    # Step 1: Initialize the database and create table if needed
    init_db()

    # Step 2: Login to the website using Playwright automation
    try:
        print("🚀 Launching browser and logging in...")
        playwright, browser, page = login()
    except Exception as e:
        print(f"❌ Error during login: {e}")
        return

    # Step 3: Confirm login success by printing page title
    try:
        title = page.title()
        print(f"📄 Page Title After Login: {title}")
    except Exception as e:
        print(f"⚠️ Could not get page title: {e}")

    # Step 4: Scrape quotes from the page
    try:
        print("🔍 Scraping quotes...")
        quotes = scrape_quotes(page)
        print(f"✅ Scraped {len(quotes)} quotes.")
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        quotes = []

    # Step 5: Insert scraped quotes into the SQLite database
    try:
        insert_quotes(quotes)
        print(f"✅ {len(quotes)} quotes saved to database.")
    except Exception as e:
        print(f"❌ Error inserting quotes into database: {e}")

    # Step 6: Pause to keep the browser open for inspection
    input("⏸️ Press Enter to close browser and exit...")

    # Step 7: Cleanup resources - close browser and stop playwright
    try:
        browser.close()
        playwright.stop()
        print("👋 Browser closed and Playwright stopped.")
    except Exception as e:
        print(f"⚠️ Error during cleanup: {e}")

if __name__ == "__main__":
    main()
