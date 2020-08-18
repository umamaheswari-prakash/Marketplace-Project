from flask import Flask, request, jsonify,render_template,redirect,url_for,session
from methods import is_valid_user,get_category_list,product_list,insert_into_cart,update_to_cart,delete_cart,view_cart,check_current_user,logged_out


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
         session['user_name']=user_name
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
    current_user=check_current_user(user_id)
    if current_user==True:
       result=insert_into_cart(user_id,product_id,quantity)
       if result==True:
          return "add_to_cart successfully", 200
       elif result==False:
          return "Enter a valid quantity",400
       else:
          return "stock is unavailable",400
    else:
        return "unathorized user",403

@app.route('/cart/<user_id>', methods=['PUT'])
def cart_update(user_id):
    user_id = user_id
    data=request.get_json()
    product_id = data['product_id']
    quantity = data['quantity']
    current_user = check_current_user(user_id)
    if current_user== True:
       result = update_to_cart(user_id,product_id,quantity)
       if result==True:
          return "Cart successfully updated", 200
       else:
          data=delete_cart(user_id,product_id)
          return data
    else:
       return "permission not given",403


@app.route('/cart/<user_id>', methods=['DELETE'])
def remove_cart_item(user_id):
    user_id = user_id
    data=request.get_json()
    product_id = data['product_id']
    current_user = check_current_user(user_id)
    if current_user== True:
        result = delete_cart(user_id, product_id)
        if result == True:
          return "Cart item removed successfully", 200
    else:
        return "permission not given",403


@app.route('/cart/<user_id>', methods=['GET'])
def cart_details(user_id):
    user_id = user_id
    current_user = check_current_user(user_id)
    if current_user == True:
      data=view_cart(user_id)
      return jsonify(data),200
    else:
      return "permission not given",403

@app.route('/logout',methods=['POST'])
def logout():
      session.pop=('logged in',None)
      session.pop=('user_name',None)
      result=logged_out()
      if result==True:
         return "logged out successfully",200
      else:
         return "already logout"



if __name__ == "__main__":
    app.run(port=80,debug=True)
