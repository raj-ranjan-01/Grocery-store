import os

class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

class LocalDevelopmentConfig(Config):
    ##### Flask APP Config #####
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///grocery.db"
    SECRET_KEY = "secretkey" 
    JWT_TOKEN_LOCATION = ["headers"]