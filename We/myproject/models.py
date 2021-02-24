from myproject import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    ################################################################
    user_history = db.relationship('UserHistory', backref='user', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash, password)

class ForgotPassword(db.Model):

    __tablename__ = 'forgotpass'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    email = db.Column(db.String(64), unique=True, index=True)
    otp = db.Column(db.Integer)

    def __init__(self, email, otp):
        self.email = email
        self.otp = otp


class UserHistory(db.Model):

    ###################################
    users = db.relationship(User)
    ###################################

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64))
    score = db.Column(db.String(64))
    attempted_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, tag, score, user_id):
        self.tag = tag
        self.score = score
        self.user_id = user_id


class Quiz(db.Model):

    # Creating python quiz question table
    __tablename__ = 'python_quiz'

    id = db.Column(db.Integer, primary_key = True)
    tag = db.Column(db.String(512))
    question = db.Column(db.String(512))
    option_a = db.Column(db.String(512))
    option_b = db.Column(db.String(512))
    option_c = db.Column(db.String(512))
    option_d = db.Column(db.String(512))
    answer = db.Column(db.String(512))

    def __init__(self, tag, question, option_a, option_b, option_c, option_d, answer):
        self.tag = tag
        self.question = question
        self.option_a = option_a
        self.option_b = option_b
        self.option_c = option_c
        self.option_d = option_d
        self.answer = answer
