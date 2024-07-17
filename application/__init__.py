from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager



db=SQLAlchemy()
DB_NAME="database.db"

def create_app():
    app=Flask(__name__)

    app.config['SECRET_KEY']="sssshhhhhhhhhhhh!"
    app.config['SQLALCHEMY_DATABASE_URI']=f"sqlite:///{DB_NAME}"
    db.init_app(app )

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import Employee

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Employee.query.get(int(user_id))


    return app



def create_database(app):
    if not path.exists("application/" + DB_NAME):
        with app.app_context():
            db.create_all()     # create_all(app=app)
            print('created database!')
