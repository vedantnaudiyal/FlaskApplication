
from flask import Blueprint, jsonify, request
from flask import render_template
from flask_login import login_required, current_user
from .models import Employee
from . import db

views=Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("home.html", employee=current_user, employees=Employee.query.all())


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


@views.route("/employees", methods=['GET'])
def getAllEmployees():
    employees=Employee.query.all()
    emp_lst = [{"name":employee.name,"email": employee.email,"age": employee.age, "isActive": employee.isActive, "employeeId": employee.id}
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
        "employeeId": employee.id
    })
