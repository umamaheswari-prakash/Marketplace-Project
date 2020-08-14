from flask import Flask, request, jsonify,render_template,redirect,url_for,session
from methods import is_valid_user,get_category_list,product_list,insert_into_cart,update_to_cart,delete_cart,view_cart


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
    user_id = user_id
    data=request.get_json()
    product_id =data['product_id']
    quantity = data['quantity']
    result=insert_into_cart(user_id,product_id,quantity)
    return result

@app.route('/cart/<user_id>', methods=['PUT'])
def cart_update(user_id):
    user_id = user_id
    data=request.get_json()
    product_id = data['product_id']
    quantity = data['quantity']
    result = update_to_cart(user_id,product_id,quantity)
    return result


@app.route('/cart/<user_id>', methods=['DELETE'])
def remove_cart_item(user_id):
    user_id = user_id
    data=request.get_json()
    product_id = data['product_id']
    result=delete_cart(user_id,product_id)
    return result


@app.route('/cart/<user_id>', methods=['GET'])
def cart_details(user_id):
    user_id = user_id
    data=view_cart(user_id)
    return jsonify(data),200


@app.route('/logout',methods=['POST'])
def logout():
      session.pop=('logged in',None)
      session.pop=('user_name',None)
      return "logged out successfully",200



if __name__ == "__main__":
    app.run(port=80,debug=True)
