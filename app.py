from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)


@app.route("/")
def main():
   item_list = []
   
   with sql.connect("EC/EC.db") as con:
      cur = con.cursor()
      cur.execute("select * from items")
      item_list= cur.fetchall(); 
      return render_template("main.html", item_list = item_list)

@app.route("/signin")
def signin():
   return render_template("signin.html")

@app.route("/item")
def item():
   return render_template("item.html")

@app.route("/items")
def items():
   return render_template("items.html")

@app.route("/register")
def register():
   return render_template("register.html")

@app.route('/add_account', methods=['GET', 'POST'])
def add_account(): 
   account_list = []
   
   if request.method == 'POST':
      try:
         FirstName = request.form['inputFirstName'] 
         LastName = request.form['inputLastName'] 
         Phone = request.form['inputPhone'] 
         Email = request.form['inputEmail'] 
         Password = request.form['inputPassword'] 
         ConfirmPassword = request.form['inputConfirmPassword']

         account_list.extend([FirstName,LastName,Phone,Email])
         
         if FirstName!="" and LastName!="" and Phone!="" and Email!="" and Password!="" and ConfirmPassword!="":
               with sql.connect("EC/EC.db") as con:
                  cur = con.cursor()
                  cur.execute("INSERT INTO users (FirstName, LastName, Phone, Email) VALUES (?,?,?,?)",(FirstName, LastName, Phone, Email))
                  con.commit()
                  msg ="Account successfully added"
                  
         else: 
               msg="error in insert operation" 
               con.rollback()
               
      except: 
         msg="error in insert operation"
         con.rollback() 
      
      finally:           
         cur.execute("select * from users where Email=?",(Email,)) 
         account_list= cur.fetchall(); 
         
         cur.execute("select * from items") 
         item_list= cur.fetchall(); 
         
         return render_template("main.html", account_list = account_list, item_list = item_list)
         con.close() 
         
         # return render_template("register_result.html", msg = msg)
         # return render_template("main.html",  account_list = account_list )
         # con.close() 

@app.route('/show_account/<string:UesrID>', methods = ['GET']) 
def show_account(UesrID):
    con = sql.connect("EC/EC.db")
    con.row_factory = sql.Row 
    cur = con.cursor() 
   #  cur.execute("select * from users")
    cur.execute("select * from users where UesrID=?",(UesrID,)) 
    account_list= cur.fetchall(); 
    return render_template("account.html", account_list= account_list) 

if __name__ == '__main__':
   app.run(debug = True)