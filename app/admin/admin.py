import os, csv
from datetime import datetime
from flask import (Blueprint, redirect, render_template, request, session,
                   url_for, current_app, send_file)
# from sklearn.externals.joblib.externals.cloudpickle.cloudpickle import instance
from werkzeug.utils import secure_filename

from app import db
from app.models import AdminLoginForm, UploadForm, User, Mass

admin_bp = Blueprint("admin_bp", __name__, template_folder='templates', 
    static_folder='/assets', static_url_path='../general/static')

admin = 'stbccadmin'
password = 'thefortunate1'


@admin_bp.route('/', methods=['POST', 'GET'])
def index():
    upload_form = UploadForm()
    admin_form = AdminLoginForm()
    if request.method == 'GET':
        if 'isadmin' in session:
            return render_template('admin/index.html', form=upload_form)
        return render_template('admin/login.html', form=admin_form)
    if request.method == 'POST':
        if admin_form.validate_on_submit():
            if admin_form.username.data == admin and admin_form.password.data == password:
                session['isadmin'] = True
                return redirect(url_for('.index'))
    return '404'    

@admin_bp.route('/upload', methods=['POST'])
def upload():
    form = UploadForm()
    if request.method == 'POST' and session['isadmin']:
        if form.validate_on_submit():
            f = form.file.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(current_app.instance_path, 'temp_files', filename))
            
            with open(os.path.join(current_app.instance_path, 'temp_files', filename),'r') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                log_file = open(os.path.join(current_app.instance_path, 'temp_files', 'logfile.txt'),'w+')
                for row in csv_reader:
                    print("{}, {}".format(row['Contact Number'], row['First Name']))
                    user = User.query.filter_by(number=row['Contact Number'])
                    if user:
                        dob = datetime.strptime(row['Date of Birth'],'%d/%m/%Y')
                        new_user = User(number=row['Contact Number'], l_name=row['Last Name'],
                                        f_name=row['First Name'], o_name=row['Other Names'], dob=dob,
                                        age=row['Age'], gender=row['Gender'], address=row['Residential Address'],
                                        emergency=row['Emergency Contact'], day_group=row['Day Group'])
                        db.session.add(new_user)
                        db.session.commit()
                        log_file.writelines('{} {}, {}: Succesfully added to db'.format(row['First Name'],
                            row['Last Name'], row['Contact Number']))
                    else:
                        log_file.writelines('{} {}, {}: already exists in db'.format(row['First Name'],
                            row['Last Name'], row['Contact Number']))
                log_file.close()
            return send_file(os.path.join(current_app.instance_path, 'temp_files', 'logfile.txt'), as_attachment=True)
            return redirect(url_for('.index'))
    return '404'


@admin_bp.route('/dumpdb', methods=['GET'])
def dumpdb():
    if request.method == 'GET' and session['isadmin']: 
        database = open(os.path.join(current_app.instance_path, 'temp_files', 'database.csv'),'w+')

        user = User.query.all()

        with database as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', 
                quotechar='"', quoting=csv.QUOTE_ALL)
            fieldnames = ['Contact Number','Last Name','First Name','Other Names','Date of Birth','Age','Gender',
                    'Residential Address','Emergency Contact','Day Group']
            csv_writer.writerow(fieldnames)
            for member in user:
                csv_writer.writerow([member.number, member.l_name, member.f_name, member.o_name, member.dob, 
                    member.age, member.gender, member.address, member.emergency, member.day_group])
        
        return send_file(os.path.join(current_app.instance_path, 'temp_files', 'database.csv'), as_attachment=True)
        return redirect(url_for('.index')) 
    return '404'

@admin_bp.route('/dumpmass/<mass_id>', methods=['GET'])
def dumpmass(mass_id):
    if request.method == 'GET' and session['isadmin']:
        mass = Mass.query.filter_by(name=mass_id).first()
        if mass:
            file = open(os.path.join(current_app.instance_path, 'temp_files', '{}.csv'.format(mass_id)),'w+')
            
            with file as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',', 
                    quotechar='"', quoting=csv.QUOTE_ALL)
                
                csv_writer.writerow(['First Name', 'Last Name', 'Contact Number'])
                
                participants = mass.participants.split(',')
                print(participants)
                for participant in participants:
                    user = User.query.filter_by(number=participant).first()
                    if user:
                        csv_writer.writerow([user.f_name, user.l_name, user.number])

            return send_file(os.path.join(current_app.instance_path, 'temp_files', '{}.csv'.format(mass_id)), as_attachment=True)
            return redirect(url_for('.index')) 
    return '404'        


@admin_bp.route('/resetmasses', methods=['GET'])
def resetmasses():
    if request.method == 'GET' and session['isadmin']:
        masses = Mass.query.all()

        for mass in masses:
            mass.participants = ' '
            mass.number_remaining = 80
            db.session.commit()
        
        users = User.query.all()
        for user in users:
            user.mass_booked = None
            db.session.commit()

        return redirect(url_for('.index'))
    return '404'