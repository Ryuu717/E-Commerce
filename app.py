from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql
from forms import RegisterForm, RegisterGuestForm, RegisteredForm
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
import pandas as pd
from datetime import date, timedelta


app = Flask(__name__)
app.secret_key = 'random string'


# Login Manager
login_manager = LoginManager(app)
login_manager.login_view = "login"

DB_path = 'EC.db'

class User(UserMixin):
    def __init__(self, UserID, FirstName, Address, LastName, Phone, Email, CardNumber, PayLater, UserType):
         self.UserID = UserID
         self.FirstName = FirstName
         self.LastName = LastName
         self.Address = Address
         self.Phone = Phone
         self.Email = Email
         self.CardNumber = CardNumber
         self.PayLater = PayLater
         self.UserType = UserType
         self.authenticated = False
   #  def is_active(self):
   #       return self.is_active()
    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return self.authenticated
    def is_active(self):
         return True
    def get_id(self):
         return self.UserID
      
      
@login_manager.user_loader
def load_user(UserID):
   con = sql.connect(DB_path)
   cur = con.cursor()
   cur.execute("SELECT * from users where UserID = (?)",[UserID])
   user_info = cur.fetchone()
   if user_info is None:
      return None
   else:
      return User(int(user_info[0]), user_info[1], user_info[2], user_info[3], user_info[4], user_info[5], user_info[6], user_info[7], user_info[8])




@app.route("/")
def main():
   # # logout
   # if str(current_user.get_id()) != 'None':
   #    logout_user()
   
   current_user_id = str(current_user.get_id())
   
   with sql.connect(DB_path) as con:
      cur = con.cursor()
      
      # 0. All Items
      cur.execute("select * from items")
      item_list= cur.fetchall(); 
      
      # 1. Categories
      cur.execute("select * from categories")
      category_list= cur.fetchall(); 
      
      # 2. Recently Viewed
      if str(current_user.get_id()) != 'None':
      # if True:
         try:
            cur.execute("select * from logs where UserID=?", (str(current_user.get_id())))
         except:
            cur.execute("select * from logs") 
      
         recently_viewed_list= cur.fetchall(); 
      
      else:
         cur.execute("select * from items where Tag = 'Electronics'")
         recently_viewed_list= cur.fetchall(); 
   
      
      # 3. Recommended
      cur.execute("select * from items where Tag = 'Recommended'")
      recommended_list= cur.fetchall(); 
      
      # 4.Buy again
      if str(current_user.get_id()) != 'None':
         try:
            cur.execute("select * from orders where UserID=?", (str(current_user.get_id())))   # if user has an order history
         except:
            cur.execute("select * from orders")    # if user doesn't have an order history
         order_list= cur.fetchall(); 
      else:
         cur.execute("select * from items where Tag = 'Health & Personal Care'")
         order_list= cur.fetchall(); 
      
      
      # 5. Great Deal
      cur.execute("select * from items where Tag = 'Deal'")
      deal_list= cur.fetchall(); 
      
      # 6. Popular now
      cur.execute("select * from orders")
      popular_list= cur.fetchall(); 
      
      # 7. Pick up
      cur.execute("select * from items where Tag = 'Pickup'")
      pickup_list= cur.fetchall(); 
   
      # 8. Fitness
      cur.execute("select * from items where Tag = 'Fitness'")
      fitness_list= cur.fetchall(); 
      
      # 9. Promotion
      cur.execute("select * from items where Tag = 'Promotion'")
      promotion_list= cur.fetchall(); 
      
      # 10. For you
      if str(current_user.get_id()) != 'None':
         df = pd.DataFrame(order_list)
         for_you_list = df[6].value_counts().keys()[0]

         cur.execute("select * from items where Category = ?", (for_you_list,))
         for_you_list= cur.fetchall(); 
      else:
         cur.execute("select * from items")
         for_you_list = cur.fetchall(); 
         
      # 11. Footer
      cur.execute("select * from footers")
      footer_list= cur.fetchall(); 
      
      # 12. Health & Personal Care
      cur.execute("select * from items where Tag = 'Health & Personal Care'")
      health_list= cur.fetchall(); 
      
      # 13. Cart 
      cur.execute("select * from carts where UserID = ?",(str(current_user.get_id()),))
      cart_list= cur.fetchall(); 
      cart_list_num = 0
      for item in cart_list:
         cart_list_num += item[12]
         
       
   return render_template("main.html", 
                          current_user_id = current_user_id, 
                          category_list = category_list, 
                          recently_viewed_list = recently_viewed_list, 
                          recommended_list = recommended_list, 
                          order_list = order_list, 
                          health_list = health_list,
                          deal_list = deal_list, 
                          popular_list = popular_list, 
                          pickup_list = pickup_list, 
                          fitness_list = fitness_list, 
                          promotion_list = promotion_list, 
                          for_you_list = for_you_list, 
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num
                          )


