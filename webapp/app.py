from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from werkzeug.security import generate_password_hash
import sqlite3

db_path = "chess_app_database.db"

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        hashed_password = generate_password_hash(request.form.get("password"))
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            data = cursor.execute("SELECT * FROM users WHERE email=? AND hash=?", (email, hashed_password)).fetchall()
            cursor.close()
            if len(data) > 0:
                session["email"] = email
                session["user_id"] = data[0]["id"]
                return redirect(url_for("index"))
            else:
                return render_template("login.html", unable_to_login=True)
        except ValueError as e:
            return render_template("login.html", unable_to_login=True)
    return render_template("login.html", unable_to_login=False)

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")