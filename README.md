"# week2" 
# Ethiopian Bank Reviews Analysis

This project collects, processes, analyzes, and visualizes customer reviews of Ethiopian banks from the Google Play Store. It uses Python for data handling, sentiment/thematic analysis, and database storage, and provides Jupyter notebooks for visualization.

---

## Project Structure

```
week2/
├── config/
│   ├── oracle_config.py
│   └── settings.py
├── data/
│   ├── raw/
│   └── processed/
├── models/
│   └── models.py
├── notebooks/
│   └── analysis.ipynb
├── src/
│   ├── analysis/
│   │   ├── sentiment.py
│   │   └── thematic_analysis.py
│   ├── database/
│   │   └── crud.py
│   ├── scrapping/
│   │   ├── scrapper.py
│   │   └── utils.py
├── requirements.txt
└── README.md
```

---

## Setup Instructions

1. **Clone the repository**
   ```sh
   git clone <repo-url>
   cd "c:\Users\hp\Desktop\10 academy\week2"
   ```

2. **Create and activate a virtual environment**
   ```sh
   python -m venv my-env
   my-env\Scripts\activate
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure the database**
   - Edit `config/oracle_config.py` and set your Oracle `CONNECTION_STRING`.

---

## Data Pipeline

1. **Scraping Reviews**
   - Use `src/scrapping/scrapper.py` to scrape reviews from the Google Play Store.
   - Output: `data/raw/all_reviews.csv`

2. **Preprocessing**
   - Clean and preprocess reviews with `src/scrapping/utils.py`.
   - Output: `data/processed/cleaned_reviews.csv`

3. **Sentiment Analysis**
   - Analyze sentiment using `src/analysis/sentiment.py`.
   - Output: `data/processed/analyzed_reviews.csv`

4. **Thematic Analysis**
   - Extract themes using `src/analysis/thematic_analysis.py`.

5. **Database Insertion**
   - Insert processed reviews into the database using `src/database/crud.py`:
     ```python
     import pandas as pd
     from src.database.crud import insert_reviews

     df = pd.read_csv("data/processed/analyzed_reviews.csv")
     insert_reviews(df)
     ```

---

## Visualization

Open `notebooks/analysis.ipynb` in Jupyter or VS Code to explore:

- **Overall Rating Distribution**: Pie chart of all review ratings.
- **Overall Sentiment Distribution**: Pie chart of all review sentiments.
- **Bank-wise Sentiment Breakdown**: Pie charts for each bank’s sentiment distribution.

Example code from the notebook:
```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('../data/processed/analyzed_reviews.csv')
plt.figure(figsize=(15, 12))

# Overall Rating Distribution
plt.subplot(2, 3, 1)
rating_counts = df['rating'].value_counts()
plt.pie(rating_counts, labels=rating_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
plt.title('Overall Rating Distribution', fontsize=14)

# Overall Sentiment Distribution
plt.subplot(2, 3, 2)
sentiment_counts = df['sentiment'].value_counts()
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=['#66b3ff','#ff9999','#99ff99'], explode=(0.05, 0.05, 0.05))
plt.title('Overall Sentiment Distribution', fontsize=14)

# Bank-wise Sentiment Breakdown
for i, bank in enumerate(df['bank'].unique(), 3):
    plt.subplot(2, 3, i+1)
    bank_data = df[df['bank'] == bank]
    counts = bank_data['sentiment'].value_counts()
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'], shadow=True)
    plt.title(f'{bank} Sentiment', fontsize=12)

plt.tight_layout()
plt.show()
```

---

## Database Models

Defined in `models/models.py`:

- **Bank**
  - `id`: Primary key
  - `name`: Name of the bank

- **Review**
  - `id`: Primary key
  - `bank_id`: Foreign key to Bank
  - `review_text`: The review content
  - `rating`: User rating
  - `date`: Date of review
  - `sentiment`: Sentiment label
  - `theme`: Thematic label

---

## Requirements

- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- SQLAlchemy
- cx_Oracle
- scikit-learn
- vaderSentiment
- tqdm
- google_play_scraper

Install all dependencies with:
```sh
pip install -r requirements.txt
```

---

## License

MIT License

---

## Contact

For questions or contributions, please open an issue or submit a pull request.
