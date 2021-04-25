from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import generate_password_hash, check_password_hash
import random
import torch

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registration")
def registration():
    return render_template("registration.html")
@app.route("/home")
def home():
    return render_template("home.html")
@app.route("/register", methods=["POST"])
def register():
    name=request.form["name"]
    password=request.form["password"]
    print("????")
    hash_value = generate_password_hash(password)
    sql="INSERT INTO users (name, password) VALUES (:name, :password)"
    db.session.execute(sql, {"name":name,"password":hash_value})
    db.session.commit()
    return redirect("/")

@app.route("/login",methods=["POST"])
def login():
    name = request.form["name"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()    
    if user==None:
        return redirect("/")
    else:
        hash_value=user[0]
        if check_password_hash(hash_value, password):
            session["name"]=name
            return redirect("/home")
        else:
            return redirect("/")
    return redirect("/")

@app.route("/logout")
def logout():
    del session["name"]
    return redirect("/")

@app.route("/calculator")
def calculator():
    x=2+2
    s="Calculator! \n"
    s+=" "+str(x)
    s+="\n"
    s+="fff"
    return s

@app.route("/page1/<int:id>")
def page(id):
    v=random.randint(0,10)
    v=round(v)
    return str(v)

