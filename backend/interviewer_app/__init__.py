from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from openai import OpenAI
from typing import List
from pydantic import BaseModel
import os

# This extracts the OpenAI API key from the environment variable.
open_ai_api_key = os.environ['openAISecretKey']

# This initialises all key objects that are going to passed through the Flask app instance
# beforehand. They can then be imported as needs be across the interviewer_app folder.
# This approach also deals with the circular import issue that can take place with the app instance.
db = SQLAlchemy()
bcrypt = Bcrypt()
loginManager = LoginManager()
client = OpenAI(api_key=open_ai_api_key)

# Creates an instance of the Flask class, then initialises all key objects to the app instance
# before returning it.
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
