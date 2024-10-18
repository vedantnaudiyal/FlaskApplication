from flask import Blueprint, render_template, request, redirect, url_for
from .models import Employee
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
import datetime, os
from flask_dance.contrib.github import make_github_blueprint, github

import logging
from flask_dance.consumer import oauth_authorized

logging.basicConfig(level=logging.DEBUG)


auth = Blueprint('auth', __name__)

# oauth_github_blueprint=make_github_blueprint(
#     client_id=os.environ.get('CLIENT_ID'),
#     client_secret=os.environ.get('CLIENT_SECRET'),
#     redirect_url="http://localhost:5000/github_login/github/authorized"
# )

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        print(data)
        email = data.get("email")
        password = data.get("password")
        employee=Employee.query.filter_by(email=email).first()
        # print(employee.email)
        # for item in employee:
        #     print(item)
        if employee and check_password_hash(employee.password, password):
            print("successfully logged in!")
            login_user(employee, remember=True)
            return redirect(url_for("views.home"))
        else:
            return "Invalid Credentials!"
    return render_template("login.html", emplopyee=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    # if not github.authorized:
    #     return redirect(url_for("github.login"))

    #
    if request.method == 'POST':
        data = request.form
        print(data)
        name = data.get("username")
        email = data.get("email")
        age = data.get("age")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        date_of_joining= data.get("date_of_joining")
        print(date_of_joining)

        # validations

        if len(name) < 4 or len(name) > 30:
            return "Error: please keep the name's length in the range of [4,30]"
        elif (len(email) < 6 or len(email) > 30) and "@" in email:
            return "Error: please give a valid email"
        elif len(password) < 4 or len(password) > 50:
            return "Error: password must be atleast 4 characters long!"
        elif password != confirm_password: return "Error: please keep the name's length in the range of [4,30]"

        try:
            date_of_joining = datetime.datetime.strptime(date_of_joining, "%Y-%m-%d").date()
        except Exception as e:
            print("updated")
            print(e)
            return "Pls fill the date in a valid format :'YYYY/MM/DD'"
        print(date_of_joining, type(date_of_joining))

        new_employee = Employee(name=name, email=email, age=age,
                                    password=generate_password_hash(password=password, method='pbkdf2'), dateofjoining=date_of_joining)
        db.session.add(new_employee)
        try:
            db.session.commit()
        except:
            return "an employee with this email already exists in the system!"


        print("new employee data stored in our table")

        return redirect(url_for("views.home"))


    return render_template("signup.html", emplopyee=current_user)
