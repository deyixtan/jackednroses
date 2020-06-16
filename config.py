import os

basedir = os.path.abspath(os.path.dirname(__name__))

class Config:
    SECRET_KEY = "jackednroses"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
