from flaskpage import db
from datetime import datetime

class Developer(db.Model):
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False)
    username=db.Column(db.String(100),nullable=False,primary_key=True)
    phone_number=db.Column(db.String(20),nullable=False)
    domain=db.Column(db.String(100),nullable=False)
    github_link=db.Column(db.String(200),nullable=False)
    linkedin_link=db.Column(db.String(200),nullable=False)
    experience=db.Column(db.String(100))
    password=db.Column(db.String(100),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"Developer('{self.name}', '{self.email}', '{self.username}', '{self.phone_number}', '{self.date_created}')"

class Client(db.Model):
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False)
    username=db.Column(db.String(60),nullable=False,primary_key=True)
    phone_number=db.Column(db.String(20),nullable=False)
    password=db.Column(db.String(60),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"Client('{self.name}', '{self.email}', '{self.username}', '{self.phone_number}', '{self.date_created}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
