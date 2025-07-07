import os
from celery import Celery
from dotenv import load_dotenv
from automation.scraper import scrape_quotes

load_dotenv()
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("rpa_prototype", broker=redis_url)

@celery_app.task
def scrape_quotes_task():
    print("Starting scraping task...")
    scrape_quotes()
    print("Scraping completed and saved to scraped_quotes.csv")
    return "Success"
