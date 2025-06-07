from google_play_scraper import app, reviews, Sort
import pandas as pd
from tqdm import tqdm
import time
from config.settings import BANK_APPS, REVIEWS_PER_BANK, LANG, COUNTRY
class BankReviewScraper:
    def __init__(self):
        self.reviews_data = []

    def scrape_bank_reviews(self, app_id, bank_name):
        continuation_token = None
        progress_bar = tqdm(total=REVIEWS_PER_BANK, desc=f"Scraping {bank_name}")

        while len(self.reviews_data) < REVIEWS_PER_BANK:
            try:
                batch, continuation_token = reviews(
                    app_id,
                    lang=LANG,
                    country=COUNTRY,
                    sort=Sort.NEWEST,
                    count=100,  # Max per request
                    continuation_token=continuation_token
                )
                for review in batch:
                    self.reviews_data.append({
                        "bank": bank_name,
                        "review": review["content"],
                        "rating": review["score"],
                        "date": review["at"].strftime("%Y-%m-%d"),
                        "source": "Google Play"
                    })
                progress_bar.update(len(batch))
                if not continuation_token:
                    break
                time.sleep(2)  # Rate limiting
            except Exception as e:
                print(f"Error scraping {bank_name}: {e}")
                break

    def save_to_csv(self, filename):
        pd.DataFrame(self.reviews_data).to_csv(filename, index=False)

# Usage
if __name__ == "__main__":
    scraper = BankReviewScraper()
    for bank_name, app_id in BANK_APPS.items():
        scraper.scrape_bank_reviews(app_id, bank_name)
    scraper.save_to_csv("data/raw/all_reviews_dashen.csv")