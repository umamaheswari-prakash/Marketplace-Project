from models import User,Product,Cart,Category,Seller
from database import db_connect
db_session=db_connect()

def is_valid_user(user_name,password):
   user=db_session.query(User).filter_by(name=user_name, password=password).first()
   auth=True
   user.is_authenticated=auth
   if user==None:
     return False
   else:
     db_session.add(user)
     db_session.commit()
     return True,user.id

def check_current_user(user_id):
    data=db_session.query(User).filter_by(id=user_id).first()
    auth=data.is_authenticated
    if auth==True:
         return True
    else:
      return False

def get_category_list():
    result=[]
    list = db_session.query(Category).all()
    for category in list:
        dict = {}
        dict['id'] = category.id
        dict['name'] = category.name
        result.append(dict)
    return result


def product_list(category_id):
    result=[]
    items = db_session.query(Product).filter(Product.category_id == category_id).all()
    for row in items:
        dict1={}
        dict1['id'] = row.id
        dict1['name'] = row.name
        dict1['price']=int(row.price)
        dict1['description']=row.description
        result.append(dict1)
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

def get_products_list(user_id):
    product_list = []
    products =db_session.query(Cart).filter_by(user_id=user_id)
    for product in products:
        product_list.append(product.product_id)
    return product_list

def desired_quantity(user_id,product_id):
    quantity = db_session.query(Cart).filter_by(user_id=user_id, product_id=product_id).first()
    return quantity
def seller_datails(seller_id):
    name=db_session.query(Seller).filter_by(id=seller_id).first()
    return name

def view_cart(user_id):
    list=get_products_list(user_id)
    print(list)
    result=[]
    detail = db_session.query(Product).all()
    for data in detail:
        if data.id in list:
            quantity = desired_quantity(user_id,data.id)
            seller=seller_datails(data.seller_id)
            result.append(cart_list(data,quantity,seller))
    return result
def cart_list(data,quantity,seller):
    dict = {}
    dict["id"] = data.id
    dict["Product"] = data.name
    dict["Seller"]=seller.name
    dict["Price"] = int(data.price)
    dict["Quantity"] = quantity.count
    return dict

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
