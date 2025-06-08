from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from config.settings import BANK_APPS, REVIEWS_PER_BANK, LANG, COUNTRY
def extract_keywords(df, bank_name, top_n=10):
    bank_reviews = df[df["bank"] == bank_name]["cleaned_review"]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    tfidf = vectorizer.fit_transform(bank_reviews)
    feature_names = vectorizer.get_feature_names_out()
    
    # Sum TF-IDF scores per term
    scores = tfidf.sum(axis=0).A1
    top_indices = scores.argsort()[-top_n:][::-1]
    
    return [feature_names[i] for i in top_indices]

# Manual theme mapping (example for CBE)
THEMES = {
    "login issues": ["login error", "cant log in"],
    "transactions": ["transfer failed", "slow transaction"],
    "ui": ["user interface", "easy to use"]
}

def assign_theme(text):
    for theme, keywords in THEMES.items():
        if any(keyword in text for keyword in keywords):
            return theme
    return "other"
if __name__ == "__main__":
    # Load cleaned reviews
    df = pd.read_csv("data/processed/cleaned_reviews.csv")
    # Extract keywords for each bank
    for bank_name in BANK_APPS.keys():
        keywords = extract_keywords(df, bank_name)
        print(f"Top keywords for {bank_name}: {keywords}")
    # Assign themes to reviews
    df["theme"] = df["cleaned_review"].apply(assign_theme)