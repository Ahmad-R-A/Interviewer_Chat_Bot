from interviewer_app import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    firstName = db.Column(db.String(length=100), nullable = False)
    lastName = db.Column(db.String(length=100), nullable = False)
    email = db.Column(db.String(length = 255), nullable = False, unique=True)
    password_hash = db.Column(db.String(length = 60), nullable = False)

