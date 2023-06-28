from flask import Flask, render_template, request, redirect, url_for, flash, session, app
import sqlite3 as sql
from forms import RegisterForm, RegisterGuestForm, RegisteredForm
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user
import pandas as pd
from datetime import date, timedelta
from shuffle import shuffle_table
from db_handler import db_select, db_select_where, db_select_where_in, db_select_distinct_where, db_select_where_cols, db_select_where_order_by, db_insert_logs, db_insert_carts, db_update_carts, db_update_payment_info, db_insert_users, db_delete, db_insert_orders, check_password, db_search_item, db_insert_wishes, db_drop_duplicates


app = Flask(__name__)
app.secret_key = 'random string'


################################################################################################
# Session
################################################################################################
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)


################################################################################################
# Class
################################################################################################
class User(UserMixin):
   def __init__(self, UserID, FirstName, LastName, Address, Phone, Email, CardNumber, PayLater, UserType):
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
   def is_anonymous(self):
      return False
   def is_authenticated(self):
      return self.authenticated
   def is_active(self):
      return True
   def get_id(self):
      return self.UserID
   def get_user_type(self):
      return self.UserType
      

################################################################################################
# Login manager
################################################################################################
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(UserID):
   user_info = db_select_where("*", "users", "UserID", UserID)
   # if user_info is None:
   if user_info == []:
      return None
   else:
      return User(int(user_info[0][0]), user_info[0][1], user_info[0][2], user_info[0][3], user_info[0][4], user_info[0][5], user_info[0][6], user_info[0][7], user_info[0][8])


################################################################################################
# Main
################################################################################################
@app.route("/")
def main():
   # 0. Current user
   current_user_id = str(current_user.get_id())
   
   # 1. Categories
   category_list = db_select("*","categories")
   
   # 2. Recently Viewed
   user_log_count = 0
   if str(current_user.get_id()) != 'None':
      try:
         recently_viewed_list = db_select_where("*","logs", "UserID", current_user_id)
         recently_viewed_list = db_drop_duplicates("logs", recently_viewed_list, "LogID", "DSEC") # Drop duplicates
         user_log_count = len(recently_viewed_list)
   
      except:
         recently_viewed_list=[]
         user_log_count = len(recently_viewed_list)
      
   else:
      recently_viewed_list = db_select_where("*","items", "Category", "Electric device")
    
   # 3. Recommended
   recommended_list = db_select_where("*","items", "Tag", "Recommended")     
   

   # 4.Buy again
   user_order_count = 0
   if current_user_id != 'None':
      try:                                                                             # if user has an order history
         order_list = db_select_where("*","orders", "UserID", current_user_id)     
         order_list = db_drop_duplicates("orders", order_list, "OrderID", "DSEC")      # Drop duplicates
         order_list = shuffle_table(order_list)                                        # Shuffle the table rows
         user_order_count = len(order_list)
         
      except:
         order_list=[]
         user_order_count = len(order_list)
      
   else:
      order_list = db_select_where("*","items", "Tag", "Health & Personal Care")
   
   
   # 5. Great Deal
   deal_list = db_select_where("*","items", "Tag", "Deal")
   deal_list = shuffle_table(deal_list)   # Shuffle the table rows
   
   
   # 6. Popular now
   popular_list = db_select("*","orders")
   
   df = pd.DataFrame(popular_list)
   top_four_order_list = df[5].value_counts().keys()[0:5]      # Top 4 order items
   top_four_order_list = top_four_order_list.tolist()
   
   popular_list = db_select_where_in("*","items", "ItemName", top_four_order_list)
   popular_list = shuffle_table(popular_list)   # Shuffle the table rows
   
   
   # 7. Pick up
   pickup_list = db_select_where("*","items", "Tag", "Pickup")
   
   # 8. Fitness
   fitness_list = db_select_where("*","items", "Tag", "Fitness")
   
   # 9. Promotion
   promotion_list = db_select_where("*","items", "Tag", "Promotion")
   
   # 10. For you
   if str(current_user.get_id()) != 'None' and order_list != []:
      df = pd.DataFrame(order_list)
      for_you_list = df[6].value_counts().keys()[0]   #Find the top category user ordered

      for_you_list = db_select_where("*","items", "Category", for_you_list)
      for_you_list = shuffle_table(for_you_list)    # Shuffle the table rows
      
   else:
      for_you_list = db_select("*","items")
      for_you_list = shuffle_table(for_you_list)    # Shuffle the table rows
   
   
   # 11. Footer
   footer_list = db_select("*","footers")
   
   # 12. Health & Personal Care
   health_list = db_select_where("*","items", "Tag", 'Health & Personal Care')
   
   # 13. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]
   
         
       
   return render_template("main.html", 
                          current_user_id = current_user_id, 
                          category_list = category_list, 
                          recently_viewed_list = recently_viewed_list, 
                          user_log_count = user_log_count,
                          recommended_list = recommended_list, 
                          order_list = order_list, 
                          user_order_count = user_order_count,
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


################################################################################################
# Sign in
################################################################################################
@app.route("/signin")
def signin():
   return render_template("signin.html")

@app.route('/signin_account', methods=['POST'])
def signin_account():
   if request.method == 'POST':   
      entered_email = request.form['Email']
      entered_password = request.form['Password']
      
      try:
         registered_user = db_select_where("*","users", "Email", entered_email)
         registered_password = registered_user[0][9]
         
      except:
         registered_user = "None"
      
         
      if registered_user != "None":
         if check_password(registered_password,entered_password):
            registered_user = load_user(registered_user[0][0])
            login_user(registered_user)
            return redirect(url_for('success', request="signin"))
         
         else:
            flash('Your password is wrong')
            return redirect(url_for('signin')) 
      else:
         flash('Your email is not registered')
         return redirect(url_for('signin')) 
      

################################################################################################
# Log out
################################################################################################
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))


