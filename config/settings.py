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