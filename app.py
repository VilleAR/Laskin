from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import generate_password_hash, check_password_hash
import random
import torch

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html")
@app.route("/registration")
def registration():
    return render_template("registration.html")
@app.route("/register", methods=["POST"])
def register():
    username=request.form["username"]
    password=request.form["password"]
    hash_value = generate_password_hash(password)
    sql="INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username":username,"password":hash_value})
    db.session.commit()
    return redirect("/")
@app.route("/login")
def login():
    return render

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

