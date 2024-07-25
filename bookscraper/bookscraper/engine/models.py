from bookscraper.engine import Base
from sqlalchemy import Column, String, Integer, Float, Text


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    url = Column(String(256))
    title = Column(String(256))
    category = Column(String(256))
    description = Column(Text)
    product_type = Column(String(256))
    price_excl_tax = Column(Float)
    price_incl_tax = Column(Float)
    tax = Column(Float)
    availability = Column(Integer)
    number_of_reviews = Column(Integer)
    stars = Column(Integer)
    price = Column(Float)
