from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://testuser:password@localhost/umfragen_test2"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

