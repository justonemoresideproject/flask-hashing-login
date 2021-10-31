from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """Model for a user"""

    __tablename__ = 'users'

    # username - a unique primary key that is no longer than 20 characters.
    # password - a not-nullable column that is text
    # email - a not-nullable column that is unique and no longer than 50 characters.
    # first_name - a not-nullable column that is no longer than 30 characters.
    # last_name - a not-nullable column that is no longer than 30 characters.

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(20), nullable=False, unique=True)

    password = db.Column(db.Text, nullable=False, unique=False)

    email = db.Column(db.String(50), nullable=False)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""
        # this one does not work at all. Returns a 'TypeError: initializer for ctype 'char' must be a bytes of length 1, not str'
        hashed = bcrypt.generate_password_hash(pwd)

        # below works, but then authentication fails
        # hashed = bcrypt.generate_password_hash(f'b{pwd}')

        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False