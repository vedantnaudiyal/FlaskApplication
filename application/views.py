from flask import Blueprint, jsonify, request
from flask import render_template
from flask_login import login_required, current_user
from .models import Employee
from . import db
import datetime
from werkzeug.security import generate_password_hash
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import select



# schema for employee model
class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model=Employee
        load_instance=True




employee_schema=EmployeeSchema()
employees_schema=EmployeeSchema(many=True)

views=Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    print("hello world")
    return render_template("home.html", employee=current_user, employees=Employee.query.all())

@views.route('/callback')
def callback():
    print("hello world")
    return render_template("home.html")


@views.route('/employees/<int:id>', methods=['DELETE'])
def deleteEmployee(id):
    # employee=json.loads(request.data)
    # emplyeeId=employee['employeeId']
    employee=Employee.query.get(id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({
            "employeeId": employee.id,
            "name": employee.name,
            "email": employee.email,
            "age": employee.age,
            "isActive": employee.isActive
        })
    else:
        return "no employee with this id is present"


@views.route("/employees/<int:id>", methods=['PUT'])
def editEmployee(id):
    print("put request")
    data = request.get_json()
    print(data)

    employee = Employee.query.get(id)
    if employee:
        print(employee)
        if data.get('name'):
            employee.name=data.get('name')
        if data.get('email'):
            employee.email = data.get('email')
        if data.get('age'):
            employee.age = data.get('age')
        if data.get('isActive'):
            employee.isActive = data.get('isActive')
        if data.get('dateOfJoining'):
            date_of_joining = data.get('dateOfJoining')
            try:
                date_of_joining = datetime.datetime.strptime(date_of_joining, "%Y-%m-%d").date()
            except Exception as e:
                print(e)
                return "Pls fill the date in a valid format :'YYYY/MM/DD'"
            employee.dateofjoining=date_of_joining
        db.session.commit()
        return jsonify({
            "employeeId": employee.id,
            "name": employee.name,
            "email": employee.email,
            "age": employee.age,
            "isActive": employee.isActive,
            "dateOfJoining": employee.dateofjoining
        })
    else:
        return "no employee with this id is present"


@views.route("/employees", methods=['GET'])
def getAllEmployees():
    print("hello world")
    employees=Employee.query.all()
    emp_lst = [{"name":employee.name,"email": employee.email,"age": employee.age, "isActive": employee.isActive, "employeeId": employee.id, "dateOfJoining": employee.dateofjoining}
                for employee  in employees]

    return jsonify(emp_lst)


@views.route("/employees/<int:id>", methods=['GET'])
def getEmployee(id):
    employee=Employee.query.get(id)

    return jsonify({
        "name":employee.name,
        "email": employee.email,
        "age": employee.age,
        "isActive": employee.isActive,
        "employeeId": employee.id,
        "dateOfJoining": employee.dateofjoining
    })

@views.route("/employees", methods=['POST'])
def createEmployee():
    data = request.json
    print("printing data", data)
    name = data.get("username")
    email = data.get("email")
    age = data.get("age")
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    date_of_joining = data.get("date_of_joining")

    # validations
    print("hello world!")
    if len(name) < 4 or len(name) > 50:
        return "Error: please keep the name's length in the range of [4,30]"
    # elif (len(email) < 6 or len(email) > 50) and "@" in email:
    #     return "Error: please give a valid email"
    elif len(password) < 4 or len(password) > 50:
        return "Error: password must be atleast 4 characters long!"
    elif password != confirm_password:
        return "Error: please keep the name's length in the range of [4,30]"

    try:
        date_of_joining = datetime.datetime.strptime(date_of_joining, "%Y-%m-%d").date()
    except Exception as e:
        print(e)
        return "Pls fill the date in a valid format :'YYYY/MM/DD'"

    new_employee = Employee(
                    name=name,
                    email=email,
                    age=age,
                    password=generate_password_hash(password=password, method='pbkdf2'),
                    dateofjoining=date_of_joining
                )
    db.session.add(new_employee)
    print("emailk", email)
    try:
        db.session.commit()
    except:
        return "an employee with this email already exists in the system!"

    return jsonify(employee_schema.dump(new_employee)), 201


@views.route("/search_by_name/<name>")
def search_employees_by_name(name):
    print("hello world")
    # employees=None
    try:
        query=select(Employee).filter(Employee.name.like(f"%{name}%")).order_by(Employee.name)
        employees=db.session.execute(query).scalars().all()
        print(employees)
    except Exception as e:
        return jsonify(e)

    return jsonify(employees_schema.dump(employees)), 200

