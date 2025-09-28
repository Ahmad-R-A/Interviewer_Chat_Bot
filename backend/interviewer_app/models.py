from interviewer_app import db, bcrypt, loginManager
from flask_login import UserMixin

# This logs the user in by utilising loginManager so that
# the User object can be searched in the database and returned to the User.
@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# The User class stores information on a User who signs up/logins to the website.
# This is key for preventing spam/incorrect usage of the OpenAI's API to save costs.
# This idea will be implemented in the future with a ChatHistory class.
# Extends UserMixin so it works with Flask-Login for session management.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    firstName = db.Column(db.String(length=100), nullable = False)
    lastName = db.Column(db.String(length=100), nullable = False)
    email = db.Column(db.String(length = 255), nullable = False, unique=True)
    password_hash = db.Column(db.String(length = 60), nullable = False)
    # chat_history = db.relationship('ChatHistory', backref='user_chat_history', lazy=True)

    # A method that acts like an attribute that when called, will raise an 
    # error message and prevent the user from accessing this field. 
    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute.")
    
    # This method is used to set the password_hash attribute with the password
    # value that was passed to this method, encrypting it and making sure it is not read.
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    # Validates the submitted password in the database.
    def validate_password(self, submitted_password):
        return bcrypt.check_password_hash(self.password_hash, submitted_password)

# class ChatHistory(db.Model, UserMixin):
#     id = db.Column(db.Integer(), primary_key=True)
#     user_messages = db.Column(db.String(), nullable=False)
#     bot_messages = db.Column(db.String(), nullable=False)
#     user = db.Column(db.Integer(), db.ForeignKey('user.id'))
    