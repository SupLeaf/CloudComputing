import os

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://testuser:password@localhost/umfragen_test"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

