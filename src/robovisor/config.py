import os

class Config:
    TESTING = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    # This should be a postgres url
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") 

class DevelopmentConfig(Config):
    # Store data in local sqlite file
    DEBUG = True
    DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Prices.sqlite3'))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'

class TestingConfig(Config):
    # Store temporary testing data in memory
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"