from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from converter import printWAV # get speech recognition function
import time, random, threading
from turbo_flask import Turbo # pip3 install turbo-flask
from flask_bcrypt import Bcrypt #for password (pip install flask-bcrypt)


app = Flask(__name__)                    # this gets the name of the file so Flask knows it's name
app.config['SECRET_KEY'] = '67414c2f94271f30852f5623dbeb57b3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
interval=10
FILE_NAME = "english.wav"
turbo = Turbo(app)
bcrypt = Bcrypt(app) # for password

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

  
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        password=form.password.data
        pw_hash = bcrypt.generate_password_hash(password)
        user = User(username=form.username.data, email=form.email.data, password=pw_hash)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        # return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)


@app.route("/captions")
def captions():
    TITLE = "English Numbers"
    return render_template('captions.html', songName=TITLE, file=FILE_NAME)  

@app.before_first_request
def before_first_request():
    #resetting time stamp file to 0
    file = open("pos.txt","w") 
    file.write(str(0))
    file.close()

    #starting thread that will time updates
    threading.Thread(target=update_captions).start()

@app.context_processor
def inject_load():
    # getting previous time stamp
    file = open("pos.txt","r")
    pos = int(file.read())
    file.close()

    # writing next time stamp
    file = open("pos.txt","w")
    file.write(str(pos+interval))
    file.close()

    #returning captions
    return {'caption':printWAV(FILE_NAME, pos=pos, clip=interval)}

def update_captions():
    with app.app_context():
        while True:
            # timing thread waiting for the interval
            time.sleep(interval)

            # forcefully updating captionsPane with caption
            turbo.push(turbo.replace(render_template('captionsPane.html'), 'load'))


'''
To View Users: run python3
>>> from app_py_file_name import db
>>> from app_py_file_name import User
>>> User.query.all()
'''
  
@app.route("/second_page")
def second_page():
    return render_template('second_page.html', subtitle='Second Page', text='This is the second page')
  
# put to byass manual environment variable setting
if __name__ == '__main__':               # this should always be at the end
    app.run(host="0.0.0.0")