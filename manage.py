import app
from app import db
from app.models import Mass

app = app.create_app()

with app.app_context():
    db.create_all()
    first_mass = Mass(name='first_mass', participants=' ',number_remaining=80)
    second_mass = Mass(name='second_mass', participants=' ',number_remaining=80)
    third_mass = Mass(name='third_mass', participants=' ',number_remaining=80)
    fourth_mass = Mass(name='fourth_mass', participants=' ',number_remaining=80)

    db.session.add(first_mass)
    db.session.add(second_mass)
    db.session.add(third_mass)
    db.session.add(fourth_mass)
    db.session.commit()
    print('Done!')