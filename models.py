from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db import db

"""
This is object oriented programming.
Here, we're defining two critical "objects" (things) that we're going to regularly use (Users and Tasks)
Doing it this way, we can ensure they are consistently created, accessed, and modified
"""


class User(db.Model):
    """"
    id = auto-generated primary key (int)
    first_name = user's real first name. cannot be null (str)
    last_name = user's real last name. cannot be null (str)
    tasks = relationship to the Task table, back-populated
    """
    id = Column(Integer, primary_key=True)
    last_name = Column(String(80), nullable=False)
    first_name = Column(String(80), nullable=False)
    tasks = relationship("Task", back_populates="user")


class Task(db.Model):
    """"
    id = auto-generated primary key (int)
    name = task title, cannot be null (str)
    desc = task description (str)
    start_date = time of creation (timestamp) - NOT YET IMPLEMENTED
    end_date = due date (timestamp) - NOT YET IMPLEMENTED
    user_id = foreign key from User table (int)
    user = relationship to User table, back-populated
    """
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    desc = Column(String(200))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, back_populates="tasks")
