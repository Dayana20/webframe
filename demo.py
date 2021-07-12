from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, BooleanField
# from wtforms.validators import DataRequired, Length, Email, EqualTo


app = Flask(__name__)                    # this gets the name of the file so Flask knows it's name
app.config['SECRET_KEY'] = '67414c2f94271f30852f5623dbeb57b3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"


@app.route("/")                          # this tells you the URL the method below is related to
def home():
    return render_template('home.html', subtitle='Home Page')


@app.route("/about")                          # this tells you the URL the method below is related to
def about():
    return render_template('about.html', subtitle='About Page')
  
# @app.route("/register")                          # this tells you the URL the method below is related to
# def register():
#     # form = RegistrationForm()
#     return render_template('register.html', subtitle='Register Form')
  
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)
  
''' To View Users: run python3
>>> from app_py_file_name import db
>>> from app_py_file_name import User
>>> User.query.all()'''
  
  
@app.route("/second_page")
def second_page():
    return render_template('second_page.html', subtitle='Second Page', text='This is the second page')
  
# put to byass manual environment variable setting
if __name__ == '__main__':               # this should always be at the end
    app.run(host="0.0.0.0")