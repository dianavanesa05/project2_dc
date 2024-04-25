from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Comments, User

class CommentsOtherProfileForm(FlaskForm):
    comments = StringField('Comment')
    submit = SubmitField(label='Post a comment')

class CommentsForm(FlaskForm):
    comments = StringField('Comment')
    submit = SubmitField(label=('Post a comment'))

class ProfileForm(FlaskForm):
    fName = StringField('First Name', validators=[DataRequired()])
    lName = StringField('Last Name', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    submit = SubmitField(label=('Edit Profile'))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
