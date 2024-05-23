from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from db import db

class User(db.Model, UserMixin):
    """
    id = auto-generated primary key (int)
    username = user's username. cannot be null and must be unique (str)
    password = user's password. cannot be null (str)
    last_name = user's real last name. cannot be null (str)
    first_name = user's real first name. cannot be null (str)
    tasks = relationship to the Task table, back-populated
    categories = relationship to the Category table, back-populated
    """
    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    last_name = Column(String(80), nullable=False)
    first_name = Column(String(80), nullable=False)
    tasks = relationship("Task", back_populates="user")
    categories = relationship("Category", back_populates="user")

class Task(db.Model):
    """
    id = auto-generated primary key (int)
    name = task title, cannot be null (str)
    desc = task description (str)
    start_date = time of creation (timestamp)
    end_date = due date (timestamp)
    user_id = foreign key from User table (int)
    category_id = foreign key from Category table (int)
    user = relationship to User table, back-populated
    category = relationship to Category table, back-populated
    """
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    desc = Column(String(200))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    category_id = Column(Integer, ForeignKey('category.id'),default=1)
    user = relationship("User", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")

class Category(db.Model):
    """
    id = auto-generated primary key (int)
    name = category name, cannot be null (str)
    desc = category description (str)
    user_id = foreign key from User table (int)
    user = relationship to User table, back-populated
    tasks = relationship to Task table, back-populated
    """
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="categories")
    tasks = relationship("Task", back_populates="category")

# Ensure to create the database and tables
if __name__ == "__main__":
    db.create_all()
