from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError


class LoginForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Full Name(For Certificate)', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self, field):
        # Check if not None for that user email!
        if Admin.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')
    #
    # def check_username(self, field):
    #     # Check if not None for that username!
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError('Sorry, that username is taken!')

class NewLeadForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    mobile = StringField('Mobile', validators=[DataRequired()])
    leadfrom = StringField('Lead From')
    handleby = StringField('Handling By')
    status = StringField('Status', validators=[DataRequired()])
    comment = StringField('Comment', validators=[DataRequired()])

    submit = SubmitField('Add!')
