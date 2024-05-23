from db import db
from models import Task, User
from main import flaskapp as app
import csv
from datetime import datetime

def seed_database():
    """
    Seeds the database with tasks and users from the data directory
    """
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()

        # Seed users from CSV
        with open('data/users.csv', "r") as file:
            csv_reader = csv.reader(file, delimiter=',')
            # skip header
            next(csv_reader)
            for row in csv_reader:
                obj = User(username=row[0],password=row[1],last_name=row[2], first_name=row[3])
                db.session.add(obj)
        db.session.commit()

        with open('data/tasks.csv', "r") as file:
            csv_reader = csv.reader(file, delimiter=",")
            # skip header
            next(csv_reader)
            for row in csv_reader:
                obj = Task(name=row[0], desc=row[1], user_id=row[4], start_date=datetime.now())
                db.session.add(obj)
        db.session.commit()


if __name__ == "__main__":
    seed_database()
