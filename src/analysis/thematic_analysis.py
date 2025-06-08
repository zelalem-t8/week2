from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from config.settings import BANK_APPS

def extract_keywords(df, bank_name, top_n=10):
    bank_reviews = df[df["bank"] == bank_name]["cleaned_review"].dropna().astype(str)
    if len(bank_reviews) == 0:
        return []
    
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    tfidf = vectorizer.fit_transform(bank_reviews)
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf.sum(axis=0).A1
    top_indices = scores.argsort()[-top_n:][::-1]
    return [feature_names[i] for i in top_indices]

THEMES = {
    "login issues": ["login", "log in", "sign in", "authentication", "password"],
    "transactions": ["transfer", "transaction", "payment", "send money", "withdraw"],
    "ui/ux": ["interface", "ui", "ux", "design", "user experience", "easy to use"],
    "customer service": ["support", "service", "help", "assistance", "response"],
    "performance": ["slow", "fast", "lag", "crash", "freeze", "responsive"]
}

def assign_theme(text):
    if pd.isna(text):
        return "other"
    text = str(text).lower()
    for theme, keywords in THEMES.items():
        if any(keyword in text for keyword in keywords):
            return theme
    return "other"

def plot_thematic_analysis(df):
    # Create figure with dynamic subplot layout
    num_banks = len(df['bank'].unique())
    rows = (num_banks + 1) // 2  # +1 to round up
    fig, axes = plt.subplots(rows, 2, figsize=(15, 5*rows))
    axes = axes.flatten()
    
    # Overall theme distribution
    theme_counts = df['theme'].value_counts()
    axes[0].bar(theme_counts.index, theme_counts.values, color=sns.color_palette("husl"))
    axes[0].set_title('Overall Theme Distribution')
    axes[0].tick_params(axis='x', rotation=45)
    
    # Bank-wise theme distribution
    for i, bank in enumerate(df['bank'].unique(), start=1):
        bank_data = df[df['bank'] == bank]
        theme_dist = bank_data['theme'].value_counts()
        axes[i].pie(theme_dist, labels=theme_dist.index, autopct='%1.1f%%',
                   colors=sns.color_palette("pastel"))
        axes[i].set_title(f'{bank} Theme Distribution')
    
    # Hide unused subplots
    for j in range(i+1, len(axes)):
        axes[j].axis('off')
    
    plt.tight_layout()
    plt.savefig('theme_analysis_plots.png')
    plt.show()

def plot_keyword_analysis(df):
    num_banks = len(df['bank'].unique())
    fig, axes = plt.subplots((num_banks + 1)//2, 2, figsize=(15, 4*num_banks))
    axes = axes.flatten()
    
    for i, bank in enumerate(df['bank'].unique()):
        keywords = extract_keywords(df, bank)
        sns.barplot(ax=axes[i], x=list(range(len(keywords))), y=keywords, palette="viridis")
        axes[i].set_title(f'Top Keywords: {bank}')
        axes[i].set_yticks(range(len(keywords)))
        axes[i].set_yticklabels(keywords)
        axes[i].set_xlabel('TF-IDF Score Rank')
    
    for j in range(i+1, len(axes)):
        axes[j].axis('off')
    
    plt.tight_layout()
    plt.savefig('results/keyword_analysis_plots.png')
    plt.show()

if __name__ == "__main__":
    try:
        df = pd.read_csv("data/processed/cleaned_reviews.csv")
        df["cleaned_review"] = df["cleaned_review"].fillna("").astype(str)
        
        # Keyword extraction
        for bank_name in BANK_APPS.keys():
            keywords = extract_keywords(df, bank_name)
            print(f"Top keywords for {bank_name}: {keywords}")
        
        # Theme assignment
        df["theme"] = df["cleaned_review"].apply(assign_theme)
        
        # Visualization
        plot_thematic_analysis(df)
        plot_keyword_analysis(df)
        
        # Save results
        df.to_csv("data/processed/thematic_analysis_results.csv", index=False)
        print("Thematic analysis completed successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")