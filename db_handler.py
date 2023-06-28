import sqlite3 as sql
from datetime import date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import random
import pandas as pd

################################################################################################
# DB Path
################################################################################################
DB_path = 'EC.db'

################################################################################################
# Functions
################################################################################################
def db_select(col, table):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT {col} FROM {table}") 
        list= cur.fetchall(); 
        
        return list

def db_select_order_by(col, table, order_col, keyword):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT {col} FROM {table} ORDER BY {order_col} {keyword}")
        list = cur.fetchall(); 
        
        return list 

def db_select_where(col, table, col_target, col_value):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT {col} FROM {table} WHERE {col_target} = '{col_value}'")
        list= cur.fetchall(); 
        
        return list

def db_select_where_in(col, table, col_target, col_values):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
    
        question_list = []
        value_list = []
        for item in col_values:
            question_list.append("?")
            value_list.append(item)
            
            
        q_tuple = ",".join(question_list)          # ex) ?,?,?
        value_tuple = tuple(value_list)           # ex) (1,2,3)
        
        cur.execute(f"SELECT {col} FROM {table} WHERE {col_target} IN ({q_tuple})",value_tuple) 
        list= cur.fetchall(); 
        
        return list

def db_select_distinct_where(col, table, col_target, col_value):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT distinct {col} FROM {table} WHERE {col_target} = '{col_value}'")
        list= cur.fetchall(); 
        
        return list
    
def db_select_where_cols(col, table, col_target_1, col_value_1, col_target_2, col_value_2):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT {col} FROM {table} WHERE {col_target_1} = '{col_value_1}' AND {col_target_2} = '{col_value_2}'")
        list= cur.fetchall(); 
        
        return list  
    
def db_select_where_order_by(col, table, col_target_1, col_value_1, order_col, keyword):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT {col} FROM {table} WHERE {col_target_1} = '{col_value_1}' ORDER BY {order_col} {keyword}")
        list = cur.fetchall(); 
        
        return list  

def db_insert_logs(item_id, user_id, user_name):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM items WHERE ItemID = '{item_id}'")
        list= cur.fetchall(); 
        
        Date = date.today()
        UserID = user_id
        ItemID = list[0][0]
        ItemName = list[0][1]
        Category = list[0][2]
        Price = list[0][3]
        Detail = list[0][4]
        Rating = list[0][5]
        Reviews = list[0][6]
        ImageURL = list[0][7]    
        
        if user_name:
            UserName = user_name
        else:
            UserName = "Guest"

        cur.execute("INSERT INTO logs (Date, UserID, UserName, ItemID, ItemName, Category, Price, Detail, Rating, Reviews, ImageURL) VALUES (?,?,?,?,?,?,?,?,?,?,?)",(Date, UserID, UserName, ItemID, ItemName, Category, Price, Detail, Rating, Reviews, ImageURL))
   
