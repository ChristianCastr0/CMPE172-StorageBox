from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
import pymysql
from forms import RegistrationForm, LoginForm
#from models import User, Post
from flask_bcrypt import Bcrypt

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
app = Flask(__name__)
app.config['SECRET_KEY'] = '662ed1f1885260069d4cebb56fa3826a'
#app.config['SQLALCHEMY_DATABASE_URI'] = "database-2.crikhltf86tj.us-west-1.rds.amazonaws.com"
bcrypt = Bcrypt(app)


REGION = 'us-west-1b'
rds_host  = "database-2.crikhltf86tj.us-west-1.rds.amazonaws.com"
name = "admin"
password = "password"
db_name = "Users"

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/user')
def user():
    return render_template('user.html',downloads=downloads)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
        with conn.cursor() as cur:
            cur.execute("insert into user values('%s', '%s', '%s', '%s')" % (form.email.data, form.first_name.data, form.last_name.data, hashed_password))
            conn.commit()
            cur.close()
        flash(f'Your account has been created!',' success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'pass':
            flash('Successful Login!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect Email/Password', 'danger')
    return render_template('login.html', title='Login', form=form)
if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)