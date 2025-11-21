from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, current_user
from auth import auth_bp, load_user_from_db


app = Flask(__name__)
app.config["SECRET_KEY"] = "1234567890"
app.register_blueprint(auth_bp)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@app.route("/")
@login_required
def index():
    return render_template("index.html")
    # return redirect("/login")

@login_manager.user_loader
def user_loader(id):
    return load_user_from_db(id)