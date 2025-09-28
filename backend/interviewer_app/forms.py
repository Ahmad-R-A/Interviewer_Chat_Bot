from interviewer_app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Length, EqualTo, Email, DataRequired

# This class inherits from the FlaskForm class and is used alongside Jinja syntax
# to create a form where the user can submit their information to create an account for the website.
# This form also has custom validation make sure that the same email is not used for multiple separate accounts
# informing the user of this error when it happens.
class SignUpForm(FlaskForm):
    firstName = StringField(label='First Name', validators=[Length(min=2, max=100), DataRequired()])
    lastName = StringField(label='Last Name', validators=[Length(min=2, max=100), DataRequired()])
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=8), DataRequired()])
    confirmPassword = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Create Account')

    # Raises an error if a user tries to sign up with an email that already exists in the database.
    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError(f'This email has already been used to make an account : {email_to_check.data} ')

# This form is used for logging into an existing account. It works similarly to the SignUpForm class.
# The other backend works takes place in the routes.py file, specifically to do with login validations.
class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Login")

# This form is used for the chat_bot_page.html where the user inputs a text
# that is to be sent to the OpenAI's API through the routes.py with both "chat_bot_page()" and "ask()" routes.
class ChatBotForm(FlaskForm):
    userPrompt = StringField(label="Prompt", validators=[DataRequired()])
    submit = SubmitField(label='Submit Prompt')