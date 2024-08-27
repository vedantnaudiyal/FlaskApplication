import pytest
from application import create_app, db, config
from application.models import Employee
from werkzeug.security import generate_password_hash
import datetime

@pytest.fixture(scope='module')
def test_client():
    flask_app=create_app(config.TestingConfig)

    with flask_app.test_client() as client:
        with flask_app.app_context():
            db.create_all()

            user0=Employee(
                name='test_user',
                email="test_user@gmail.com",
                age=21,
                password=generate_password_hash(password="test_user_password", method='pbkdf2'),
                dateofjoining=datetime.datetime.strptime("2024-07-01", "%Y-%m-%d").date()
            )
            # sewt up
            db.session.add(user0)
            db.session.commit()

            yield client

            # tear down
            db.drop_all()