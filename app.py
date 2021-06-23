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
#******************************************************************************************
#ALWAYS USE SAME NAME FOR EVERYTHING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Otherwise nothing works (idk)
#*******************************************************************************************

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
    hash_value = generate_password_hash(password)
    sql="INSERT INTO users (name, password, score) VALUES (:name, :password, 0)"
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
            return redirect("/")
        else:
            return redirect("/")
    return redirect("/home")

@app.route("/logout")
def logout():
    del session["name"]
    return redirect("/")

@app.route("/math")
def math():
    sql = "SELECT id, question, answer, date FROM math ORDER BY id DESC"
    res=db.session.execute(sql)
    questions=res.fetchall()
    return render_template("math.html", questions=questions)

@app.route("/math/<int:id>")
def mathid(id):
    sql="SELECT question FROM math WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    question = result.fetchone()[0]
    sql="SELECT answer FROM math WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    ans=result.fetchone()[0]
    return render_template("mathquestion.html", id=id, question=question,ans=ans)

@app.route("/answer", methods=["POST"])
def answer():
    name=request.form.get('name')
    id=request.form['id']
    id=int(id)
    ans=request.form["answer"]
    sql="SELECT answer FROM math WHERE id=:id"
    result=db.session.execute(sql, {"id":id})
    corr=result.fetchone()[0]
    if ans==corr:
        sql="UPDATE users SET score=score+1 WHERE name=:name"       
        res=db.session.execute(sql, {"id":id})
        db.session.commit()
        sql="SELECT score FROM users WHERE name=:name"
        score=res.fetchone()[2]
        return render_template("correct.html", ans=ans, score=score)
    else:
        session["guess"]=ans
    return redirect("/math/"+str(id))


@app.route("/page1/<int:id>")
def page(id):
    v=random.randint(0,10)
    v=round(v)
    return str(v)

