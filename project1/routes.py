from flask import render_template, url_for, flash, redirect, request
from project1 import app, db, bcrypt
from project1.models import User, File
from project1.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user,current_user
from project1.s3 import S3
from werkzeug.utils import secure_filename

downloads = [
    {
        'file_name': 'Download File',
        'download_date': '10/19/2019',
        'download_time': '15:20:12',
        'last_update': '10/19/2019',
        'description': 'This is my download file'
    },
    {
        'file_name': 'Download File2',
        'download_date': '10/19/2019',
        'download_time': '15:20:12',
        'last_update': '10/19/2019'
    }
]

s3 =S3()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/user')
def user():
    return render_template('user.html',downloads=downloads)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data, passwrd=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!',' success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.passwrd, form.password.data):
            login_user(user,remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Incorrect Email/Password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/upload_file', methods=['GET','POST'])
def upload_file():
    s3 = S3()
    if request.method == 'POST':
        if request.files:
            user_file = request.files['file']
            filename = secure_filename(user_file.filename)
            object_name = current_user.email+"/"+filename
            #Send to bucket
            print(filename)
            print(object_name)
            print(current_user.email)
            s3.upload(user_file, object_name, current_user.email)
            #Push to DB
            #upload_file = File(name=user_file,description=request.form['description'])
            print(request.form['description'])
            print(user_file)
        
            return redirect(url_for('user'))

    #return render_template('user.html')
