from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User
from datetime import datetime, date

#Übernommen aus den Beispielen
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

#Übernommen aus den Beispielen
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

#Übernommen aus den Beispielen
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

#Übernommen aus den Beispielen
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

#Übernommen aus den Beispielen        
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

#Übernommen aus den Beispielen
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

#Übernommen aus den Beispielen
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

#Übernommen aus den Beispielen
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

# zu löschen
class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')

#Übernommen aus den Beispielen
class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

#Übernommen aus den Beispielen
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

#Eigenentwicklung
class CreateTeam(FlaskForm):
    teamname = StringField('Teamname', validators=[DataRequired()])
    beschreibung = StringField('Beschreibung', validators=[DataRequired()])
    submit = SubmitField('Create Team')

class CreateTermin(FlaskForm):
    terminname = StringField('Terminname', validators=[DataRequired()])
    beschreibung = StringField('Beschreibung', validators=[DataRequired()])
    datum = DateField('Datum', format='%Y-%m-%d', validators=[DataRequired()])
    zeit = TimeField('Zeit', validators=[DataRequired()])
    submit = SubmitField('Termin erstellen')

    '''def validate_datum(self, datum):
        datum = date.today()
        if self.datum < datum:
            raise ValidationError('Der Termin kann nicht in der Vergangenheit liegen.')'''