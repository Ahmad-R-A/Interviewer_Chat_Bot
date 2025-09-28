# The import below for create_app method is important as this returns
# the app object alongside everything else being initialised within the app object
# so it is ready to be run through this file.
# The db is also important so that a database can be created if the app detects that
# there is no database within the directory.
from interviewer_app import create_app, db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)