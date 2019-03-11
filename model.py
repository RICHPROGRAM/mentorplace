from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Users(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    phone = db.Column(db.String(15))

class Consultants(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    name = db.Column(db.String(100))
    bio = db.Column(db.String(100))
    qualification = db.Column(db.String(100))
    background = db.Column(db.String(100))
    category = db.Column(db.String(100))
    languages = db.Column(db.String(100))
    skills = db.Column(db.String(100))
    specialities = db.Column(db.String(100))
    image = db.Column(db.String(100))

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    message = db.Column(db.String(100))

class Category(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    image =db.Column(db.String(100))

class Appointment(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    user_email = db.Column(db.String(100))
    user_contact = db.Column(db.String(100))
    cons_username = db.Column(db.String(100))
    cons_email = db.Column(db.String(100))
    cons_contact = db.Column(db.String(100))
    cons_fees = db.Column(db.String(100))
    cons_availability= db.Column(db.String(100))
    appointment_date = db.Column(db.DateTime)
    appointment_time = db.Column(db.DateTime)
    appointment_duration = db.Column(db.String(100))
    amount = db.Column(db.String(100))
    queries = db.Column(db.String(100))
