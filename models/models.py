from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Bank(Base):
    __tablename__ = "banks"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    bank_id = Column(Integer, ForeignKey("banks.id"))
    review_text = Column(String(1000))
    rating = Column(Float)
    date = Column(Date)
    sentiment = Column(String(10))
    theme = Column(String(50))