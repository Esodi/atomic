#!/usr/bin/python3

# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Enum

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'  # Explicitly set the table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    competitions = relationship('UserCompetition', back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'

class Competition(db.Model):
    __tablename__ = 'competitions'  # Explicitly set the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    details = db.Column(db.Text)
    fee = db.Column(db.Float)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)  # Date of the competition
    location = db.Column(db.String(255), nullable=False)  # Location of the competition
    prizes = db.Column(db.Text, nullable=True)  # Description of the prizes for the competition
    participants = relationship('UserCompetition', back_populates='competition')

    def __repr__(self):
        return f'<Competition {self.name}>'



class UserCompetition(db.Model):
    __tablename__ = 'user_competitions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    competition_id = db.Column(db.Integer, db.ForeignKey('competitions.id'), nullable=False)
    status = db.Column(Enum('joined', 'participant', 'winner', name='user_competition_status'), default='joined')
    project_description = db.Column(db.Text)
    project_file_name = db.Column(db.String(255))
    project_file_data = db.Column(db.LargeBinary)
    project_file_mimetype = db.Column(db.String(255))
    submission_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = relationship('User', back_populates='competitions')
    competition = relationship('Competition', back_populates='participants')

    def __repr__(self):
        return f'<UserCompetition {self.user_id} - {self.competition_id}>'