def db_insert_carts(item_id, user_id, user_name, item_count):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM items WHERE ItemID = '{item_id}'")
        list= cur.fetchall(); 
        
        Date = date.today()
        UserID = user_id
        ItemID = list[0][0]
        ItemName = list[0][1]
        Category = list[0][2]
        Price = list[0][3]
        Detail = list[0][4]
        Rating = list[0][5]
        Reviews = list[0][6]
        ImageURL = list[0][7]  
        ItemCount = item_count  
        
        if user_name:
            UserName = user_name
        else:
            UserName = "Guest"

        cur.execute("INSERT INTO carts (Date, UserID, UserName, ItemID, ItemName, Category, Price, Detail, Rating, Reviews, ImageURL, ItemCount) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(Date, UserID, UserName, ItemID, ItemName, Category, Price, Detail, Rating, Reviews, ImageURL, ItemCount))

def db_insert_wishes(item_list, user_id, user_name):
    with sql.connect(DB_path) as con:
        cur = con.cursor()

        for num in item_list:         
            Date = date.today()
            UserID = user_id
            UserName = user_name
            ItemID = num[0]
            ItemName = num[1]
            Category = num[2]
            Price = num[3]
            Detail = num[4]
            Rating = num[5]
            ImageURL = num[7]
            
            cur.execute("INSERT INTO wishes (Date, UserID, UserName, ItemID, ItemName, Category, Price, Detail, Rating, ImageURL) VALUES (?,?,?,?,?,?,?,?,?,?)",(Date, UserID, UserName, ItemID, ItemName, Category, Price, Detail, Rating, ImageURL))
            con.commit()   
            
def db_insert_users(form, user_type):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        
        if user_type == "Guest":
            hashed_salted_password = ""
        else:
            
            # Hashing & Salting
            hashed_salted_password = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
        
        cur.execute("INSERT INTO users (FirstName, LastName, Address, Phone, Email, CardNumber, UserType, Password) VALUES (?,?,?,?,?,?,?,?)",(form.first_name.data, form.last_name.data, form.address.data, form.phone.data, form.email.data, form.card_number.data, user_type, hashed_salted_password))
        con.commit()
              
def db_insert_orders(cart_list, user_id, user_name):
    with sql.connect(DB_path) as con:
        cur = con.cursor()

        for num in cart_list:         
            Date = date.today()
            UserID = user_id
            UserName = user_name
            ItemID = num[4]
            ItemName = num[5]
            Category = num[6]
            Price = num[7]
            Detail = num[8]
            Rating = random.randint(1, 5)
            # Reviews = num[10]
            Reviews = "---------------------------------------------------------------------"
            ImageURL = num[11]
            ItemCount = num[12]
            ReviewTitle = "-----------"
            
            cur.execute("INSERT INTO orders (Date, UserID, UserName, ItemID, ItemName, Category, Price, Detail, Rating, Reviews, ImageURL, ItemCount, ReviewTitle) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",(Date, UserID, UserName, ItemID, ItemName, Category, Price, Detail, Rating, Reviews, ImageURL, ItemCount, ReviewTitle))
            con.commit()   
         
def db_update_carts(item_id, item_count):
   with sql.connect(DB_path) as con:
      cur = con.cursor()
      
      cur.execute(f"UPDATE carts SET ItemCount = {item_count} WHERE CartID = '{item_id}'")
      con.commit()
       
def db_delete(table, col_target, col_value):
   with sql.connect(DB_path) as con:
      cur = con.cursor()
      
      cur.execute(f"DELETE FROM {table} WHERE {col_target} = '{col_value}'")
      con.commit() 

def db_update_payment_info(form, user_id):
      with sql.connect(DB_path) as con: 
         cur = con.cursor() 
         cur.execute("UPDATE users SET FirstName=?, LastName=?, Address=?, Phone=?, Email=?, CardNumber=? WHERE UserID=?", (form.first_name.data, form.last_name.data, form.address.data, form.phone.data, form.email.data, form.card_number.data, user_id)) 
         con.commit()

def db_search_item(search_name):
   with sql.connect(DB_path) as con:
      con.row_factory = sql.Row 
      cur = con.cursor() 
      
      cur.execute(f"select * from items where Detail Like '%{search_name}%' OR\
                                             ItemName Like '%{search_name}%' OR\
                                             Category Like '%{search_name}%' OR\
                                             AnotherDetail Like '%{search_name}%'")
      list= cur.fetchall(); 
      
      return list
  
def db_drop_duplicates(table_name, list, sort_col, sort_order):
    with sql.connect(DB_path) as con:
        cur = con.cursor()
        # Check colmuns
        cur.execute(f"PRAGMA table_info('{table_name}')") 
        table_info= cur.fetchall(); 
        
        cols = []
        for i in range(len(table_info)):
            cols.append(table_info[i][1])
        print(cols)


    df = pd.DataFrame(list)            
    if (table_name == "logs"):
        cols = ["LogID", "Date", "UserID", "UserName", "ItemID", "ItemName", "Category", "Price", "Detail","Rating", "Reviews", "ImageURL"]
    elif (table_name == "orders"):
        cols = ["OrderID", "Date", "UserID", "UserName", "ItemID", "ItemName", "Category", "Price", "Detail","Rating", "Reviews", "ImageURL", "ItemCount", "ReviewTitle"]
    else:
        cols = ['WishID', 'Date', 'UserID', 'UserName', 'ItemID', 'ItemName', 'Category', 'Price', 'Detail', 'Rating', 'ImageURL']
    
    if (sort_order == "ASC"):
        sort_order = True
    else:
        sort_order = False

    df.columns = cols
    df.drop_duplicates(subset=['ItemID'], keep='last', inplace=True)
    df["Price"] = df["Price"].astype(float)
    df.sort_values(by = sort_col, ascending = sort_order, inplace=True)
    new_list = df.values.tolist()
    
    return new_list

def check_password(registered_password, entered_password):
    return check_password_hash(registered_password, entered_password)
