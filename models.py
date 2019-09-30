from app import db
from datetime import datetime


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    explanation = db.Column(db.String(200), nullable=True)
    questions = db.relationship('Question', backref='poll', lazy=True)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    text = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    test_choices = db.relationship('TestChoice', backref='question', lazy=True)


class TestChoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    text = db.Column(db.String(100))
