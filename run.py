from flask import Flask,render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import openpyxl
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import email_validator
from flask_bcrypt import Bcrypt

class DeveloperForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    username=StringField('Username',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    phone_number = StringField('Phone Number',validators=[DataRequired()])
    domain = SelectField('Domain', choices=['Web Developer','Graphics Designer','Digital Marketing','Video Editing'], validators=[DataRequired()])
    github_link = StringField('Github Link', validators=[DataRequired()])
    linkedin_link = StringField('Linkedin Link', validators=[DataRequired()])
    experience = StringField('Experience', validators=[DataRequired()])
    password= StringField('Password', validators=[DataRequired()])
    confirm_password= StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_phone_number(self, phone_number):
        dev = Developer.query.filter_by(phone_number=phone_number.data).first()
        if dev:
            raise ValidationError('That phone number is taken. Please choose a different one.')
            
    def validate_username(self, username):
        dev = Developer.query.filter_by(username=username.data).first()
        if dev:
            raise ValidationError('That username is taken. Please choose a different one.')

class ClientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    username=StringField('Username',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    confirm_password= StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_phone_number(self, phone_number):
        client = Client.query.filter_by(phone_number=phone_number.data).first()
        if client:
            raise ValidationError('That phone number is taken. Please choose a different one.')
            
    
    def validate_username(self, username):
        client = Client.query.filter_by(username=username.data).first()
        if client:
            raise ValidationError('That username is taken. Please choose a different one.')
        
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_username(self, username):
        dev = Developer.query.filter_by(username=username.data).first()
        if not dev:
            raise ValidationError('That username is not registered. Please register first.')
        
dir_path = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)
app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app) 
bcrypt=Bcrypt(app)


class Developer(db.Model):
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False)
    username=db.Column(db.String(100),nullable=False)
    phone_number=db.Column(db.String(20),nullable=False,primary_key=True)
    domain=db.Column(db.String(100),nullable=False)
    github_link=db.Column(db.String(200),nullable=False)
    linkedin_link=db.Column(db.String(200),nullable=False)
    experience=db.Column(db.String(100))
    password=db.Column(db.String(100),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Developer %r>' % self.name

class Client(db.Model):
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False)
    username=db.Column(db.String(60),nullable=False)
    phone_number=db.Column(db.String(20),nullable=False,primary_key=True)
    password=db.Column(db.String(60),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Client %r>' % self.name

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html',template_folder='templates')

@app.route('/developer', methods=['GET', 'POST'])
def developer(): 
    form=DeveloperForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_developer = Developer(name=form.name.data, 
                                  email=form.email.data, 
                                  username=form.username.data,
                                  phone_number=form.phone_number.data,
                                  domain=form.domain.data,
                                  github_link=form.github_link.data,
                                  linkedin_link=form.linkedin_link.data,
                                  experience=form.experience.data,
                                  password=hashed_password)
        with app.app_context():
            db.session.add(new_developer)
            db.session.commit()
        
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('developer.html',template_folder='templates', form=form)

@app.route('/client', methods=['GET', 'POST'])
def client():
    form=ClientForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_client = Client(name=form.name.data, 
                            email=form.email.data,
                            username=form.username.data, 
                            phone_number=form.phone_number.data,
                            password=hashed_password)
        with app.app_context():
            db.session.add(new_client)
            db.session.commit()
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('home'))
    
    return render_template('client.html',template_folder='templates',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        dev = Developer.query.filter_by(username=form.username.data).first()
        client = Client.query.filter_by(username=form.username.data).first()
        password_dev = Developer.query.filter_by(password=form.password.data).first()
        if dev is None and client is None:
            flash('That username is not registered. Please register first.')
            return redirect(url_for('home'))
        if ((dev and bcrypt.check_password_hash(password_dev, form.password.data))|(client and bcrypt.check_password_hash(password_dev, form.password.data))):
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html',template_folder='templates',form=form)


if __name__ == '__main__':
    app.run()
    
