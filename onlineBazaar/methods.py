from models import User,Product,Cart,Category
from database import db_connect
db_session=db_connect()

def is_valid_user(user_name,password):
   user=db_session.query(User).filter_by(name=user_name, password=password).first()
   auth=True
   user.is_authenticated=auth
   if db_session.query(User).filter_by(name=user_name, password=password).first():
      db_session.add(user)
      db_session.commit()
      return True
   else:
      return False

def check_current_user(user_id,password):
    data=db_session.query(User).filter_by(id=user_id).first()
    auth=data.is_authenticated
    pswd=data.password
    if auth==True:
      if password ==pswd:
         return True
      else:
        return False
    else:
      return False

def get_category_list():
    result=[]
    list = db_session.query(Category).all()
    for category in list:
        result.append("category_id:{}  category_name:{}".format(category.id,category.name))
    return result

def product_list(category_id):
    result=[]
    items = db_session.query(Product).filter(Product.category_id == category_id).all()
    for row in items:
        result.append("Id:{}    Name:{}   price:{}".format(row.id, row.name, row.price))
    return result

def insert_into_cart(user_id,product_id,quantity):
    stock = db_session.query(Product).filter_by(id=product_id).first()
    available_stock = stock.count
    if available_stock > int(quantity) and int(quantity)>0:
        item = Cart(user_id=user_id, product_id=product_id, count=quantity)
        db_session.add(item)
        db_session.commit()
        return True
    elif int(quantity)<=0:
        return False
    else:
        return "result"

def update_to_cart(user_id,product_id,quantity):
    product = db_session.query(Cart).filter_by(user_id=user_id, product_id=product_id).first()
    product.product_id = product_id
    product.count = quantity
    if int(quantity)>0:
      db_session.add(product)
      db_session.commit()
      return True
    else:
      return False

def delete_cart(user_id,product_id):
    product = db_session.query(Cart).filter_by(user_id=user_id, product_id=product_id).first()
    db_session.delete(product)
    db_session.commit()
    return True

def view_cart(user_id):
    list=[]
    result=[]
    products = db_session.query(Cart).filter_by(user_id=user_id).all()
    for row in products:
        list.append(row.product_id)
    detail = db_session.query(Product).all()
    for data in detail:
        if data.id in list:
            result.append("Id:{}   Product:{}   Price:{}   Quantity:{}".format(data.id, data.name, data.price, data.count))
    return result

def logged_out(user_id):
    user = db_session.query(User).filter_by(id=user_id).first()
    if user.is_authenticated==True:
        auth = False
        user.is_authenticated = auth
        db_session.add(user)
        db_session.commit()
        return True
    else:
        return False
