from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
import pyrebase 

#Code goes below here

image_link = "https://scontent.ftlv21-1.fna.fbcdn.net/v/t31.18172-1/1502644_10152506946962507_2442851309927378964_o.png?stp=c49.0.148.148a_dst-png_p148x148&_nc_cat=111&ccb=1-7&_nc_sid=1eb0c7&_nc_ohc=d-R_wjIm2d8AX_NugPv&_nc_ht=scontent.ftlv21-1.fna&oh=00_AT8CSjiG8-biys_qQ9tU-yrxzJSp6HANxsz5c3mFVk-G2Q&oe=62FD0A1B"

config = {
  'apiKey': "AIzaSyDDQnFYQgmOMw8q8PLMJ67I79NgjiDMGWg",
  'authDomain': "ibrahim-mini-pro.firebaseapp.com",
  'projectId': "ibrahim-mini-pro",
  'storageBucket': "ibrahim-mini-pro.appspot.com",
  'messagingSenderId': "175534370798",
  'appId': "1:175534370798:web:ae2f1e2fe74dd12e1be8ff",
  'measurementId': "G-53VQVPLR1J",
  "databaseURL": "https://ibrahim-mini-pro-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase =pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
 
@app.route('/', methods=['GET', 'POST' ])
def home():
    return render_template("home.html")


@app.route('/main' , methods=['GET','POST'] )  
def main():
    users = db.child('Users').get().val()
    print(users)
    for user in users:
        print(user,'bob',login_session['user']['localId'])
        if user == login_session['user']['localId']:
            yop = users[user]['email']
            print(user, 'user') 
            return render_template('main.html' , yop = yop)
        
    return render_template('home.html')    





@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
       username = request.form['username']
       if username == 'admin':
           login_session['admin'] = True
    return render_template("admin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
   error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       user = {"email": email, "password": password}
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            db.child("Users").child(login_session["user"]["localId"]).set(user)
            return redirect(url_for('main'))
       except:
           error = "Authentication failed"
   return render_template("signup.html")
   print(auth.create_user_with_email_and_password(email, password))



@app.route('/login', methods=['GET', 'POST'])
def login():
   error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('main'))
       except:
           error = "Authentication failed"
   return render_template("login.html")




@app.route('/ment' , methods= [ 'GET' , 'POST' ])
def ment():
    return render_template ('ment.html')


@app.route('/cucumber')
def cucumber():
    return render_template ('cucumber.html')



@app.route('/shiri')
def shiri():
    return render_template ('shiri.html')



@app.route('/meat')
def meat():
    return render_template ('meat.html')




@app.route("/add_info", methods=["GET", "POST"])
def plants():
    if request.method == 'POST':
       name = request.form['name']
       plant_type = request.form['plant_type']
       season = request.form['season']
       try:
            plant = {"name": name, "plant_type": plant_type, "season": season}
            db.child("Plants").push(plant)
            return redirect(url_for('main')) 
       except:
           return render_template("add_plant.html", error = "Failed to add plant")    
    return render_template("add_plant.html")








#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)