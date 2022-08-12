import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publishers"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), unique=True)


class Shop(Base):
    __tablename__ = "shops"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), unique=True)


class Book(Base):
    __tablename__ = "books"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=100), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publishers.id"), nullable=False)
    publisher = relationship(Publisher, backref="books")


class Stock(Base):
    __tablename__ = "stoks"

    id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer, nullable=False, default=0)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("books.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shops.id"), nullable=False)

    book = relationship(Book, backref="stocks")
    shop = relationship(Shop, backref="stocks")


class Sale(Base):
    __tablename__ = "sales"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.DECIMAL, nullable=False)
    data_sale = sq.Column(sq.DATETIME, nullable=False)
    count = sq.Column(sq.Integer, nullable=False, default=1)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stocks.id"), nullable=False)

    stock = relationship(Stock, backref="sales")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
