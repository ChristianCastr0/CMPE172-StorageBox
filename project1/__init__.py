from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

application = app = Flask(__name__)
app.config['SECRET_KEY'] = '662ed1f1885260069d4cebb56fa3826a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:password@database-2.crikhltf86tj.us-west-1.rds.amazonaws.com/Users'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
lm = LoginManager(app)

from project1 import routes