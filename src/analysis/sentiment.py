from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(df):
    def get_sentiment(text):
        if isinstance(text, float):  # Handle NaN/float values
            return "neutral"
        score = analyzer.polarity_scores(str(text))["compound"]  # Ensure text is string
        return "positive" if score > 0.05 else "negative" if score < -0.05 else "neutral"
    
    df["sentiment"] = df["cleaned_review"].apply(get_sentiment)
    return df

if __name__ == "__main__":
    # Load and test with sample data
    df = pd.read_csv("data/processed/cleaned_reviews.csv")
    df = analyze_sentiment(df)
    df.to_csv("data/processed/analyzed_reviews.csv", index=False)
    print("Sentiment analysis completed!")