################################################################################################
# Item
################################################################################################
@app.route('/item/<string:Category>', methods = ['GET']) 
def item_category(Category):
   
   # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   # 1. item
   item_list = db_select_where("*","items", "Category", Category)

   # 2. Categories
   category_list =  db_select("*","categories")
   
   # 3. Footer
   footer_list =  db_select("*","footers")
   
   # 4. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]


   return render_template("item.html", 
                          item_list = item_list,
                          category_list = category_list,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num,
                          current_user_id = current_user_id,
                          data_source = "items"
                          )

@app.route('/item/tag=<string:Tag>', methods = ['GET']) 
def item_tag(Tag):
   
   # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   # 1. item
   item_list = db_select_where("*","items", "Tag", Tag)
   

   # 2. Categories
   category_list =  db_select("*","categories")
   
   # 3. Footer
   footer_list =  db_select("*","footers")
   
   # 4. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]
      
   return render_template("item.html", 
                          item_list = item_list,
                          category_list = category_list,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num,
                          data_source = "items"
                          )

@app.route('/item/popular_now', methods = ['GET']) 
def item_popular_now():
   # 0. User ID 
   current_user_id = str(current_user.get_id())
       
   # 1. Ordered items
   popular_list = db_select("*","orders")
   popular_list = db_drop_duplicates("orders", popular_list, "Date", "DSEC")  # Drop duplicates

   # 2. Categories
   category_list =  db_select("*","categories")
   
   # 3. Footer
   footer_list =  db_select("*","footers")

   # 4. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]
   
      
   return render_template("item.html", 
                          item_list = popular_list,
                          category_list = category_list,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num,
                          data_source = "popular_now"
                          )

@app.route('/item/recently_viewed', methods = ['GET']) 
def item_recently_viewed():
   
   # 0. User ID 
   current_user_id =  str(current_user.get_id())
   
   # 1. Searched items
   recently_viewed_list = db_select_where("*","logs", "UserID", current_user_id)
   recently_viewed_list = db_drop_duplicates("logs", recently_viewed_list, "LogID", "DSEC")        # Drop duplicates

   # 2. Categories
   category_list =  db_select("*","categories")
   
   # 3. Footer
   footer_list =  db_select("*","footers")
   
   # 4. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]
   
      
   return render_template("item.html", 
                          item_list = recently_viewed_list,
                          category_list = category_list,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num,
                          current_user_id = current_user_id,
                          data_source = "recently_viewed"
                          )

