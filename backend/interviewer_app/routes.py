from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import SignUpForm, LoginForm
from .models import User
from interviewer_app import db, loginManager
from flask_login import login_user

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home_page():
    return render_template('index.html')

@main.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user_login = User.query.filter_by(email=form.email.data).first()

        if attempted_user_login and attempted_user_login.validate_password(form.password.data):
            login_user(attempted_user_login)
            flash(f'You have successfully logged in, {attempted_user_login.firstName} {attempted_user_login.lastName}', category='success')
            return redirect(url_for('main.home_page'))
        else:
            flash(f'Login failed. Type in your email and password correctly.', category='danger')

    return render_template('login_page.html', form=form)

@main.route("/sign-up", methods=['GET', 'POST'])
def sign_up_page():
    form = SignUpForm()
    
    if form.validate_on_submit():
        user_to_create = User(firstName=form.firstName.data,
                              lastName=form.lastName.data,
                              email=form.email.data,
                              password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('main.home_page'))
    
    if form.errors != {}: # Checks if there are any errors from the validations in the SignUpForm class.
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('sign_up_page.html', form=form)