@app.route("/signin")
def signin():
   return render_template("signin.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))

# @app.route("/item")
# def item():
   
#    with sql.connect(DB_path) as con:
#       cur = con.cursor()
            
#       # 1. Categories
#       cur.execute("select * from categories")
#       category_list= cur.fetchall(); 
      
#       # 2. Cart
#       cur.execute("select * from carts where UserID = ?",(str(current_user.get_id()),))
#       cart_list= cur.fetchall(); 
#       cart_list_num = len(cart_list)
      
#    return render_template("item.html", 
#                           category_list = category_list,
#                           cart_list = cart_list,
#                           cart_list_num = cart_list_num
#                           )

# @app.route("/items")
# def items():
   
#    with sql.connect(DB_path) as con:
#       cur = con.cursor()
      
#       # 0. Items
#       cur.execute("select * from items")
#       item_list= cur.fetchall(); 
      
#       # 1. Categories
#       cur.execute("select * from categories")
#       category_list= cur.fetchall(); 
      
#    return render_template("items.html", item_list = item_list, category_list = category_list)

@app.route('/show_item', methods = ['GET']) 
def show_item():

   with sql.connect(DB_path) as con:
      con.row_factory = sql.Row 
      cur = con.cursor() 
      
      # 1. item
      cur.execute("select * from orders")
      item_list= cur.fetchall() 
      
      # 2. Categories
      cur.execute("select * from categories")
      category_list= cur.fetchall()
      
      # 3. Footer
      cur.execute("select * from footers")
      footer_list= cur.fetchall(); 
      
   return render_template("item.html", 
                          category_list = category_list,
                          item_list = item_list,
                          footer_list=footer_list)

@app.route('/show_item/<string:Category>', methods = ['GET']) 
def show_item_category(Category):

   with sql.connect(DB_path) as con:
      con.row_factory = sql.Row 
      cur = con.cursor() 
      
      # 1. item
      cur.execute("select * from items where Category=?",(Category,)) 
      item_list= cur.fetchall() 
      
      # 2. Categories
      cur.execute("select * from categories")
      category_list= cur.fetchall()
      
      # 3. Footer
      cur.execute("select * from footers")
      footer_list= cur.fetchall(); 
      
      # 4. Cart 
      cur.execute("select * from carts where UserID = ?",(str(current_user.get_id()),))
      cart_list= cur.fetchall(); 
      cart_list_num = 0
      for item in cart_list:
         cart_list_num += item[12]
      
   return render_template("item.html", 
                          item_list = item_list,
                          category_list = category_list,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num
                          )

@app.route('/show_item/tag=<string:Tag>', methods = ['GET']) 
def show_item_tag(Tag):

   with sql.connect(DB_path) as con:
      con.row_factory = sql.Row 
      cur = con.cursor() 
      
      # 1. item
      cur.execute("select * from items where Tag=?",(Tag,)) 
      item_list= cur.fetchall() 
      
      # 2. Categories
      cur.execute("select * from categories")
      category_list= cur.fetchall()
      
      # 3. Footer
      cur.execute("select * from footers")
      footer_list= cur.fetchall(); 
      
      # 4. Cart 
      cur.execute("select * from carts where UserID = ?",(str(current_user.get_id()),))
      cart_list= cur.fetchall(); 
      cart_list_num = 0
      for item in cart_list:
         cart_list_num += item[12]
      
   return render_template("item.html", 
                          item_list = item_list,
                          category_list = category_list,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num
                          )


@app.route('/show_item/<string:Category>/rating=<string:Rating>', methods = ['GET']) 
def show_item_rating(Category, Rating):

   with sql.connect(DB_path) as con:
      con.row_factory = sql.Row 
      cur = con.cursor() 
      
      # 1. item
      cur.execute("select * from items where Category=? and Rating=? ",(Category, Rating)) 
      item_list= cur.fetchall() 
      
      # 2. Categories
      cur.execute("select * from categories")
      category_list= cur.fetchall()
      
      # 3. Footer
      cur.execute("select * from footers")
      footer_list= cur.fetchall(); 
      
      # 4. Cart 
      cur.execute("select * from carts where UserID = ?",(str(current_user.get_id()),))
      cart_list= cur.fetchall(); 
      cart_list_num = 0
      for item in cart_list:
         cart_list_num += item[12]
      
   return render_template("item.html", 
                          item_list = item_list,
                          category_list = category_list,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num
                          )


@app.route('/show_item/<string:Category>/price=<string:Sort>', methods = ['GET']) 
def show_item_price_order(Category, Sort):

   with sql.connect(DB_path) as con:
      con.row_factory = sql.Row 
      cur = con.cursor() 
      
      
      # 1. item
      if Sort == 'ASC':
         cur.execute("select * from items where Category=? order by Price ASC",(Category,)) 
      else:
         cur.execute("select * from items where Category=? order by Price DESC",(Category,)) 
      item_list= cur.fetchall() 
      
      # 2. Categories
      cur.execute("select * from categories")
      category_list= cur.fetchall()
      
      # 3. Footer
      cur.execute("select * from footers")
      footer_list= cur.fetchall(); 
      
      # 4. Cart 
      cur.execute("select * from carts where UserID = ?",(str(current_user.get_id()),))
      cart_list= cur.fetchall(); 
      cart_list_num = 0
      for item in cart_list:
         cart_list_num += item[12]
      
   return render_template("item.html", 
                          item_list = item_list,
                          category_list = category_list,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num)
   

@app.route('/show_items/<string:ItemID>', methods = ['GET']) 
def show_items(ItemID):

   with sql.connect(DB_path) as con:
      con.row_factory = sql.Row 
      cur = con.cursor() 
      
      # 1. item detail
      cur.execute("select * from items where ItemID=?",(ItemID,)) 
      item_detail= cur.fetchall() 
      
      
      # 2. Related Items
      cur.execute("select * from items where Category=?",(item_detail[0]["Category"],)) 
      related_items= cur.fetchall() 
   
      # 3. Searched items(Customers also search)
      cur.execute("select * from logs where Category=?",(item_detail[0]["Category"],)) 
      searched_items= cur.fetchall() 
      
      # 4. Categories
      cur.execute("select * from categories")
      category_list= cur.fetchall()
      
      # 5. Footer
      cur.execute("select * from footers")
      footer_list= cur.fetchall(); 
      
      # 6. Cart 
      cur.execute("select * from carts where UserID = ?",(str(current_user.get_id()),))
      cart_list= cur.fetchall(); 
      cart_list_num = 0
      for item in cart_list:
         cart_list_num += item[12]
      
      # 7. Date
      today = date.today()
      delivery_date = today + timedelta(days=7)
      month = delivery_date.strftime("%b")
      day = delivery_date.strftime("%d")
      year = delivery_date.strftime("%Y")
      weekday = delivery_date.strftime("%a")
      
      delivery_date = f"{month}, {day}, {year} ({weekday})"
      
      # 8. User ID
      current_user_id = current_user_id = str(current_user.get_id())
      
   return render_template("items.html", 
                          current_user_id = current_user_id,
                          category_list = category_list,
                          item_detail = item_detail,
                          related_items = related_items,
                          searched_items = searched_items,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num,
                          delivery_date = delivery_date)

# @app.route("/payment")
# def payment():
#    return render_template("payment.html")



@app.route("/payment/<string:UserID>", methods=['GET', 'POST'])
def payment(UserID):
   item_list = []
   category_list = []
   
   with sql.connect(DB_path) as con:
      con.row_factory = sql.Row 
      cur = con.cursor() 
      
      # 1. Categories
      cur.execute("select * from categories")
      category_list= cur.fetchall()
      
      # 2. Cart 
      cur.execute("select * from carts where UserID = ?",(UserID,))
      cart_list= cur.fetchall(); 
      cart_list_num = 0
      for item in cart_list:
         cart_list_num += item[12]
      
      # 3. Total Cost
      total_cost = 0
      for item in cart_list:
         # total_cost += float(item["Price"])
         total_cost += float(item[7]) * float(item[12])
      
      # 4. User Details
      cur.execute("select * from users where UserID=?",(UserID,)) 
      user_list= cur.fetchone(); 
      
      # 5. Date
      today = date.today()
      delivery_date = today + timedelta(days=7)
      month = delivery_date.strftime("%b")
      day = delivery_date.strftime("%d")
      year = delivery_date.strftime("%Y")
      weekday = delivery_date.strftime("%a")
      
      delivery_date = f"{month}, {day}, {year} ({weekday})"
      
      
      
      
   return render_template("payment.html",
                          category_list = category_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num,
                          total_cost = total_cost,
                          user_list = user_list,
                          delivery_date = delivery_date
                          )


# @app.route("/register")
# def register():
#    return render_template("register.html")

@app.route("/register")
def register():
    form = RegisterForm()
    if request.method == 'POST': 
        if form.validate() == False: 
            flash('All fields are required.') 
            return render_template('register.html', form = form) 
        else: 
            return render_template('main.html') 
    
    if request.method == 'GET': 
        return render_template('register.html', form = form) 
    return "test"

@app.route("/register_guest")
def register_guest():
    form = RegisterGuestForm()
    if request.method == 'POST': 
        if form.validate() == False: 
            flash('All fields are required.') 
            return render_template('register_guest.html', form = form) 
        else: 
            return render_template('main.html') 
    
    if request.method == 'GET': 
        return render_template('register_guest.html', form = form) 
    return "test"


@app.route('/add_guest', methods=['GET', 'POST'])
def add_guest(): 
   item_list = []
   category_list = []
   
   with sql.connect(DB_path) as con:
      cur = con.cursor()
      cur.execute("select * from items")
      item_list= cur.fetchall(); 
      
      cur.execute("select * from categories")
      category_list= cur.fetchall(); 
      
      
   form = RegisterGuestForm()
   
   if form.validate_on_submit(): 
      cur.execute("INSERT INTO users (FirstName, LastName, Address, Phone, Email, CardNumber, UserType) VALUES (?,?,?,?,?,?,?)",(form.first_name.data, form.last_name.data, form.address.data, form.phone.data, form.email.data, form.card_number.data, "Guest"))
      con.commit()
      cur.execute("select * from users where Email=?",(form.email.data,)) 
      new_user= cur.fetchone(); 
      
      
      new_user = load_user(new_user[0])
      login_user(new_user)
      print(f"Current User: {current_user.get_id()}")
      # msg = "Registered successfully"
      # return redirect(url_for('main')) 
      return redirect(url_for('success',request = "guest"))
   
   else:
      return render_template('register_guest.html', form = form)
   


@app.route('/add_account', methods=['GET', 'POST'])
def add_account(): 
   item_list = []
   category_list = []
   
   with sql.connect(DB_path) as con:
      cur = con.cursor()
      cur.execute("select * from items")
      item_list= cur.fetchall(); 
      
      cur.execute("select * from categories")
      category_list= cur.fetchall(); 
      
      
   form = RegisterForm()
   
   if form.validate_on_submit(): 
      cur.execute("INSERT INTO users (FirstName, LastName, Phone, Email) VALUES (?,?,?,?)",(form.first_name.data, form.last_name.data, form.phone.data, form.email.data))
      con.commit()
      cur.execute("select * from users where Email=?",(form.email.data,)) 
      new_user= cur.fetchone(); 
      
      
      new_user = load_user(new_user[0])
      login_user(new_user)
      print(f"Current User: {current_user.get_id()}")
      # msg = "Registered successfully"
      # return redirect(url_for('main')) 
      return redirect(url_for('success'))
   
   else:
      return render_template('register.html', form = form)
   


@app.route('/show_account/<string:UserID>', methods = ['GET']) 
def show_account(UserID):
   
   form = RegisterForm()
   registered_form = RegisteredForm()
   
   with sql.connect(DB_path) as con:
      con.row_factory = sql.Row 
      cur = con.cursor() 
   
      # 1. Categories
      cur.execute("select * from categories")
      category_list= cur.fetchall() 
   
      # 2. Accounts
      cur.execute("select * from users where UserID=?",(UserID,)) 
      account_list= cur.fetchall()
      
      # 3. Orders
      cur.execute("select * from orders where UserID=?",(UserID,)) 
      order_list= cur.fetchall()
      
      # 4. Wishes
      cur.execute("select * from items where Wishers=?",(UserID,)) 
      wisher_list= cur.fetchall(); 
      
      # 5. Footer
      cur.execute("select * from footers")
      footer_list= cur.fetchall(); 
      
   return render_template("account.html", 
                          category_list = category_list,
                          account_list = account_list, 
                          order_list = order_list,
                          wisher_list = wisher_list,
                          form = form, 
                          registered_form = registered_form, 
                          footer_list=footer_list)


@app.route('/signin_user', methods=['GET', 'POST'])
def signin_user():
   Email = request.form['Email']
   
   with sql.connect(DB_path) as con:
      cur = con.cursor()
      cur.execute("select * from users where Email=?",(Email,)) 
      # user_info= cur.fetchall()
      registered_user= cur.fetchone(); 
      
      if registered_user:
         # msg ="Sign in successfully"
         
         registered_user = load_user(registered_user[0])
         login_user(registered_user)
         # flash('You were successfully logged in')
         # return redirect(url_for('main'))
         return redirect(url_for('success', request="signin"))
         
         
      else:
         # msg="Your email is not registered."
         flash('Your email is not registered')
         return redirect(url_for('signin')) 
         # con.rollback()
   

@app.route('/update_account', methods=['GET', 'POST'])
def update_account():
   form = RegisteredForm()

   if form.validate_on_submit(): 
      with sql.connect(DB_path) as con: 
         cur = con.cursor() 
         cur.execute("UPDATE users SET FirstName=?, LastName=?, Address=?, Phone=?, Email=?, CardNumber=? WHERE UserID=?", (form.first_name.data, form.last_name.data, form.address.data, form.phone.data, form.email.data, form.card_number.data,current_user.UserID)) 
         con.commit()
         msg="Data Updated Successfully"
         return redirect(url_for('show_account',UserID=current_user.UserID)) 
      
   else:
      msg="error in update operation" 
      return redirect(url_for('show_account',UserID=current_user.UserID)) 
   


@app.route('/add_cart/<string:ItemID>', methods=['GET', 'POST'])
def add_cart(ItemID): 
   item_list = []
   category_list = []
   
   item_count = request.form['quantity']
   
   with sql.connect(DB_path) as con:
      cur = con.cursor()
      
      cur.execute("select * from items where ItemID = ?",(ItemID,))
      item_list= cur.fetchall(); 
      
      Date = date.today()
      UserID = current_user.get_id()
      UserName = current_user.FirstName
      ItemID = item_list[0][0]
      ItemName = item_list[0][1]
      Category = item_list[0][2]
      Price = item_list[0][3]
      Detail = item_list[0][4]
      Rating = item_list[0][5]
      Reviews = item_list[0][6]
      ImageURL = item_list[0][7]
      ItemCount = item_count
      
      # 1. Category list
      cur.execute("select * from categories")
      category_list= cur.fetchall(); 
      
      # 2. Cart 
      cur.execute("select * from carts where UserID = ?",(UserID,))
      cart_list= cur.fetchall(); 
      cart_list_num = 0
      for item in cart_list:
         cart_list_num += item[12]
      
      # 3. Total Cost
      total_cost = 0
      for item in cart_list:
         # total_cost += float(item["Price"])
         total_cost += float(item[7])
      
      # 4. User Details
      cur.execute("select * from users where UserID=?",(UserID,)) 
      user_list= cur.fetchone(); 
      
      
      # 5. Date
      today = date.today()
      delivery_date = today + timedelta(days=7)
      month = delivery_date.strftime("%b")
      day = delivery_date.strftime("%d")
      year = delivery_date.strftime("%Y")
      weekday = delivery_date.strftime("%a")
      
      delivery_date = f"{month}, {day}, {year} ({weekday})"
      
				
      cur.execute("INSERT INTO carts (Date, UserID, UserName, ItemID, ItemName, Category, Price, Detail, Rating, Reviews, ImageURL, ItemCount) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(Date, UserID, UserName, ItemID, ItemName, Category, Price, Detail, Rating, Reviews, ImageURL, ItemCount))
      # con.commit()


   return redirect(url_for('success', request= "add_cart"))


@app.route('/pay_now/<string:ItemID>', methods=['GET', 'POST'])
def pay_now(ItemID): 
   item_list = []
   category_list = []
   
   item_count = request.form['quantity']
   
   with sql.connect(DB_path) as con:
      cur = con.cursor()
      
      cur.execute("select * from items where ItemID = ?",(ItemID,))
      item_list= cur.fetchall(); 
      
      Date = date.today()
      UserID = current_user.get_id()
      UserName = current_user.FirstName
      ItemID = item_list[0][0]
      ItemName = item_list[0][1]
      Category = item_list[0][2]
      Price = item_list[0][3]
      Detail = item_list[0][4]
      Rating = item_list[0][5]
      Reviews = item_list[0][6]
      ImageURL = item_list[0][7]
      ItemCount = item_count
      
      # 1. Category list
      cur.execute("select * from categories")
      category_list= cur.fetchall(); 
      
      # 2. Cart 
      cur.execute("select * from carts where UserID = ?",(UserID,))
      cart_list= cur.fetchall(); 
      cart_list_num = 0
      for item in cart_list:
         cart_list_num += item[12]
      
      # 3. Total Cost
      total_cost = 0
      for item in cart_list:
         # total_cost += float(item["Price"])
         total_cost += float(item[7])
      
      # 4. User Details
      cur.execute("select * from users where UserID=?",(UserID,)) 
      user_list= cur.fetchone(); 
      
      
      # 5. Date
      today = date.today()
      delivery_date = today + timedelta(days=7)
      month = delivery_date.strftime("%b")
      day = delivery_date.strftime("%d")
      year = delivery_date.strftime("%Y")
      weekday = delivery_date.strftime("%a")
      
      delivery_date = f"{month}, {day}, {year} ({weekday})"
      
				
      cur.execute("INSERT INTO carts (Date, UserID, UserName, ItemID, ItemName, Category, Price, Detail, Rating, Reviews, ImageURL, ItemCount) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(Date, UserID, UserName, ItemID, ItemName, Category, Price, Detail, Rating, Reviews, ImageURL, ItemCount))
      # con.commit()


   return redirect(url_for('payment', UserID= UserID))
   

@app.route('/payment/update_cart/<string:ItemID>', methods=['GET', 'POST'])
def update_cart(ItemID): 
   
   item_count = request.form['quantity']
   
   with sql.connect(DB_path) as con:
      cur = con.cursor()
      
      cur.execute("UPDATE carts SET ItemCount = ? WHERE CartID = ?",(item_count, ItemID,))
      con.commit()
      
      return redirect(url_for('payment', UserID= current_user.get_id()))


@app.route('/payment/delete_cart/<string:ItemID>', methods=['GET', 'POST'])
def delete_cart(ItemID): 
   with sql.connect(DB_path) as con:
      cur = con.cursor()
   
      cur.execute("DELETE FROM carts WHERE CartID=?",(ItemID,))
      con.commit() 
   
   return redirect(url_for('payment', UserID= current_user.get_id()))
  
  
@app.route("/success/<string:request>")
def success(request):
   if request == "order":
      title = "Ordered successfully"
      detail = "Thank you for placing your order!"
      
      with sql.connect(DB_path) as con:
         cur = con.cursor()
         
         if current_user.UserType == "Guest":
            # Delete cart items
            cur.execute("select CartID from carts where UserID=?", (str(current_user.get_id()),))
            delete_list= cur.fetchall(); 
            print(delete_list)
            for num in delete_list:
               cur.execute("DELETE FROM carts WHERE CartID=?",(num[0],))
               
            cur.execute("DELETE FROM users WHERE UserType=?",("Guest",))
            title = "Ordered successfully"
            detail = "Thank you for placing your order!"
            
         else:
           
            # Records orders 
            cur.execute("select * from carts where UserID=?", (str(current_user.get_id())),)
            cart_list= cur.fetchall(); 
            
            for num in cart_list:         
               Date = date.today()
               UserID = current_user.get_id()
               UserName = current_user.FirstName
               ItemID = num[0]
               ItemName = num[5]
               Category = num[6]
               Price = num[7]
               Detail = num[8]
               Rating = num[9]
               Reviews = num[10]
               ImageURL = num[11]
               ItemCount = num[12]
               
               cur.execute("INSERT INTO orders (Date, UserID, UserName, ItemID, ItemName, Category, Price, Detail, Rating, Reviews, ImageURL, ItemCount) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(Date, UserID, UserName, ItemID, ItemName, Category, Price, Detail, Rating, Reviews, ImageURL, ItemCount))
            
            # Delete cart items
            cur.execute("select CartID from carts where UserID=?", (str(current_user.get_id())),)
            delete_list= cur.fetchall(); 
            for num in delete_list:
               cur.execute("DELETE FROM carts WHERE CartID=?",(num[0],))
            
            con.commit()
   
   elif request == "signin":
      title = "Sign in successfully"
      detail = "Welcome to " + current_user.FirstName + " " + current_user.LastName
      
   elif request == "add_cart":
      title = "Added item successfully"
      detail = "Keep enjoy your shopping!"
      
   elif request == "guest":
      title = "Temporaly your information is recorded"
      detail = "Enjoy your shopping!"
      
   return render_template("success.html", title=title, detail=detail) 


@app.route("/orders/<string:UserID>", methods=['GET', 'POST'])
def orders(UserID):
   
   with sql.connect(DB_path) as con:
      con.row_factory = sql.Row 
      cur = con.cursor() 
      
      # 1. Categories
      cur.execute("select * from categories")
      category_list= cur.fetchall()
      
      # 2. Order detail
      cur.execute("select * from orders where UserID=?",(UserID,)) 
      order_list= cur.fetchall(); 
      # order_list_num = len(order_list)
      
      
      
      # 3. Total Cost
      total_cost = 0
      for item in order_list:
         total_cost += float(item["Price"])
      
      # 4. User Details
      # cur.execute("select * from users where UserID=?",(UserID,)) 
      # user_list= cur.fetchone(); 
      
      # 5. Date
      # today = date.today()
      # delivery_date = today + timedelta(days=7)
      # month = delivery_date.strftime("%b")
      # day = delivery_date.strftime("%d")
      # year = delivery_date.strftime("%Y")
      # weekday = delivery_date.strftime("%a")
      
      # delivery_date = f"{month}, {day}, {year} ({weekday})"
      
      
   return render_template("orders.html",
                          category_list = category_list,
                          order_list = order_list
                        #   order_list_num = order_list_num,
                        #   total_cost = total_cost,
                        #   user_list = user_list,
                        #   delivery_date = delivery_date
                          )


if __name__ == '__main__':
   app.run(debug = True)