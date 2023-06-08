from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql
from forms import RegisterForm, RegisteredForm
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
import pandas as pd

app = Flask(__name__)
app.secret_key = 'random string'


# Login Manager
login_manager = LoginManager(app)
login_manager.login_view = "login"

DB_path = 'EC.db'

class User(UserMixin):
    def __init__(self, UserID, FirstName, LastName, Phone, Email):
         self.UserID = UserID
         self.FirstName = FirstName
         self.LastName = LastName
         self.Phone = Phone
         self.Email = Email
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
      return User(int(user_info[0]), user_info[1], user_info[2], user_info[3], user_info[4])




@app.route("/")
def main():
   # # logout
   # if str(current_user.get_id()) != 'None':
   #    logout_user()
   
   current_user_id = str(current_user.get_id())
   print(current_user_id)
   
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
                          footer_list=footer_list)


@app.route("/signin")
def signin():
   return render_template("signin.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))

@app.route("/item")
def item():
   
   with sql.connect(DB_path) as con:
      cur = con.cursor()
            
      # 1. Categories
      cur.execute("select * from categories")
      category_list= cur.fetchall(); 
      
   return render_template("item.html", category_list = category_list)



@app.route("/items")
def items():
   
   with sql.connect(DB_path) as con:
      cur = con.cursor()
      
      # 0. Items
      cur.execute("select * from items")
      item_list= cur.fetchall(); 
      
      # 1. Categories
      cur.execute("select * from categories")
      category_list= cur.fetchall(); 
      
   return render_template("items.html", item_list = item_list, category_list = category_list)

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
      
   return render_template("item.html", 
                          item_list = item_list,
                          category_list = category_list,
                          footer_list=footer_list)


@app.route('/show_items/<string:ItemID>', methods = ['GET']) 
def show_items(ItemID):

   with sql.connect(DB_path) as con:
      con.row_factory = sql.Row 
      cur = con.cursor() 
      
      # 1. item detail
      cur.execute("select * from items where ItemID=?",(ItemID,)) 
      item_detail= cur.fetchall() 
      
      
      # #  Related Items
      # cur.execute("select * from items where Category=?",(item_detail[0]["Category"],)) 
      # related_items= cur.fetchall() 
   
      # #  Searched items(Customers also search)
      # cur.execute("select * from logs where Category=?",(item_detail[0]["Category"],)) 
      # searched_items= cur.fetchall() 
      
      # Categories
      cur.execute("select * from categories")
      category_list= cur.fetchall()
      
      #  Footer
      cur.execute("select * from footers")
      footer_list= cur.fetchall(); 
      
   return render_template("items.html", 
                          category_list = category_list,
                          item_detail = item_detail,
                        #   related_items = related_items,
                        #   searched_items = searched_items,
                          footer_list=footer_list)


@app.route("/payment")
def payment():
   return render_template("payment.html")

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
   print(form.validate_on_submit())
   
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
         return redirect(url_for('success'))
         
         
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
   
   
@app.route("/success")
def success():
   return render_template("success.html")
   

if __name__ == '__main__':
   app.run(debug = True)