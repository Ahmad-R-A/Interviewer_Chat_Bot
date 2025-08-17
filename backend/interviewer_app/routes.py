from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import SignUpForm
from .models import User
from interviewer_app import db

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home_page():
    return render_template('index.html')

@main.route("/login")
def login_page():
    return render_template('login_page.html')

@main.route("/sign-up", methods=['GET', 'POST'])
def sign_up_page():
    form = SignUpForm()
    
    if form.validate_on_submit():
        user_to_create = User(firstName=form.firstName.data,
                              lastName=form.lastName.data,
                              email=form.email.data,
                              password_hash=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('/home'))
    
    if form.errors != {}: # Checks if there are any errors from the validations in the SignUpForm class.
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('sign_up_page.html', form=form)