@app.route('/item/buy_again', methods = ['GET']) 
def item_buy_again():
   
   # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   # 1. Ordered items
   ordered_items = db_select_where("*","orders", "UserID", current_user_id)
   ordered_items = db_drop_duplicates("orders", ordered_items, "Date", "DSEC")        # Drop duplicates
      
   # 2. Categories
   category_list =  db_select("*","categories")
   
   # 3. Footer
   footer_list =  db_select("*","footers")

   # 4. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]
         
      
   return render_template("item.html", 
                          item_list = ordered_items,
                          category_list = category_list,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num,
                          data_source = "buy_again"
                          )


##################
# Rating Sort
@app.route('/item/<string:Category>_rating=<string:Rating>', methods = ['GET']) 
def item_user_rating(Category, Rating):
   # 0. User ID 
   current_user_id = str(current_user.get_id())
       
   # 1. item
   item_list = db_select_where_cols("*","items", "Category", Category, "Rating", Rating)
   if(item_list != []):
      item_list = db_select_where_cols("*","items", "Category", Category, "Rating", Rating)
   else:
      flash("No products found")
      return redirect(url_for("item_category", Category = Category))
      

   # 2. Categories
   category_list =  db_select("*","categories")
   
   # 3. Footer
   footer_list =  db_select("*","footers")

   # 4. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]

      
   return render_template("item.html", 
                          item_list = item_list,
                          category_list = category_list,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num,
                          data_source = "items"
                          )
 
@app.route('/item/popular_now_rating=<string:Rating>', methods = ['GET']) 
def item_popular_now_rating(Rating):
   # 0. User ID 
   current_user_id = str(current_user.get_id())
       
   # 1. Popular items
   popular_list = db_select_where("*","orders", "Rating", Rating)
   popular_list = db_drop_duplicates("orders", popular_list, "OrderID", "DSEC")        # Drop duplicates

   # 2. Categories
   category_list =  db_select("*","categories")
   
   # 3. Footer
   footer_list =  db_select("*","footers")

   # 4. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]
      
      
   return render_template("item.html", 
                          item_list = popular_list,
                          category_list = category_list,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num,
                          data_source = "popular_now"
                          )
   
@app.route('/item/recently_viewed_rating=<string:Rating>', methods = ['GET']) 
def item_recently_viewed_rating(Rating):
   # 0. User ID 
   current_user_id = str(current_user.get_id())
       
   # 1. Searched items
   searched_list = db_select_where_cols("*","logs", "UserID", current_user_id, "Rating", Rating)
   if(searched_list != []):
      searched_list = db_select_where_cols("*","logs", "UserID", current_user_id, "Rating", Rating)
   else:
      flash("No products found")
      return redirect(url_for("item_recently_viewed"))
   
   searched_list = db_drop_duplicates("logs", searched_list, "LogID", "DSEC")        # Drop duplicates

   # 2. Categories
   category_list =  db_select("*","categories")
   
   # 3. Footer
   footer_list =  db_select("*","footers")

   # 4. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]
      
      
   return render_template("item.html", 
                          item_list = searched_list,
                          category_list = category_list,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num,
                          data_source = "recently_viewed"
                          )
 
@app.route('/item/buy_again_rating=<string:Rating>', methods = ['GET']) 
def item_buy_again_rating(Rating):
   # 0. User ID 
   current_user_id = str(current_user.get_id())
       
   # 1. Ordered items
   order_list = db_select_where_cols("*","orders", "UserID", current_user_id, "Rating", Rating)
   if(order_list != []):
      order_list = db_select_where_cols("*","orders", "UserID", current_user_id, "Rating", Rating)
   else:
      flash("No products found")
      return redirect(url_for("item_buy_again"))
   
   order_list = db_drop_duplicates("orders", order_list, "Date", "DSEC")        # Drop duplicates

   # 2. Categories
   category_list =  db_select("*","categories")
   
   # 3. Footer
   footer_list =  db_select("*","footers")

   # 4. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]
      
      
   return render_template("item.html", 
                          item_list = order_list,
                          category_list = category_list,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num,
                          data_source = "buy_again"
                          )
  
 
