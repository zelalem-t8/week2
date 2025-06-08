import pandas as pd
import re

def preprocess_reviews(df):
    # Remove duplicates
    df = df.drop_duplicates(subset=["review", "bank"])
    
    # Handle missing data
    df = df.dropna(subset=["review"])
    df["rating"] = df["rating"].fillna(0)
    
    # Clean text: remove special chars, lowercase
    df["cleaned_review"] = df["review"].apply(
        lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x.lower())
    )
    return df

# Example usage after scraping:
df = pd.read_csv("data/raw/all_reviews.csv")
cleaned_df = preprocess_reviews(df)
cleaned_df.to_csv("data/processed/cleaned_reviews.csv", index=False)