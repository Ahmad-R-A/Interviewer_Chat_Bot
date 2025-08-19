from interviewer_app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Length, EqualTo, Email, DataRequired

class SignUpForm(FlaskForm):
    firstName = StringField(label='First Name', validators=[Length(min=2, max=100), DataRequired()])
    lastName = StringField(label='Last Name', validators=[Length(min=2, max=100), DataRequired()])
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=8), DataRequired()])
    confirmPassword = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Create Account')

    # Raises an error message when a unique email is not used to create an account.
    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError(f'This email has already been used to make an account : {email_to_check.data} ')

class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    password = StringField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Login")