##################
# Price Sort
@app.route('/item/<string:Category>_price=<string:Sort>', methods = ['GET']) 
def item_price_order(Category, Sort):
  # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   # 1. item
   if Sort == 'ASC':
      item_list = db_select_where_order_by("*","items", "Category", Category, "Price", Sort)
   else:
      item_list = db_select_where_order_by("*","items", "Category", Category, "Price", Sort)

   # 2. Categories
   category_list =  db_select("*","categories")
   
   # 3. Footer
   footer_list =  db_select("*","footers")

   # 4. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]
      

      
   return render_template("item.html", 
                          item_list = item_list,
                          category_list = category_list,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num,
                          data_source = "items"
                          )
   
@app.route('/item/popular_now_price=<string:Sort>', methods = ['GET']) 
def item_popular_now_price_order(Sort):
  # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   # 1. item
   item_list = db_select("*","orders")
   if Sort == 'ASC':
      item_list = db_drop_duplicates("orders", item_list, "Price", "ASC")        # Drop duplicates
      
   else:
      item_list = db_drop_duplicates("orders", item_list, "Price", "DESC")        # Drop duplicates
      

   # 2. Categories
   category_list =  db_select("*","categories")
   
   # 3. Footer
   footer_list =  db_select("*","footers")

   # 4. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]
      

      
   return render_template("item.html", 
                          item_list = item_list,
                          category_list = category_list,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num,
                          data_source = "popular_now"
                          )
  
@app.route('/item/recently_viewed_price=<string:Sort>', methods = ['GET']) 
def item_recently_viewed_price_order(Sort):
  # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   # 1. item
   item_list = db_select_where("*","logs", "UserID", current_user_id)
   if Sort == 'ASC':
      item_list = db_drop_duplicates("logs", item_list, "Price", "ASC")        # Drop duplicates
      
   else:
      item_list = db_drop_duplicates("logs", item_list, "Price", "DESC")        # Drop duplicates

   # 2. Categories
   category_list =  db_select("*","categories")
   
   # 3. Footer
   footer_list =  db_select("*","footers")

   # 4. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]
      

      
   return render_template("item.html", 
                          item_list = item_list,
                          category_list = category_list,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num,
                          data_source = "recently_viewed"
                          )
 
@app.route('/item/buy_again_price=<string:Sort>', methods = ['GET']) 
def item_buy_again_price_order(Sort):
  # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   # 1. item
   item_list = db_select_where("*","orders", "UserID", current_user_id)
   if Sort == 'ASC':
      item_list = db_drop_duplicates("orders", item_list, "Price", "ASC")        # Drop duplicates
      
   else:
      item_list = db_drop_duplicates("orders", item_list, "Price", "DESC")        # Drop duplicates

   # 2. Categories
   category_list =  db_select("*","categories")
   
   # 3. Footer
   footer_list =  db_select("*","footers")

   # 4. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]
      

      
   return render_template("item.html", 
                          item_list = item_list,
                          category_list = category_list,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num,
                          data_source = "buy_again"
                          )
  

################################################################################################
# Items Detail
################################################################################################
@app.route('/items/<string:ItemID>', methods = ['GET']) 
def items(ItemID):
  # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   # 1. item detail
   item_detail = db_select_where("*","items", "ItemID", ItemID)
   another_detail_list = item_detail[0][10].split("|")

   # 2. Related Items
   related_items = db_select_where("*","items", "Category", item_detail[0][2])   
   related_items = shuffle_table(related_items)    # Shuffle the table rows
   
   # 3. Searched items
   searched_items_cols = db_select_distinct_where("ItemID","logs", "Category", item_detail[0][2])    
   
   list = []                        # Change the list format  from [(1,), (2,), (3,)] to (1,2,3)
   for item in searched_items_cols:  
      list.append(item[0])          
   
   searched_items = db_select_where_in("*","items", "ItemID", list)
   searched_items = shuffle_table(searched_items)    # Shuffle the table rows  

   # 4. Categories
   category_list =  db_select("*","categories")
   
   # 5. Footer
   footer_list =  db_select("*","footers")

   # 6. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
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
      

   # 8. Record useraction to Log
   if current_user.get_id():
      db_insert_logs(ItemID, current_user_id, current_user.FirstName)
   else:
      db_insert_logs(ItemID, "", "")
   
   
   # 9. Reviews
   try:
      review_list= db_select_where("*","orders", "ItemID", ItemID)
      df = pd.DataFrame(review_list)
      df.columns = ["OrderID", "Date", "UserID", "UserName", "ItemID", "ItemName", "Category", "Price", "Detail","Rating", "Reviews", "ImageURL", "ItemCount", "ReviewTitle"]
      review_count = len(df["Rating"])
      rating_count_list = []
      for i in range(5):
         rating_count_list.append(len(df[df["Rating"] == i+1]))
      
      rating_ratio_list = []
      for i in range(5):
         rating_ratio = round(rating_count_list[i]/review_count * 100 , 1)
         rating_ratio_list.append(rating_ratio)
      
      rating_ave = df["Rating"].mean()
   except:
      review_list = False
      rating_ratio_list = 0
      rating_ave = 0
   

   return render_template("items.html", 
                          current_user_id = current_user_id,
                          category_list = category_list,
                          item_detail = item_detail,
                          related_items = related_items,
                          searched_items = searched_items,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num,
                          delivery_date = delivery_date,
                          another_detail_list = another_detail_list,
                          review_list = review_list,
                          rating_ratio_list = rating_ratio_list,
                          rating_ave = rating_ave,
                          )

