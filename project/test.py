from this import d
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta 
from flask_sqlalchemy import SQLAlchemy
from admin.main_2 import second

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(hours=2)

app.register_blueprint(second, url_prefix="/admin")

db = SQLAlchemy(app)

class users(db.Model):
    __tablename__ = 'users'
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", content="Testing")

@app.route("/view")
def view():
    return render_template("view.html", values = users.query.all())

@app.route("/test")
def test():
    return render_template("new.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email 
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash("Login successful!")
        return redirect(url_for("user", usr=user))
    else: 
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]
           

        return render_template("user.html", email=email)
    else: 
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"Successfully logged out {user}!", "info")
    session.pop("user", None)
    session.pop("email", None)
    
    return redirect(url_for("login"))

# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}!"

# @app.route("/admin")
# def admin():
#     return redirect(url_for("home"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)   