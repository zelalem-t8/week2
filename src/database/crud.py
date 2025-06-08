from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Bank, Review, Base
import pandas as pd
from config.oracle_config import CONNECTION_STRING

engine = create_engine(CONNECTION_STRING)
Session = sessionmaker(bind=engine)

def insert_reviews(df):
    session = Session()
    try:
        for _, row in df.iterrows():
            bank = session.query(Bank).filter_by(name=row["bank"]).first()
            if not bank:
                bank = Bank(name=row["bank"])
                session.add(bank)
                session.commit()
            
            review = Review(
                bank_id=bank.id,
                review_text=row["review"],
                rating=row["rating"],
                date=row["date"],
                sentiment=row["sentiment"],
                theme=row["theme"]
            )
            session.add(review)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()