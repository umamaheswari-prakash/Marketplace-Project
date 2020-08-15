from domain_entities import User, Category, Cart, Product
from database_connection import db_connect
session=db_connect()


def is_valid_user(user_name,password):
    details=session.query(User).filter_by(name=user_name, password=password).first()
    details.name=user_name
    details.password=password
    details.authentication=True
    if details !=None:
       session.add(details)
       session.commit()
       return True
    else:
       return False

def check_current_user(user_id):
    user=session.query(User).filter_by(id=user_id).first()
    if user.authentication==True:
        return True
    else:
        return False



def get_category_list():
    result=[]
    list = session.query(Category).all()
    for category in list:
        result.append("category_id:{}  category_name:{}".format(category.id,category.name))
    return result

def product_list(category_id):
    result=[]
    items = session.query(Product).filter(Product.category_id == category_id).all()
    for row in items:
        result.append("Id:{}    Name:{}   price:{}".format(row.id, row.name, row.price))
    return result


def insert_into_cart(user_id,product_id,quantity):
    stock = session.query(Product).filter_by(id=product_id).first()
    available_stock = stock.count
    if available_stock > int(quantity) and int(quantity)>0:
        item = Cart(user_id=user_id, product_id=product_id, count=quantity)
        session.add(item)
        session.commit()
        return "add_to_cart successfully", 200
    elif int(quantity)<=0:
        return "enter a valid quantity",400
    else:
        return "stock is unavailable", 400

def update_to_cart(user_id,product_id,quantity):
    product = session.query(Cart).filter_by(user_id=user_id, product_id=product_id).one()
    product.product_id = product_id
    product.count = quantity
    session.add(product)
    session.commit()
    return "Cart successfully updated", 200

def delete_cart(user_id,product_id):
    product = session.query(Cart).filter_by(user_id=user_id, product_id=product_id).first()
    session.delete(product)
    session.commit()
    return "Cart item removed successfully", 200



def view_cart(user_id):
    list=[]
    result=[]
    products = session.query(Cart).filter_by(user_id=user_id).all()
    for row in products:
        list.append(row.product_id)
    detail = session.query(Product).all()
    for data in detail:
        if data.id in list:
            result.append("Id:{}   Product:{}   Price:{}   Quantity:{}".format(data.id, data.name, data.price, data.count))
    return result

def logged_out(user_id):
    user=session.query(User).filter_by(id=user_id).one()
    user.authentication=False
    session.add(user)
    session.commit()
    return True
