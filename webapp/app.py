from flask import Flask, render_template, request, redirect
import sqlite3
from helper.py import db_execute

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pass
        # continue here accept the data from the login form and process it with the database, either you accept the login or reject it and create a new
        # html file (no-login.html) that displays the unable to login
    return render_template("login.html")
