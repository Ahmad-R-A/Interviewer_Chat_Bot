import json
from flask import Blueprint, Response, render_template, redirect, session, stream_with_context, url_for, flash, request, jsonify
from .forms import SignUpForm, LoginForm, ChatBotForm
from .models import User, ChatHistory
from interviewer_app import db, loginManager
from flask_login import login_user, logout_user, login_required
from interviewer_app import client

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home_page():
    return render_template('index.html')

@main.route('/interviewer_chat_bot', methods=['POST', 'GET'])
@login_required
def chat_bot_page():
    form = ChatBotForm()

    # if form.validate_on_submit:
    #     chat_history = ChatHistory.query.filter_by(user=)

    return render_template('chat_bot_page.html', form=form)

@main.route('/ask', methods=['POST'])
@login_required
def ask():
    data = request.get_json()
    user_input = data.get("userPrompt")

    def generate():
        response = client.responses.create(
            model='gpt-5-mini',
            input=[
                {
                    "role": "system",
                    "content": "You are an interviewer preparing the user for their career path."
                },
                {
                    "role": "user",
                    "content": user_input
                },
            ],
            stream=True,
        )

        for chunk in response:
            response_type = chunk.type

            if response_type == "response.output_text.delta" and chunk.delta is not None:
                delta = chunk.delta
                yield delta

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@main.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user_login = User.query.filter_by(email=form.email.data).first()

        if attempted_user_login and attempted_user_login.validate_password(form.password.data):
            login_user(attempted_user_login)
            session['_user_id'] = attempted_user_login.id
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
        login_user(user_to_create)
        session['_user_id'] = user_to_create.id
        flash(f'You have successfully signed up and have now logged in as {user_to_create.firstName} {user_to_create.lastName}', category='success')
        return redirect(url_for('main.home_page'))
    
    if form.errors != {}: # Checks if there are any errors from the validations in the SignUpForm class.
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('sign_up_page.html', form=form)

@main.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out of your account.', category='info')
    return redirect(url_for('main.home_page'))

@main.errorhandler(401)
def unauthorised_access(error):
    return render_template('error_pages/401_error_page.html'), 401

@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('error_pages/404_error_page.html'), 404

@main.app_errorhandler(405)
def method_not_allowed(error):
    return render_template('error_pages/405_error_page.html'), 405