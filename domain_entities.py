from sqlalchemy import Integer, String,Column,ForeignKey,BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(120),unique=True)
    password=Column(String(20),unique=True)
    authentication=Column(BOOLEAN,default=False)
    cart = relationship('Cart', backref='User')


class Category(Base):

    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    product=relationship('Product',backref='Category')



class Seller(Base):

    __tablename__ = 'seller'
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    product= relationship('Product', backref='Seller')


class Product(Base):

    __tablename__ = 'product'
    id = Column(Integer,primary_key=True)
    name = Column(String(120))
    price = Column(Integer)
    count=Column(Integer)
    description =Column(Integer)
    seller_id=Column(Integer, ForeignKey('seller.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    cart = relationship('Cart', backref='Product')
class Cart(Base):

    __tablename__ = 'cart'
    id=Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    product_id = Column(Integer,ForeignKey('product.id'))
    count = Column(Integer)































