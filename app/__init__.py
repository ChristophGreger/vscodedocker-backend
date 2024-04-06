from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") or "you-will-never-guess"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI") or "sqlite:///site.db"

db = SQLAlchemy(app)

from app.database import models

from app.auth import auth
app.register_blueprint(auth)
