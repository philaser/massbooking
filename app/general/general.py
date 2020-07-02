
from flask import Blueprint
from flask import render_template, redirect, request, url_for, session
from app.models import CheckInForm, BookingForm, RegisterForm, User, Mass, sendMessage
from app import db

general_bp = Blueprint("general_bp", __name__,template_folder='templates',
    static_url_path='/assets',static_folder='static')




@general_bp.route("/", methods=['POST', 'GET'])
def index():
    form = CheckInForm()
    if request.method == 'GET':
        return render_template('general/index.html', form=form)
    return '404 Something bad happened. Please contact the Administrator'

    
@general_bp.route("/checkin", methods=['POST'])
def checkin():
    if request.method == 'POST':
        form = CheckInForm()
        if form.validate_on_submit():
            user = User.query.filter_by(number=form.number.data).first()
            if user != None:
                session['number'] = user.number
                return redirect(url_for('.book'))
            return redirect(url_for('.register'))
    return '404 Something bad happened. Please contact the Administrator'


@general_bp.route("/register", methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('general/register.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user = user = User.query.filter_by(number=form.number.data).first()
            if user != None:
                return render_template('general/userexists.html')

            user = User(number=form.number.data, l_name=form.l_name.data,
                f_name=form.f_name.data, o_name=form.o_name.data, dob=form.dob.data,
                age=form.age.data, gender=form.gender.data, address=form.address.data,
                emergency=form.emergency.data, day_group=form.day_group.data)
            db.session.add(user)
            db.session.commit()
            session['number'] = form.number.data
            return redirect(url_for('.book'))
    return '404 Something bad happened. Please contact the Administrator'



@general_bp.route("/book", methods=['POST', 'GET'])
def book():
    form = BookingForm()
    number = session['number']
    user = User.query.filter_by(number=number).first()
    mass_name = {'first_mass':'Saturday 07:00pm', 'second_mass':'Sunday 07:00am', 
                'third_mass':'Sunday 09:00am', 'fourth_mass':'Sunday 11:00am'}
    # getting the remaining number of slots per mass
    mass_data = {}
    masses = Mass.query.all()
    for mass in masses:
        mass_data[mass_name[mass.name]]  = mass.number_remaining
    
    print(mass_data['Saturday 07:00pm'])

    if request.method == 'GET':
        if user.mass_booked != None:
            return render_template('general/bookingconfirmation.html', mass = mass_name[user.mass_booked])
        return render_template('general/booking.html', form=form, mass_data = mass_data)
    elif request.method == 'POST':
        if form.validate_on_submit():
            data = form.masses.data
            mass = Mass.query.filter_by(name=data).first()
            if mass.number_remaining == 0:
                return render_template('general/massfull.html')
            user.mass_booked = data
            mass.participants = mass.participants + ',{}'.format(user.number)
            mass.number_remaining = mass.number_remaining - 1
            db.session.commit()
            message = sendMessage(user.number, user.f_name, user.l_name, user.mass_booked)
            print(message)
            return render_template('general/bookingconfirmation.html', mass = mass_name[user.mass_booked])
    return '404 Something bad happened. Please contact the Administrator'