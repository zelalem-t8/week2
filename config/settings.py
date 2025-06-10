from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# App IDs for Ethiopian banks
BANK_APPS = {
    # "cbe": "com.combanketh.mobilebanking",
    # "boa": "com.boa.boaMobileBanking",
    "dashen": "com.dashen.dashensuperapp"
}

# Scraping settings
REVIEWS_PER_BANK = 448
LANG = "en"  # Language for reviews
COUNTRY = "et"  # Ethiopia
# config.py

USERNAME = "system"
PASSWORD = "YourPassword123"
HOST = "localhost"
PORT = 1521
SERVICE_NAME = "XEPDB1"

CONNECTION_STRING = f"oracle+cx_oracle://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/?service_name={SERVICE_NAME}"
