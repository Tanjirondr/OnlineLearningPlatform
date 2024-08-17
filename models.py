from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///default.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return app

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    credits = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    enrollments = db.relationship('Enrollment', backref='course', lazy='dynamic')
    
    def __repr__(self):
        return f'<Course {self.title}>'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    enrollments = db.relationship('Enrollment', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    enrolled_on = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Enrollment User: {self.user_id}, Course: {self.course_id}>'

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)