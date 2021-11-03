from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, UserForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_hashing_login"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/')
def redirect_to_reg():
    return redirect ('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if 'username' in session:
        redirect(f'/users/{session["username"]}')

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.commit()

        user = User.query.filter_by(username=username).first()
        session['username'] = username
        return redirect('/secret')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # if 'user_id' in session:
    if "username" in session:
        redirect(f'/users/{session["username"]}')

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            session["username"] = user.username
            return redirect("/secret")
        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)
        
@app.route('/secret')
def secret():
    if "username" not in session:
        flash('You do not have permission to that resource')
        return redirect('login.html')
    return redirect(f'/users/{session["username"]}')

@app.route('/users/<username>')
def get_user(username):
    if "username" not in session:
        flash('You do not have permission to that resource')
        return redirect('/login')
    user = User.query.filter_by(username=f'{username}').first()

    return render_template('user.html', user=user)

@app.route('/users/<username>/update', methods=['GET', 'POST'])
def edit_user(username):
    user = User.query.filter_by(username=username).first()
    if "username" not in session or session["username"] != user.username:
        flash('You do not have permission to that resource')
        return redirect('/login')

    user = User.query.filter_by(username=username).first()
    form = UserForm(obj=user)
    return render_template('editUser.html', form=form, user=user)
    

@app.route('/logout')
def logout():
    session.pop('username')
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    user = User.query.filter_by(username=username).first()
    form = FeedbackForm()
    if "username" not in session:
        flash('You do not have permission to that resource')
        return render_template('login.html')
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content, user_id=user.id)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f'/users/{username}')
    return render_template('addFeedback.html', user=user, form=form)

@app.route('/users/<username>/delete', methods=['GET', 'POST'])
def delete_user(username):
    if session['username'] != feedback.user.username or "username" not in session:
        flash('You do not have permission to that resource')
        return render_template('login.html')

    db.session.delete(feedback)
    db.session.commit()


@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    form = FeedbackForm(obj=feedback)

    if session['username'] != feedback.user.username or "username" not in session:
        flash('You do not have permission to that resource')
        return render_template('login.html')

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.add(feedback)
        db.session.commit()

        return redirect(f'/users/{session["username"]}')
        
    return render_template('editFeedback.html', form=form)

@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def deleteBack(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if session['username'] != feedback.user.username or "username" not in session:
        flash('You do not have permission to that resource')
        return render_template('login.html')

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f'/users/{feedback.user.username}')
    