
class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///database.db"
    TESTING = False
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_database.db'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
