from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_hashing_login"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

# Make routes for the following:

# GET /
# Redirect to /register.

# GET /register
# Show a form that when submitted will register/create a user. This form should accept a username, password, email, first_name, and last_name.

# Make sure you are using WTForms and that your password input hides the characters that the user is typing!

# POST /register
# Process the registration form by adding a new user. Then redirect to /secret
# GET /login
# Show a form that when submitted will login a user. This form should accept a username and a password.

# Make sure you are using WTForms and that your password input hides the characters that the user is typing!

# POST /login
# Process the login form, ensuring the user is authenticated and going to /secret if so.
# GET /secret
# Return the text “You made it!” (don’t worry, we’ll get rid of this soon)

@app.route('/')
def redirect_to_reg():
    return redirect ('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data,
        password = form.password.data,

        newUser = User.register(username, password)

        newUser.email = form.email.data,
        newUser.first_name = form.first_name.data,
        newUser.last_name = form.last_name.data

        db.session.add(newUser)
        db.session.commit()

        return redirect('/secret')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            session["user_id"] = user.id  # keep logged in
            return redirect("/secret")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)
        
        
@app.route('/secret')
def secret():
    return "You made it!"