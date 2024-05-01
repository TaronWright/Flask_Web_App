from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in succesfully!", category= 'success')
                login_user(user, remember= True) # this uses the flask_login library (stores in flask session)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again", category = 'error')
        else:
            flash('Email does not exist', category = "error")

    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required #this ensures that we cannot access this page if the user is not logged in
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('sign-up', methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
    
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists", category = 'error')
        elif len(email) < 4:
            flash("Email must be greater than 4 characters.", category = 'error')
        elif len(firstName) < 3:
            flash("First Name must be greater than 2 characters.", category = 'error')
        elif not password1:
            flash("Must enter a Password", category ='error')
        elif password1 != password2:
            flash("Passwords do not match", category = 'error')
        else:
            new_user = User(email = email, firstName = firstName, password = generate_password_hash(password1, method ='pbkdf2:sha256') )
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category = 'success')
            login_user(user, remember= True) # this uses the flask_login library (stores in flask session)
            return redirect(url_for('views.home')) # this url_for takes the blueprint name and then the function name with this dot notation


    return render_template("sign-up.html", user = current_user)