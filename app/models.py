import enum
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from app import db
from sqlalchemy import Column,Integer,String,ForeignKey,Float,Boolean,Enum,DateTime
from datetime import datetime

class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2
    EMPLOYEE = 3

class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

class User(BaseModel, UserMixin):
    # id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name

class Category(BaseModel):
    __tablename__ = 'category'

    # id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    # id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    price = Column(Float, default=0)
    image = Column(String(100),
                   default='https://reviewmaydocsach.com/wp-content/uploads/2022/08/cai-dung-cua-thanh-nhan-nguyen-duy-can.jpg')
    quantity=Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)
    book_author = relationship('BookAuthor', backref='product', lazy=True)
    comments = relationship('Comment', backref='product', lazy=True)
    def __str__(self):
        return self.name

class Author(BaseModel):
    name = Column(String(50), nullable=True)
    biography = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    birthday = Column(DateTime, nullable=True)
    book_author = relationship('BookAuthor', backref='author', lazy=True)
    def __str__(self):
        return self.name

class BookAuthor(BaseModel):
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    author_id = Column(Integer, ForeignKey(Author.id), nullable=False)

class Receipt(BaseModel):
    status = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)

class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)


if __name__=='__main__':
    from app import app
    with app.app_context():
        db.create_all()

        c1 = Category(name='Sách tâm lý')
        c2 = Category(name='Sách giáo dục')
        c3 = Category(name='Sách tài chính')
        db.session.add(c1)
        db.session.add(c2)
        db.session.add(c3)
        db.session.commit()

        p1 = Product(name='Predictably Irrational', price=210000,quantity=10,category_id=1)
        p2 = Product(name='How Pschycology Works', price=250000,quantity=12, category_id=1)
        # # p3 = Product(name='Cái dũng của thánh nhân', auhor_name='Nguyễn Duy Cần',price=240000, category_id=2)
        # p4 = Product(name='Toán học cao cấp', auhor_name='Trần Trung Kiệt',price=290000, category_id=2)
        p5 = Product(name='Finance Wheel', price=25000,quantity=12, category_id=3)
        db.session.add_all([p1,p2,p5])
        db.session.commit()

        a1 = Author(name='Lionel Messi', biography='Football Player',country='Argentina')
        a2 = Author(name='Cristiano Ronaldo', biography='Football Player',country='Portugal')
        # # p3 = Product(name='Cái dũng của thánh nhân', auhor_name='Nguyễn Duy Cần',price=240000, category_id=2)
        # p4 = Product(name='Toán học cao cấp', auhor_name='Trần Trung Kiệt',price=290000, category_id=2)
        a5 = Author(name='Neymar Jr', biography='Football Player',country='Brazil')
        db.session.add_all([a1,a2,a5])
        db.session.commit()

        ba1=BookAuthor(product_id=1,author_id=1)
        ba2=BookAuthor(product_id=1,author_id=2)
        ba3=BookAuthor(product_id=2,author_id=2)
        ba4=BookAuthor(product_id=3,author_id=3)
        db.session.add_all([ba1,ba2,ba3,ba4])
        db.session.commit()
        import hashlib
        u = User(name='Admin', username='admin', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),user_role=UserRoleEnum.ADMIN)
        db.session.add(u)
        db.session.commit()
        import hashlib
        u = User(name='Thu', username='Employee', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),user_role=UserRoleEnum.EMPLOYEE)
        db.session.add(u)
        db.session.commit()
        import hashlib
        u = User(name='Nhi', username='user', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),user_role=UserRoleEnum.USER)
        db.session.add(u)
        db.session.commit()

        c1 = Comment(content='Good', user_id=1, product_id=1)
        c2 = Comment(content='Nice', user_id=1, product_id=1)
        db.session.add_all([c1, c2])
        db.session.commit()

        # r1=Receipt(created_date='2024-1-1',user_id=1,status=True)
        # r2=Receipt(created_date='2024-1-23',user_id=2,status=True)
        # r3=Receipt(created_date='2024-2-1',user_id=3,status=True)
        # r4=Receipt(created_date='2024-2-4',user_id=1,status=True)
        # r5=Receipt(created_date='2024-3-1',user_id=1,status=True)
        # r6=Receipt(created_date='2023-12-1',user_id=1,status=True)
        # db.session.add_all([r1,r2,r3,r4,r5,r6])
        # db.session.commit()

        # rd1=ReceiptDetails(product_id=1,receipt_id=1)
        # rd2=ReceiptDetails(product_id=2,receipt_id=1)
        # rd3=ReceiptDetails(product_id=3,receipt_id=1)
        # rd4=ReceiptDetails(product_id=3,receipt_id=1)
        # rd5=ReceiptDetails(product_id=2,receipt_id=2)
        # rd6=ReceiptDetails(product_id=3,receipt_id=2)
        # rd7=ReceiptDetails(product_id=2,receipt_id=2)
        # rd8=ReceiptDetails(product_id=1,receipt_id=2)
        # rd9=ReceiptDetails(product_id=1,receipt_id=3)
        # rd10=ReceiptDetails(product_id=2,receipt_id=3)
        # rd11=ReceiptDetails(product_id=3,receipt_id=3)
        # rd12=ReceiptDetails(product_id=3,receipt_id=4)
        # rd13=ReceiptDetails(product_id=2,receipt_id=4)
        # rd14=ReceiptDetails(product_id=3,receipt_id=4)
        # rd15=ReceiptDetails(product_id=2,receipt_id=5)
        # rd16=ReceiptDetails(product_id=1,receipt_id=5)
        # rd17=ReceiptDetails(product_id=1,receipt_id=5)
        # rd18=ReceiptDetails(product_id=1,receipt_id=6)
        # rd19=ReceiptDetails(product_id=1,receipt_id=6)
        # rd20=ReceiptDetails(product_id=1,receipt_id=6)
        # rd21=ReceiptDetails(product_id=2,receipt_id=6)
        # rd22=ReceiptDetails(product_id=3,receipt_id=6)
        # db.session.add_all([rd1,rd2,rd3,rd4,rd5,rd6,rd7,rd8,rd9,rd10,rd11,rd12,rd13,rd14,rd15,rd16,rd17,rd18,rd19,rd20,rd21,rd22])
        # db.session.commit()


