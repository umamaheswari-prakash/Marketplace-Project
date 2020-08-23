from flask import Flask,request,jsonify,render_template,url_for
from werkzeug.utils import redirect
from flask import session
from methods import *

app = Flask(__name__)
app.secret_key="onlineShopping"


@app.route('/')
def Home():
    return "welcome to the online Bazaar",200

@app.route('/login', methods=['GET','POST'])
def get_login_details():
    data=request.get_json()
    user_name = data['user_name']
    password = data['password']
    result=is_valid_user(user_name,password)
    if result== True:
        session['password']=password
        return "logged in successfully ",200
        #return redirect(url_for(Home))
    else:
       #return  render_template(url_for('login.hlml'))
       return "invalid user_name or password",401

@app.route('/category', methods=['GET'])
def get_category():
    category=get_category_list()
    return jsonify(category),200

@app.route('/category/<id>', methods=['GET'])
def get_available_items(id):
    category_id = id
    list=product_list(category_id)
    return jsonify(list),200

@app.route('/cart/<user_id>', methods=['POST'])
def add_to_cart(user_id):
    data=request.get_json()
    product_id =data['product_id']
    quantity = data['quantity']
    current_user=check_current_user(user_id,session['password'])
    try:
      if current_user==True:
         result=insert_into_cart(user_id,product_id,quantity)
         if result==True:
            return "add_to_cart successfully", 200
         elif result==False:
            return "Enter a valid quantity",400
         else:
            return "stock is unavailable",400
    except Exception as e:
      return (str(e))
    return "cannot access:'unauthorized user",403


@app.route('/cart/<user_id>', methods=['PUT'])
def cart_update(user_id):
    user_id = user_id
    data=request.get_json()
    product_id = data['product_id']
    quantity = data['quantity']
    current_user = check_current_user(user_id,session['password'])
    if current_user== True:
       try:
          result = update_to_cart(user_id,product_id,quantity)
          if result==True:
            return "Cart successfully updated", 200
          else:
            data=delete_cart(user_id,product_id)
            return data
       except Exception as e:
          return (str(e))
    else:
       return "cannot access:'unauthorized user", 403


@app.route('/cart/<user_id>', methods=['DELETE'])
def remove_cart_item(user_id):
    user_id = user_id
    data=request.get_json()
    product_id = data['product_id']
    current_user = check_current_user(user_id,session['password'])
    if current_user== True:
        try:
          result = delete_cart(user_id, product_id)
          if result == True:
            return "Cart item removed successfully", 200
        except Exception as e:
            return (str(e))
    else:
      return "cannot access:'unauthorized user'",403


@app.route('/cart/<user_id>', methods=['GET'])
def cart_details(user_id):
    user_id = user_id
    current_user = check_current_user(user_id,session['password'])
    if current_user == True:
      data=view_cart(user_id)
      return jsonify(data),200
    else:
      return "cannot access:'unauthorized user",403

@app.route('/logout/<user_id>',methods=['POST'])
def logout(user_id):
      session.pop=('password',None)
      result=logged_out(user_id)
      if result==True:
         return "logged out successfully",200
      else:
         return "please login"

if __name__ == "__main__":
    app.run(port=80,debug=True)
