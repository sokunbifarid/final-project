from flask import Flask, Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from helper import open_database, close_database, commit_database, User
import user_data

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

def load_user_from_db(id):
    cursor = open_database()
    userdata = cursor.execute("SELECT * FROM users WHERE id=?", [id]).fetchone()
    close_database()
    if userdata:
        return User(userdata[0], userdata[2], userdata[1])
    return None

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try_login(email, password)
    return render_template("login.html", unable_to_login=False)

def try_login(email, password):
    try:  
        cursor = open_database()
        data = cursor.execute("SELECT * FROM users WHERE email=?", [email]).fetchone()
        if not check_password_hash(data[3], password):
            return render_template("login.html", unable_to_login=True)
        close_database()
        if len(data) > 0:
            user = User(data[0], data[2], data[1])
            login_user(user)
            return redirect(url_for("index"))
        else:
            return render_template("login.html", unable_to_login=True)
    except ValueError as e:
        return render_template("login.html", unable_to_login=True)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")
        cursor = open_database()
        try:
            data = cursor.execute("SELECT * FROM users WHERE username=? AND email = ?", [username, email]).fetchall()
            if data:
                return render_template("register.html", wrong_credentials=False, account_exists=True)
        except ValueError as e:
            pass
        if password != confirm_password:
            return render_template("register.html", wrong_credentials=True, account_exists=False)
        hashed_password = generate_password_hash(request.form.get("password"))
        cursor.execute("INSERT INTO users (username, email, hash, cash) VALUES(?,?,?,?)", [username, email, hashed_password, user_data.get_user_starting_cash()])
        commit_database()
        close_database()
        # return render_template("index.html")
        try_login(email, password)
    return render_template("register.html", wrong_credentials=False, account_exists=False)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return {"success" : 200}