@app.route('/pay_now/<string:ItemID>', methods=['POST'])
def pay_now(ItemID): 
   item_count = request.form['quantity']
   
   # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   # 1. User Details
   user_list = db_select_where("*","users", "UserID", current_user_id)

   
   # 2. Categories
   category_list =  db_select("*","categories")
   
   # 3. Footer
   footer_list =  db_select("*","footers")

   # 4. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]
   
   # 5. Total Cost
   total_cost = 0
   for item in cart_list:
      total_cost += float(item[7]) 

   # 6. Date
   today = date.today()
   delivery_date = today + timedelta(days=7)
   month = delivery_date.strftime("%b")
   day = delivery_date.strftime("%d")
   year = delivery_date.strftime("%Y")
   weekday = delivery_date.strftime("%a")
   
   delivery_date = f"{month}, {day}, {year} ({weekday})"
   
   # 7. Add to cart
   if current_user.get_id():
      db_insert_carts(ItemID, current_user_id, current_user.FirstName, item_count)
   else:
      db_insert_carts(ItemID, "", "", item_count)


   return redirect(url_for('payment', UserID = current_user_id))
   

################################################################################################
# Payment
################################################################################################
@app.route("/payment", methods=['GET'])
def payment():
   registered_form = RegisteredForm()

   # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   # 1. User Details
   user_list = db_select_where("*","users", "UserID", current_user_id)
   try:
      card_num = user_list[0][6].split('-')[2]
   except:
      card_num = ""
   
   # 2. Categories
   category_list =  db_select("*","categories")
   
   # 3. Footer
   footer_list =  db_select("*","footers")

   # 4. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]


   # 3. Total Cost
   total_cost = 0
   for item in cart_list:
      total_cost += float(item[7]) * float(item[12])  # price * item count
         
   # 6. Date
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
                          delivery_date = delivery_date,
                          current_user_id = current_user_id,
                          footer_list = footer_list,
                          registered_form = registered_form,
                          card_num = card_num
                          )


@app.route('/payment/update_cart/<string:ItemID>', methods=['POST'])
def update_cart(ItemID): 
   item_count = request.form['quantity']
   db_update_carts(ItemID, item_count)
      
   return redirect(url_for('payment', UserID= current_user.get_id()))


@app.route('/payment/delete_cart/<string:ItemID>', methods=['POST'])
def delete_cart(ItemID): 
   db_delete("carts", "CartID", ItemID)
   
   return redirect(url_for('payment', UserID= current_user.get_id()))
 

@app.route('/update_payment_info', methods=['POST'])
def update_payment():
   form = RegisteredForm()
   
   # 0. User ID 
   current_user_id = str(current_user.get_id())

   if form.validate_on_submit(): 
      db_update_payment_info(form, current_user_id)
      return redirect(url_for('payment',UserID=current_user.UserID)) 
      
   else:
      return redirect(url_for('payment',UserID=current_user.UserID)) 


################################################################################################
# Registration
################################################################################################
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


