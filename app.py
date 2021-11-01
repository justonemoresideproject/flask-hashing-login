from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterForm, LoginForm, FeedbackForm

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

    if session['user_id']:
        user = User.query.get_or_404(session['user_id'])
        redirect(f'/users/{user.username}')

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

    if session['user_id']:
        user = User.query.get_or_404(session['user_id'])
        redirect(f'/users/{user.username}')

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            session["user_id"] = user.id
            return redirect("/secret")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)
        
# Now that we have some logging in and and logging out working. Let’s add some authorization! When a user logs in, take them to the following route:

# GET /users/<username>
# Display a template the shows information about that user (everything except for their password)

# You should ensure that only logged in users can access this page.
        
@app.route('/secret')
def secret():
    if "user_id" not in session:
        flash('You do not have permission to that resource')
        return render_template('login.html')
    # return render_template('secrets.html')
    username = form.username.data
    return redirect(f'/users/{username}')

@app.route('/users/<username>')
def get_user(username):
    # if "user_id" not in session:
    #     flash('You do not have permission to that resource')
    #     return render_template('login.html')
    user = User.query.filter_by(username=f'{username}').first()

    return render_template('user.html', user=user)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id')
    return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    user = User.query.filter_by(username=f'{username}')
    form = FeedbackForm()
    if "user_id" not in session:
        flash('You do not have permission to that resource')
        return render_template('login.html')
    return render_template('addFeedback.html', user=user, form=form)

@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(feedback)

    if session['user_id'] != feedback.user.id or "user_id" not in session:
        flash('You do not have permission to that resource')
        return render_template('login.html')

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        return redirect(f'users/{feedback.user.username}')
        
    return render_template('feedback.html', feedback=feedback)

@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def deleteBack(feedback_id):
    if session['user_id'] != feedback.user.id or "user_id" not in session:
        flash('You do not have permission to that resource')
        return render_template('login.html')
    
    feedback = Feedback.query.get_or_404(feedback_id)

    db.session.delete(feedback)
    db.session.commit()

    redirect(f'/users/{feedback.user.username}')
    