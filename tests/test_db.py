from app.models import Mass, User, db
from datetime import datetime

def test_db(app, client):
    with app.app_context():
        masses = Mass.query.all()
        first_mass = Mass.query.filter_by(name='first_mass').first()
        assert masses != None
        assert first_mass.name == 'first_mass'


def test_user(app, client):
    with app.app_context():
        dob = datetime.strptime('4/23/1990','%m/%d/%Y')
        user = User(number='240216169',l_name='Johnson',f_name='Jesse',dob=dob,age=30,gender='Male',address='Sakumono',emergency='240216169',day_group='Monday')
        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(number='240216169').first()

        assert user.number == '240216169'