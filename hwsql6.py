import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models_hwsql6 import create_tables, Publisher, Shop, Book, Stock, Sale

DSN = "postgresql://postgres:alciona@localhost:5432/HWSQL6"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

q = session.query(Publisher).filter(Publisher.name == input("Введите название издателя: "))
for s in q.all():
    print(s.id, s.name)

q = session.query(Publisher).filter(Publisher.id == input("Введите идентификатор (id) издателя: "))
for s in q.all():
    print(s.id, s.name)

subq = session.query(Shop).all()
for s in subq:
    print(s.id, s.name)


subq = session.query(Stock).join(Shop).subquery()
for b in session.query(Publisher).join(Book).filter(Book.id == subq.c.id_book).all():
    print(f"\t {b.id}   {b.name}")