from interviewer_app import db, bcrypt, loginManager
from flask_login import UserMixin

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    firstName = db.Column(db.String(length=100), nullable = False)
    lastName = db.Column(db.String(length=100), nullable = False)
    email = db.Column(db.String(length = 255), nullable = False, unique=True)
    password_hash = db.Column(db.String(length = 60), nullable = False)
    # chat_history = db.relationship('ChatHistory', backref='user_chat_history', lazy=True)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute.")
    
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
    