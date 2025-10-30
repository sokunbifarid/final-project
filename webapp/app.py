from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from werkzeug.security import generate_password_hash
import sqlite3
import helper
import user_data

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234567890"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        hashed_password = generate_password_hash(request.form.get("password"))
        try:  
            cursor = helper.open_database()
            data = cursor.execute("SELECT * FROM users WHERE username=?", (username)).fetchall()
            print("data: " + str(data))
            check_password_hash(data[0]["hash"], hashed_password)
            helper.close_database()
            print("username: " + str(username) + ", hash passowrd: " + str(hashed_password))
            if len(data) > 0:
                session["username"] = username
                session["user_id"] = data[0]["id"]
                return redirect(url_for("index"))
            else:
                return render_template("login.html", unable_to_login=True)
        except ValueError as e:
            return render_template("login.html", unable_to_login=True)
    return render_template("login.html", unable_to_login=False)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")
        cursor = helper.open_database()
        try:
            data = cursor.execute("SELECT * FROM users WHERE username=? AND email = ?", (username, email)).fetchall()
            if data:
                return render_template("register.html", wrong_credentials=False, account_exists=True)
        except ValueError as e:
            pass
        if password != confirm_password:
            return render_template("register.html", wrong_credentials=True, account_exists=False)
        hashed_password = generate_password_hash(request.form.get("password"))
        cursor.execute("INSERT INTO users (username, email, hash, cash) VALUES(?,?,?,?)", (username, email, hashed_password, user_data.get_user_starting_cash()))
        helper.commit_database()
        helper.close_database()
        return render_template("index.html")
    return render_template("register.html", wrong_credentials=False, account_exists=False)

