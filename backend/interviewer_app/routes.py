from flask import Blueprint, Response, render_template, redirect, session, stream_with_context, url_for, flash, request
from .forms import SignUpForm, LoginForm, ChatBotForm
from .models import User, ChatHistory
from interviewer_app import db, loginManager
from flask_login import login_user, logout_user, login_required
from interviewer_app import client

# Blueprint ensures that importing the app object does not have to be done and instead,
# all routes can be assigned to the Blueprint object, then the Blueprint object can be
# passed to the app object and provide all the routes to it. This prevents a circular import issue.
main = Blueprint('main', __name__)

'''
Below are the main routes for the website. These routes are accessible as a webpage
or are means of communication with the OpenAI's API whilst making sure a user cannot
explicitly access that route.
'''

# The home page has 2 routes to ensure users do not have issues coming across the website through the URL.
@main.route("/")
@main.route("/home")
def home_page():
    return render_template('index.html')

# This the interviewer chat bot page of the website.
@main.route('/interviewer_chat_bot', methods=['POST', 'GET'])
@login_required
def chat_bot_page():
    form = ChatBotForm()

    # if form.validate_on_submit:
    #     chat_history = ChatHistory.query.filter_by(user=)

    return render_template('chat_bot_page.html', form=form)

# This is the route where user's input gets extracted and the communication
# between Python and the OpenAI API takes place. The response is then returned back to the website.
# NOTE: This route is protected by login_required and only accepts POST,
# so it can only be accessed via an authenticated request.
@main.route('/ask', methods=['POST'])
@login_required
def ask():
    data = request.get_json()
    user_input = data.get("userPrompt")

    # A helper function to get the response from the OpenAI API and yield
    # each chunk of data back to the chat bot page.
    def generate():
        # Getting a response from OpenAI. To make it easier to keep up with the documentation, naming convention
        # is in accordance with the names of the fields provided by the documentation.
        # More can be understood from the documentation:
        # https://platform.openai.com/docs
        response = client.responses.create(
            model='gpt-5-mini',
            input=[
                {
                    # The contents of the system role is fixed for now.
                    # However, plans for a customising the contents of the system role will be added in the future.
                    "role": "system",
                    "content": "You are an interviewer preparing the user for their career path."
                },
                {
                    # This is where the user's input is passed to the OpenAI.
                    "role": "user",
                    "content": user_input
                },
            ],
            stream=True,
        )

        # Each chunk is a response object. Within these objects contains lots of information.
        # However we are only concerned with a few key details.
        for chunk in response:
            # Each response object has a type so we first need to carry out a validation
            # to make sure we can access existing fields and not crash the server.
            response_type = chunk.type

            if response_type == "response.output_text.delta" and chunk.delta is not None:
                # response.output_text.delta is the response type we are looking for. It has a field called
                # delta which contains the text response from OpenAI.
                delta = chunk.delta
                yield delta

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

# This route is where the user gets to login into their account
# and use the Interviewer Chat Bot.
@main.route("/login", methods=['GET', 'POST'])
def login_page(): 
    form = LoginForm()

    # Validates the login form through the validators set up in the LoginForm class in forms.py 
    if form.validate_on_submit():
        # Should only return a single User object, otherwise None will be returned
        attempted_user_login = User.query.filter_by(email=form.email.data).first()

        # Checks to see if the User object exists alongside the correct password being provided for the account
        if attempted_user_login and attempted_user_login.validate_password(form.password.data):
            # Logs in the user to the session as well as setting a session variable for the user id and redirecting
            # to the home page.
            login_user(attempted_user_login)
            session['_user_id'] = attempted_user_login.id
            flash(f'You have successfully logged in, {attempted_user_login.firstName} {attempted_user_login.lastName}', category='success')
            return redirect(url_for('main.home_page'))
        else:
            # Displays an error message to the user. Also provides a category to implement in the
            # HTML pages by using Jinja Template.
            flash(f'Login failed. Type in your email and password correctly.', category='danger')

    return render_template('login_page.html', form=form)

# This route is where the user gets to create their account,
# with the information being stored in a database and are logged in immediately.
@main.route("/sign-up", methods=['GET', 'POST'])
def sign_up_page():
    form = SignUpForm()
    
    # Validates the sign up form through the validators set up in the SignUpForm class in forms.py 
    if form.validate_on_submit():
        # Manually assigns the data of the form fields to the User class fields.
        user_to_create = User(firstName=form.firstName.data,
                              lastName=form.lastName.data,
                              email=form.email.data,
                              password=form.password.data)
        # This object is then submitted to the database
        db.session.add(user_to_create)
        db.session.commit()

        # The user is also logged in and is informed of this, being redirected back to the home page.
        login_user(user_to_create)
        session['_user_id'] = user_to_create.id
        flash(f'You have successfully signed up and have now logged in as {user_to_create.firstName} {user_to_create.lastName}', category='success')
        return redirect(url_for('main.home_page'))
    
    if form.errors != {}: # Checks if there are any errors from the validations in the SignUpForm class.
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('sign_up_page.html', form=form)

# Logs the user out and clears their Flask-Login session
@main.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out of your account.', category='info')
    return redirect(url_for('main.home_page'))

'''
END of routes.
'''

'''
Below are the errorhandler routes that provide a clean and user friendly error page.
'''

@main.errorhandler(401)
def unauthorised_access(error):
    return render_template('error_pages/401_error_page.html'), 401

@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('error_pages/404_error_page.html'), 404

@main.app_errorhandler(405)
def method_not_allowed(error):
    return render_template('error_pages/405_error_page.html'), 405

'''
END of errorhandlers.
'''