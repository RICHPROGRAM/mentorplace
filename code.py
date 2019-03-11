from flask import Flask, render_template, flash, request, session, url_for, Markup, redirect, send_from_directory, json
from werkzeug.utils import secure_filename
import os
import json
from model import *
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/tll'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'qwertyuioplkjhgfdsazxcvbnm'

db = SQLAlchemy(app)

UPLOAD_FOLDER = 'static/image'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4' ''])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    posts = Consultants.query.all()
    categories = Category.query.all()
    return render_template("home.html", posts=posts, categories=categories)

@app.route("/test")
def test():
    return render_template("basic.html")

@app.route("/profile/<username>")
def profile(username):
    post = Consultants.query.filter_by(username=username).first()
    return render_template("profile.html", post=post)

@app.route("/appointment/<username>",  methods=['GET', 'POST'])
def appointment(username):
    post = Consultants.query.filter_by(username=username).first()
    if request.method == "post":
       print("post method")
       if session['logged_in']== True:
          print("post metho")
          username = db.Column(db.String(100))
          user_email = db.Column(db.String(100))
          user_contact = db.Column(db.String(100))
          cons_username = post.username
          cons_email = post.email
          cons_contact = post.contact
          cons_fees = post.price
          cons_availability = post.availability
          appointment_date = db.Column(db.DateTime)
          appointment_time = db.Column(db.DateTime)
          appointment_duration = db.Column(db.String(100))
          amount = appointment_duration * cons_fees
          queries = request.form.get('queries')
          post = Appointment(username=username, user_email=user_email, user_contact=user_contact, cons_username=cons_username, cons_email=cons_email, cons_contact = cons_contact,
                             cons_fees=cons_fees, cons_availability = cons_availability, appointment_date=appointment_date, appointment_time=appointment_time,
                             appointment_duration=appointment_duration, amount=amount, quesries =queries)
          db.session.add(post)
          db.session.commit()
       else:
          print('xyz')
          return render_template("appointment.html", post=post, user_login = False)
    return render_template("appointment.html", post=post)


@app.route("/login")
def login():
    if request.method == "post":
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email, password=password).first()
        if user is None:
           error ='Username or Password is invalid'
           return render_template('login.html', error = error)
        else:
           session['logged_in'] = True
           return redirect(url_for('home'))
    return render_template("login.html")

@app.route("/signup")
def signup():
    if request.method == "post":
        username = request.method.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('input_password')
        conf_password = request.form.get('input_conf_password')

        check_email = Users.query.filter_by(email=email).first()
        if (password == conf_password) and check_email is None:
           post = Users(username=username, email=email, phone=phone, password =password)
           db.session.add(post)
           db.session.commit()
    return render_template("registration.html")

@app.route("/category", methods=['GET', 'POST'])
def category():
    post = Consultants.query.all()
    return render_template("category_list.html", posts=post)

@app.route("/new_category", methods=['GET', 'POST'])
def add_category():
    filename = ""
    if request.method == 'POST':
        try:
            file = request.files['image']
            print(file)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                filename = request.form.get('image')
        except Exception as e:
            print("Form without file " + str(e))
        category_name = request.form.get('category_name')
        description = request.form.get('description')
        image = filename
        post = Category(category_name=category_name, description=description, image=image)
        db.session.add(post)
        db.session.commit()
    return render_template("new_category.html")

@app.route("/become_a_mentor", methods=['GET', 'POST'])
def mentor():
    filename=""
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        bio = request.form.get('bio')
        qualification = request.form.get('qualification')
        background = request.form.get('background')
        category = request.form.get('category')
        languages = request.form.get('languages')
        skills = request.form.get('skills')
        specialities = request.form.get('specialities')
        os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], name))
        try:
            file = request.files['photo']
            print(file)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], name, filename))
            else:
                filename = request.form.get('photo')
        except Exception as e:
            print("Form without file " + str(e))

        post = Consultants( username=username, name = name, image=filename, bio=bio, qualification=qualification, background=background, category=category, languages =languages, skills=skills, specialities=specialities)
        db.session.add(post)
        db.session.commit()
    return render_template("become_an_advisor.html")

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username=='Jain' and password=='Richa':
            session['username'] = username
            session['logged_in'] = True

    if 'username' in session and session['username'] == 'Jain':
        #posts = db.session.query(Appointments).all()
        consultants = db.session.query(Consultants).all()
        return render_template('dashboard.html', consultants=consultants)
    else:
        return render_template('login.html')

if __name__== "__main__":

 app.run()
