from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql
from forms import RegisterForm, RegisteredForm
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
import pandas as pd

app = Flask(__name__)
app.secret_key = 'random string'

# Database Link
DB_Path = 'EC.db'

# Login Manager
login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, UserID, FirstName, LastName, Phone, Email):
         self.UserID = UserID
         self.FirstName = FirstName
         self.LastName = LastName
         self.Phone = Phone
         self.Email = Email
         self.authenticated = False
    def is_active(self):
         return self.is_active()
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
   con = sql.connect(DB_Path)
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
   
   
   all_items = []
   
   with sql.connect("EC.db") as con:
      cur = con.cursor()
      
      # 0. All Items
      cur.execute("select * from items")
      item_list= cur.fetchall(); 
      all_items.append(item_list)
      
      # 1. Categories
      cur.execute("select * from categories")
      category_list= cur.fetchall(); 
      all_items.append(category_list)
      
      # 2. Recently Viewed
      # -->From Wish List or Log(Update Later)
      if str(current_user.get_id()) != 'None':
      # if True:
         try:
            cur.execute("select * from logs where UserID=?", (str(current_user.get_id())))
         except:
            cur.execute("select * from logs") 
      
         recently_viewed_list= cur.fetchall(); 
         all_items.append(recently_viewed_list)
      
      else:
         cur.execute("select * from orders")
         order_list= cur.fetchall(); 
         all_items.append(order_list)
   
      
      # 3. Recommended
      cur.execute("select * from items where Tag = 'Recommended'")
      recommended_list= cur.fetchall(); 
      all_items.append(recommended_list)
      
      # 4.Buy again
      if str(current_user.get_id()) != 'None':
         try:
            cur.execute("select * from orders where UserID=?", (str(current_user.get_id())))   # if user has an order history
         except:
            cur.execute("select * from orders")    # if user doesn't have an order history
         # cur.execute("select * from orders where UserID=?", (str(current_user.get_id())))
         # cur.execute("select * from orders where UserID=?", (str(1)))
         # cur.execute("select * from orders")
         order_list= cur.fetchall(); 
         all_items.append(order_list)
      else:
         cur.execute("select * from orders")
         order_list= cur.fetchall(); 
         all_items.append(order_list)
      
      # 5. Great Deal
      cur.execute("select * from items where Tag = 'Deal'")
      deal_list= cur.fetchall(); 
      all_items.append(deal_list)
      
      # 6. Popular now
      cur.execute("select * from orders")
      popular_list= cur.fetchall(); 
      all_items.append(popular_list)
      
      # 7. Pick up
      cur.execute("select * from items where Tag = 'Pickup'")
      deal_list= cur.fetchall(); 
      all_items.append(deal_list)
   
      # 8. Fitness
      cur.execute("select * from items where Tag = 'Fitness'")
      fitness_list= cur.fetchall(); 
      all_items.append(fitness_list)
      
      # 9. Promotion
      cur.execute("select * from items where Tag = 'Promotion'")
      promotion_list= cur.fetchall(); 
      all_items.append(promotion_list)
      
      # 10. For you
      if str(current_user.get_id()) != 'None':
         df = pd.DataFrame(order_list)
         for_you_list = df[6].value_counts().keys()[0]

         cur.execute("select * from items where Category = ?", (for_you_list,))
         for_you_list= cur.fetchall(); 
         all_items.append(for_you_list)
      else:
         cur.execute("select * from items")
         for_you_list = cur.fetchall(); 
         all_items.append(for_you_list)
         
      # 11. Footer
      cur.execute("select * from footers")
      footer_list= cur.fetchall(); 
      all_items.append(footer_list)
         
       
   return render_template("main.html", current_user = current_user, all_items = all_items, footer_list=footer_list)


# @app.route("/user_main/<user_id>")
# def user_main(user_id):
#    item_list = []
#    category_list = []
   
#    with sql.connect("EC.db") as con:
#       cur = con.cursor()
#       cur.execute("select * from items")
#       item_list= cur.fetchall(); 
      
#       cur.execute("select * from categories")
#       category_list= cur.fetchall(); 
      
#       cur.execute("select * from users where UserID = '%s'" %user_id)
#       user_info= cur.fetchall(); 
      
#       return render_template("main.html", item_list = item_list, category_list = category_list, user_info = user_info)

@app.route("/signin")
def signin():
   return render_template("signin.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))

@app.route("/item")
def item():
   all_items = []
   
   with sql.connect("EC.db") as con:
      cur = con.cursor()
      
      # 0. All Items
      cur.execute("select * from items")
      item_list= cur.fetchall(); 
      all_items.append(item_list)
      
      # 1. Categories
      cur.execute("select * from categories")
      category_list= cur.fetchall(); 
      all_items.append(category_list)
      
   return render_template("item.html", all_items = all_items)

@app.route("/items")
def items():
   all_items = []
   
   with sql.connect("EC.db") as con:
      cur = con.cursor()
      
      # 0. All Items
      cur.execute("select * from items")
      item_list= cur.fetchall(); 
      all_items.append(item_list)
      
      # 1. Categories
      cur.execute("select * from categories")
      category_list= cur.fetchall(); 
      all_items.append(category_list)
      
   return render_template("items.html", all_items = all_items)


@app.route("/payment")
def payment():
   all_items = []
   
   with sql.connect("EC.db") as con:
      cur = con.cursor()
      
      # 0. All Items
      cur.execute("select * from items")
      item_list= cur.fetchall(); 
      all_items.append(item_list)
      
      # 1. Categories
      cur.execute("select * from categories")
      category_list= cur.fetchall(); 
      all_items.append(category_list)
      
   return render_template("payment.html", all_items=all_items)

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


@app.route('/add_account', methods=['GET', 'POST'])
def add_account(): 
   item_list = []
   category_list = []
   
   with sql.connect("EC.db") as con:
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
   all_items = []
   
   form = RegisterForm()
   registered_form = RegisteredForm()
   
   with sql.connect("EC.db") as con:
      con.row_factory = sql.Row 
      cur = con.cursor() 
   
      # 0. All Items
      cur.execute("select * from items")
      item_list= cur.fetchall()
      all_items.append(item_list)
      
      # 1. Categories
      cur.execute("select * from categories")
      category_list= cur.fetchall() 
      all_items.append(category_list)
   
      # 2. Accounts
      cur.execute("select * from users where UserID=?",(UserID,)) 
      account_list= cur.fetchall()
      all_items.append(account_list)
      
      # 3. Orders
      cur.execute("select * from orders where UserID=?",(UserID,)) 
      order_list= cur.fetchall()
      all_items.append(order_list) 
      
      # 4. Wishes
      cur.execute("select * from items where Wishers=?",(UserID,)) 
      wisher_list= cur.fetchall(); 
      all_items.append(wisher_list)
      
      # 5. Footer
      cur.execute("select * from footers")
      footer_list= cur.fetchall(); 
      
   return render_template("account.html", all_items= all_items, form = form, registered_form = registered_form, footer_list=footer_list)


@app.route('/signin_user', methods=['GET', 'POST'])
def signin_user():
   Email = request.form['Email']
   
   with sql.connect("EC.db") as con:
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
      with sql.connect("EC.db") as con: 
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