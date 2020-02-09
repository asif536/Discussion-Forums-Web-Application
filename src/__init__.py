from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"]=os.environ.get('SECRET_KEY')
app.config["DEBUG"]=True
db=SQLAlchemy(app)
from src import routes