@app.route('/add_guest', methods=['POST'])
def add_guest(): 
   form = RegisterGuestForm()
   
   # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   # 1. Item list
   item_list = db_select("*","items")
   
   # 2. Categories
   category_list =  db_select("*","categories")
   

   if form.validate_on_submit(): 
      # Check existing email
      entered_email = form.email.data
      
      try:
         existing_email = db_select_where("Email", "users", "Email", entered_email)
         if entered_email in existing_email[0]:
            flash("Your email is already in use. Please sign in instead")
            return render_template('register_guest.html', form = form)
         
      except:
         db_insert_users(form, "Guest")
         
         new_user = db_select_where("*", "users", "Email", form.email.data)
         new_user = load_user(new_user[0][0])
         login_user(new_user)
         print(f"User ID: {new_user.UserType}")

         return redirect(url_for('success',request = "guest"))
   else:
      return render_template('register_guest.html', form = form)    
   

@app.route('/add_account', methods=['POST'])
def add_account(): 
   form = RegisterForm()
   
   # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   # 1. Item list
   item_list = db_select("*","items")
   
   # 2. Categories
   category_list =  db_select("*","categories")
   
   if form.validate_on_submit(): 
      
      # Check existing email
      entered_email = form.email.data
      try:
         existing_email = db_select_where("Email", "users", "Email", entered_email)
         if entered_email in existing_email[0]:
            flash("Your email is already in use. Please sign in instead")
            return render_template('register.html', form = form)
         
      except:
         db_insert_users(form, "")    
         new_user = db_select_where("*", "users", "Email", form.email.data)
         new_user = load_user(new_user[0][0])
         login_user(new_user)

         return redirect(url_for('success',request = "add_account"))
   else:
      return render_template('register.html', form = form) 
   

################################################################################################
# Account
################################################################################################
@app.route('/account/', methods = ['GET']) 
def account():
   
   form = RegisterForm()
   registered_form = RegisteredForm()

   # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   # 1. Accounts
   account_list = db_select_where("*", "users", "UserID", current_user_id)
   try:
      card_num = account_list[0][6].split('-')[2]
   except:
      card_num = ""
   
   # 2. Categories
   category_list =  db_select("*","categories")
    
   # 3. Orders
   order_list = db_select_where("*", "orders", "UserID", current_user_id)
   
   if str(current_user.get_id()) != 'None' and order_list != []:
      order_list = db_drop_duplicates("orders", order_list, "Date", "DSEC")  # Drop duplicates
   else:
      order_list = []
   
   
   # 4. Wishes
   wisher_list = db_select_where("*", "wishes", "UserID", current_user_id)

   if str(current_user.get_id()) != 'None' and wisher_list != []:
      wisher_list = db_drop_duplicates("wishes", wisher_list, "Date", "DSEC")  # Drop duplicates
   else:
      wisher_list = []


   # 3. Footer
   footer_list =  db_select("*","footers")
   
   # 4. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]
      
   return render_template("account.html", 
                          category_list = category_list,
                          account_list = account_list, 
                          order_list = order_list,
                          wisher_list = wisher_list,
                          form = form, 
                          registered_form = registered_form, 
                          footer_list=footer_list,
                          card_num = card_num,
                          cart_list_num = cart_list_num
                          )

@app.route('/update_account', methods=['POST'])
def update_account():
   form = RegisteredForm()
   
   # 0. User ID 
   current_user_id = str(current_user.get_id())

   if form.validate_on_submit(): 
      db_update_payment_info(form, current_user_id)
      return redirect(url_for('account', UserID = current_user_id)) 
      
   else:
      return redirect(url_for('account',UserID=current_user.UserID)) 


################################################################################################
# Cart
################################################################################################
@app.route('/add_cart/<string:ItemID>', methods=['POST'])
def add_cart(ItemID): 
   item_count = request.form['quantity']
   
   # # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   # 1. Items
   item_list = db_select_where("*", "items", "ItemID", ItemID)

   # 2. Categories
   category_list =  db_select("*","categories")
    

   # 3. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]

   # 4. Total Cost
   total_cost = 0
   for item in cart_list:
      total_cost += float(item[7])
   
   # 5. User Details
   user_list = db_select_where("*", "users", "UserID", current_user_id)

   # 6. Date
   today = date.today()
   delivery_date = today + timedelta(days=7)
   month = delivery_date.strftime("%b")
   day = delivery_date.strftime("%d")
   year = delivery_date.strftime("%Y")
   weekday = delivery_date.strftime("%a")
   
   delivery_date = f"{month}, {day}, {year} ({weekday})"
   
   
   db_insert_carts(ItemID, current_user_id, current_user.FirstName, item_count)

   return redirect(url_for('success', request= "add_cart"))


