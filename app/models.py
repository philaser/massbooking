from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from sqlalchemy.sql.expression import column
from wtforms import RadioField, StringField, PasswordField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange
import requests
from app import db
import os


class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class UploadForm(FlaskForm):
    file = FileField('Upload file to database',validators=[FileRequired()])

class CheckInForm(FlaskForm):
    number = StringField('Number', validators=[Length(min=10, max=10, message='Number must be 10 digits')])

class BookingForm(FlaskForm):
    masses = RadioField('Please select the mass you want to attend', 
        choices=[(('second_mass','Sunday 07:00am'),
        ('third_mass','Sunday 09:30am')], validators=[DataRequired()])

class RegisterForm(FlaskForm):
    number = StringField('Phone number', validators=[DataRequired(), Length(min=10, max=10, message='Number must be 10 digits')])
    l_name = StringField('last name', validators=[DataRequired()])
    f_name = StringField('First name', validators=[DataRequired()])
    o_name = StringField('Other names')
    # datefield only works with below format else it will not validate
    dob = DateField('Date of birth', format='%Y-%m-%d', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(max=120, message='Please enter a valid age')])
    gender = RadioField('Gender', choices=[('male','Male'),('female','Female')], validators=[DataRequired()])
    address = StringField('Residential address', validators=[DataRequired()])
    emergency = StringField('Emergency contact', validators=[DataRequired(), Length(min=10, max=10, message='Number must be 10 digits')])
    day_group = RadioField('Day group', choices=[('Monday','Monday'), ('Tuesday','Tuesday'), ('Wednesday','Wednesday'), 
        ('Thursday','Thursday'), ('Friday','Friday'), 
        ('Saturday','Saturday'), ('Sunday', 'Sunday')], validators=[DataRequired()])


class User(db.Model):
    number = db.Column(db.String(10), primary_key=True)
    l_name = db.Column(db.String(80), nullable=False)
    f_name = db.Column(db.String(80), nullable=False)
    o_name = db.Column(db.String(80))
    dob = db.Column(db.Date,nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    address= db.Column(db.String, nullable=False)
    emergency= db.Column(db.String, nullable=False)
    day_group= db.Column(db.String, nullable=False)
    mass_booked = db.Column(db.String)

    def __repr__(self):
        return 'User {}'.format(self.number)


class Mass(db.Model):
    name = db.Column(db.String, primary_key=True)
    participants = db.Column(db.Text)
    number_remaining = db.Column(db.Integer)


    def __repr__(self):
        return 'User {}'.format(self.name)





def sendMessage(number, f_name, l_name, mass_id ):
    api_key = os.environ['MNOTIFY_API_KEY']
    name = '{} {}'.format(f_name, l_name)
    mass_name = {'first_mass':'Saturday 6:00pm', 'second_mass':'Sunday 7:00am', 
        'third_mass':'Sunday 9:30am', 'fourth_mass':'Sunday 11:00am'}
    mass = mass_name[mass_id]
    num = [number]
    url = "https://api.mnotify.com/api/sms/quick?key=" + api_key
    payload = {'recipient':num, 'sender':'StBakhita', 'message':'Hello {} your booking for Mass on {} is confirmed. Be on time to go through all safety protocols. Thanks.'.format(name, mass)}

    r = requests.post(url, json=payload)
    print(r.content)
    return r.status_code

