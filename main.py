import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True, nullable=False)

    books = relationship("Book", back_populates = "publisher")

    def __str__(self):
        return f'{self.name}'

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=255), unique=True, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship("Publisher", back_populates ="books")
    stocks = relationship("Stock", back_populates = "book")

    def __str__(self):
        return f'{self.title}'

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True, nullable=False)

    stocks = relationship("Stock", back_populates = "shop")

    def __str__(self):
        return f'{self.name}'

class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.SmallInteger, nullable=False)

    book = relationship("Book", back_populates = "stocks")
    shop = relationship("Shop", back_populates = "stocks")
    sales = relationship("Sale", back_populates = "stock")

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric(10, 2), nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.SmallInteger, nullable=False)

    stock = relationship("Stock", back_populates = "sales")


    def __str__(self):
        return f'{self.price} | {self.date_sale}'


type_db = "postgresql"
login = "postgres"
password = "postgres"
host = "localhost:5432"
name_db = "bookstore"

DSN = f'{type_db}://{login}:{password}@{host}/{name_db}'
engine = sqlalchemy.create_engine(DSN)

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()
pub_1 = Publisher(name = "Пушкин Александр Сергеевич")
pub_2 = Publisher(name = "Достоевский Федор Михайлович")
pub_3 = Publisher(name = "Гоголь Николай Ваильевич")
session.add_all([pub_1, pub_2, pub_3])
session.commit()

book_1 = Book(title = "Евгений Онегин", id_publisher = '1')
book_2 = Book(title = "Капитанская дочка", id_publisher = '1')
book_3 = Book(title = "Преступление и наказание", id_publisher = '2')
book_4 = Book(title = "Бесы", id_publisher = '2')
book_5 = Book(title = "Вечера на хуторе близ Диканьки", id_publisher = '3')
book_6 = Book(title = "Мёртвые души", id_publisher = '3')
session.add_all([book_1, book_2, book_3, book_4, book_5, book_6])
session.commit()

shop_1 = Shop(name = "КнигаЛэнд")
shop_2 = Shop(name = "Букинг")
shop_3 = Shop(name = "ЧитайГород")
session.add_all([shop_1, shop_2, shop_3])
session.commit()

st_1 = Stock(id_book = "1", id_shop = "1", count = "5")
st_2 = Stock(id_book = "3", id_shop = "1", count = "2")
st_3 = Stock(id_book = "5", id_shop = "1", count = "1")
st_4 = Stock(id_book = "2", id_shop = "2", count = "4")
st_5 = Stock(id_book = "6", id_shop = "2", count = "7")
st_6 = Stock(id_book = "4", id_shop = "2", count = "3")
st_7 = Stock(id_book = "1", id_shop = "3", count = "5")
st_8 = Stock(id_book = "4", id_shop = "3", count = "2")
st_9 = Stock(id_book = "2", id_shop = "3", count = "9")
session.add_all([st_1, st_2, st_3, st_4, st_5, st_6, st_7, st_8, st_9])
session.commit()

sale_1 = Sale(price = "280.00", date_sale = "12.01.2025", id_stock = "1", count = "1")
sale_2 = Sale(price = "350.00", date_sale = "15.01.2025", id_stock = "1", count = "2")
sale_3 = Sale(price = "220.00", date_sale = "16.01.2025", id_stock = "2", count = "1")
sale_4 = Sale(price = "630.00", date_sale = "17.01.2025", id_stock = "3", count = "1")
sale_5 = Sale(price = "450.00", date_sale = "18.01.2025", id_stock = "4", count = "3")
sale_6 = Sale(price = "530.00", date_sale = "25.01.2025", id_stock = "1", count = "2")
sale_7 = Sale(price = "190.00", date_sale = "30.01.2025", id_stock = "7", count = "1")
sale_8 = Sale(price = "415.00", date_sale = "05.02.2025", id_stock = "8", count = "1")
sale_9 = Sale(price = "190.00", date_sale = "10.02.2025", id_stock = "7", count = "1")
session.add_all([sale_1, sale_2, sale_3, sale_4, sale_5, sale_6, sale_7, sale_8, sale_9])
session.commit()
session.close()

def get_shops(filter_string):
    session = Session()
    query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale
    ).join(Publisher, Book.id_publisher == Publisher.id)\
    .join(Stock, Book.id == Stock.id_book)\
    .join(Shop, Shop.id == Stock.id_shop)\
    .join(Sale, Sale.id_stock == Stock.id)
    if filter_string.isdigit():
        sub_query = query.filter(Publisher.id == filter_string).all()
    else:
        sub_query = query.filter(Publisher.name == filter_string).all()
    for Title, Shop_name, Price, Date_sale in sub_query:
        print(f"{Title: <30} | {Shop_name: <10} | {Price: <8} | {Date_sale.strftime('%d-%m-%Y')}")
    session.close()

if __name__ == "__main__":
    get_shops('Гоголь Николай Ваильевич')
    get_shops('2')
