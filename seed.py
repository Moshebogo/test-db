from faker import Faker
from app import app
from models import db


fake = Faker()


if __name__ == '__main__':
    with app.app_context():
        

        boat_names = []