################################################################################################
# Wishlist
################################################################################################
@app.route('/add_wishlist/<string:ItemID>', methods=['POST'])
def add_wishlist(ItemID): 
   
   # # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   # 1. Items
   item_list = db_select_where("*", "items", "ItemID", ItemID)
   
   db_insert_wishes(item_list, current_user_id, current_user.FirstName)
   return redirect(url_for('success', request= "add_wishes"))


################################################################################################
# Success
################################################################################################
@app.route("/success/<string:request>")
def success(request):
   
   # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   if request == "order":
       
      title = "Ordered successfully"
      detail = "Thank you for placing your order!"
         
      # Check address and card number
      user_info = db_select_where("*", "users", "UserID", current_user_id)
      address = str(user_info[0][3])
      card_number = str(user_info[0][6])
      
      if address != "" and card_number != "":
         if current_user.UserType == "Guest":
            # Delete cart items
            delete_list = db_select_where("CartID", "carts", "UserID", current_user_id)
            for num in delete_list:
               db_delete("carts", "CartID", num[0])
               
            db_delete("users", "UserType", "Guest")
            title = "Ordered successfully"
            detail = "Thank you for placing your order!"
            
         else:
            # Records orders 
            cart_list = db_select_where("*", "carts", "UserID", current_user_id)
            
            db_insert_orders(cart_list, current_user_id, current_user.FirstName)
            
            # Delete cart items
            delete_list = db_select_where("CartID", "carts", "UserID", current_user_id)

            for num in delete_list:
               db_delete("carts", "CartID", num[0])
            
      else:
         flash("Please fill out address and card number")
         return redirect(url_for("payment", UserID = current_user.get_id()))
            
   elif request == "signin":
      title = "Sign in successfully"
      detail = "Welcome to " + current_user.FirstName + " " + current_user.LastName
      
   elif request == "add_cart" or request == "add_wishes":
      title = "Added item successfully"
      detail = "Keep enjoy your shopping!"
   
   elif request == "guest":
      title = "Temporaly your information is recorded"
      detail = "Enjoy your shopping!"
      
   elif request == "add_account":
      title = "Registered successfully"
      detail = "Welcome to " + current_user.FirstName + " " + current_user.LastName
   
   elif request == "search_fail":
      title = "Item not found"
      detail = "Try other search key words"
      
      
      
   return render_template("success.html", title=title, detail=detail) 


################################################################################################
# Orders
################################################################################################
@app.route("/orders")
def orders_user():
   
   # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   # 1. Categories
   category_list =  db_select("*","categories")
    
   # 2. Orders
   # order_list = db_select_where("*", "orders", "UserID", current_user_id)
   order_list = db_select_where_order_by("*", "orders", "UserID", current_user_id, "Date", "DESC")
   

   # 3. Footer
   footer_list =  db_select("*","footers")
   
   # 4. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]
      
   return render_template("orders.html",
                          category_list = category_list,
                          order_list = order_list,
                          footer_list = footer_list,
                          current_user_id = current_user_id,
                          cart_list_num = cart_list_num
                          )


################################################################################################
# Search
################################################################################################
@app.route('/search', methods = ['POST']) 
def search():
   search_item = request.form["search"]
   
   # 0. User ID 
   current_user_id = str(current_user.get_id())
   
   # 1. item
   if db_search_item(search_item) == []:
      flash("Searched item is not found")
      return redirect(url_for('main'))
   else:
      item_list = db_search_item(search_item)

   # 2. Categories
   category_list =  db_select("*","categories")
   
   # 3. Footer
   footer_list =  db_select("*","footers")
   
   # 4. Cart 
   cart_list = db_select_where("*","carts", "UserID", current_user_id)
   cart_list_num = 0
   for item in cart_list:
      cart_list_num += item[12]


   return render_template("item.html", 
                          item_list = item_list,
                          category_list = category_list,
                          footer_list=footer_list,
                          cart_list = cart_list,
                          cart_list_num = cart_list_num,
                          current_user_id = current_user_id,
                          data_source = "items"
                          )


if __name__ == '__main__':
   app.run(debug = True)