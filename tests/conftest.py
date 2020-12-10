import pytest

from app.models import Mass
from app import create_app, db
from dotenv import load_dotenv, find_dotenv

#loading .env file for local testing 

load_dotenv(find_dotenv())




flask_app = create_app()

with flask_app.app_context():
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


@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()