import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
# from .config import Config


db=SQLAlchemy()

def create_app(configs):
    app=Flask(__name__)
    app.config.from_object(configs)
    app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')


    db.init_app(app)


    from .views import views
    from .auth import auth
    from .auth import oauth_github_blueprint


    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(oauth_github_blueprint, url_prefix="/github_login")
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
    # if not path.exists("application/" + DB_NAME):
    with app.app_context():
        db.create_all()     # create_all(app=app)
        print('created database!')

