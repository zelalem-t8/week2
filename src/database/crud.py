import os
import pandas as pd
import oracledb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Bank, Review, Base

# Set this only if you run into NLS-related errors (prevention)
os.environ["NLS_LANG"] = "AMERICAN_AMERICA.AL32UTF8"

# ✅ DO NOT initialize Oracle Client if you want pure Python (thin mode)
# oracledb.init_oracle_client(lib_dir=None)  <-- remove this

# ✅ Use thin mode connection string
DATABASE_URL = "oracle+oracledb://system:YourPassword123@localhost:1521/?service_name=XEPDB1"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Create tables
Base.metadata.create_all(engine)

def insert_reviews(df: pd.DataFrame):
    session = Session()
    bank_cache = {}

    try:
        for _, row in df.iterrows():
            bank_name = row["bank"]

            if bank_name in bank_cache:
                bank = bank_cache[bank_name]
            else:
                bank = session.query(Bank).filter_by(name=bank_name).first()
                if not bank:
                    bank = Bank(name=bank_name)
                    session.add(bank)
                    session.flush()
                bank_cache[bank_name] = bank

            review = Review(
                bank_id=bank.id,
                review_text=str(row["review"]),
                rating=float(row["rating"]),
                date=pd.to_datetime(row["date"]).date() if pd.notnull(row["date"]) else None,
                sentiment=str(row["sentiment"]),
                theme=str(row["theme"]),
            )
            session.add(review)

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error inserting reviews: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    df = pd.read_csv("data/processed/thematic_analysis_results.csv")
    insert_reviews(df)
