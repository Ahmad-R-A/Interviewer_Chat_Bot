from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired

class SignUpForm(FlaskForm):
    firstName = StringField(label='First Name', validators=[Length(min=2, max=100), DataRequired()])
    lastName = StringField(label='Last Name', validators=[Length(min=2, max=100), DataRequired()])
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=8), DataRequired()])
    confirmPassword = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Create Account')
