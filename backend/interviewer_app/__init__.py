from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from openai import OpenAI
from typing import List
from pydantic import BaseModel
import os

open_ai_api_key = os.environ['openAISecretKey']

db = SQLAlchemy()
bcrypt = Bcrypt()
loginManager = LoginManager()
client = OpenAI(api_key=open_ai_api_key)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///interviewer_app.db'
    app.config['SECRET_KEY'] = 'some_secret_key'  # required for FlaskForm CSRF

    db.init_app(app)
    bcrypt.init_app(app)
    loginManager.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app
