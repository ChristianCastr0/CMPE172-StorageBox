from datetime import datetime
from project1 import db, lm
from flask_login import UserMixin

@lm.user_loader
def load_user(user_email):
    return User.query.get(user_email)


class User(db.Model, UserMixin):
    email = db.Column(db.String(50), nullable=False, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    passwrd = db.Column(db.String(60), nullable=False)
    uploads = db.relationship('File', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"

    def get_id(self):
           return (self.email)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.String(100))
    user_id = db.Column(db.String(50), db.ForeignKey('user.email'), nullable=False)

    def __repr__(self):
        return f"File('{self.name}', '{self.upload_date}')"