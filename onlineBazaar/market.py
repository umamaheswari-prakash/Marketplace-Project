from flask import Flask,request,jsonify,render_template,url_for
from werkzeug.utils import redirect
from flask import session
from flask_cors import CORS,cross_origin
from methods import *
import os

app = Flask(__name__,template_folder='templates',static_folder='static')
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.secret_key="onlineShopping"

@cross_origin()
@app.route('/login', methods=['POST'])
def get_login_details():
       value=request.get_json()
       print("error",value)
       user_name=value['user_name']
       password =value['password']
       print(user_name,password)
       (result,userid)=is_valid_user(user_name,password)
       if result== True:
          session['password']=password
          print("logged in successfully,200")
          return jsonify({'ok':200,'user_id':userid})
       else:
          return jsonify({'ok': '401'})

@cross_origin()
@app.route('/categories', methods=['GET'])
def get_categories():
    categories=get_category_list()
    return jsonify(categories),200

@cross_origin()
@app.route('/category/<id>', methods=['GET'])
def get_available_items(id):
    category_id = id
    list=product_list(category_id)
    return jsonify(list),200

@cross_origin()
@app.route('/cart/<user_id>', methods=['POST'])
def add_to_cart(user_id):
    value=request.get_json()
    product_id =value['product_id']
    quantity = 1
    current_user=check_current_user(user_id)
    if current_user == True:
        result = insert_into_cart(user_id, product_id, quantity)
        try:
           if result==True:
              return jsonify({'ok':'add to cart successfully'})
           elif result==False:
              return jsonify({'ok':'enter valid quantity'})
           else:
              return jsonify({'ok':'stock is unavailable'})
        except Exception as e:
           return (str(e))
    return jsonify({'ok':'unauthorized user'})

@cross_origin()
@app.route('/cart/<user_id>', methods=['PUT'])
def cart_update(user_id):
    user_id = user_id
    data=request.get_json()
    product_id = data['product_id']
    quantity = data['quantity']
    current_user = check_current_user(user_id)
    if current_user== True:
       try:
          result = update_to_cart(user_id,product_id,quantity)
          if result==True:
            return  jsonify({'ok':'cart updated successfully'})
          else:
            data=delete_cart(user_id,product_id)
            return jsonify(data)
       except Exception as e:
          return (str(e))
    else:
       return jsonify({'ok':'unauthorized user'})

@cross_origin()
@app.route('/cart/<user_id>', methods=['DELETE'])
def remove_cart_item(user_id):
    user_id = user_id
    value=request.get_json()
    print(value)
    product_id = value['product_id']
    current_user = check_current_user(user_id)
    if current_user== True:
        try:
          result = delete_cart(user_id, product_id)
          if result == True:
             return jsonify({'ok':'cart item removed successfully'})
        except Exception as e:
            return (str(e))
    else:
      return jsonify({'ok':'unauthorized user'})

@cross_origin()
@app.route('/cart/<user_id>',methods=['GET'])
def cart_details(user_id):
    user_id = user_id
    current_user = check_current_user(user_id)
    if current_user == True:
      data=view_cart(user_id)
      return jsonify(data),200
    else:
      return jsonify({'ok':'unauthorized user'})

@cross_origin()
@app.route('/logout/<user_id>',methods=['POST'])
def logout(user_id):
      result=logged_out(user_id)
      if result==True:
         return jsonify({'ok':'logout successfully'})
      else:
         return jsonify({'ok':'please login'})

if __name__ == "__main__":
    app.run(port=80,debug=True)
