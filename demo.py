import sys
try:
    from flask import Flask, render_template, url_for, flash, redirect, request
    from forms import RegistrationForm
    from flask_sqlalchemy import SQLAlchemy
    from converter import printWAV  # get speech recognition function
    import time
    import random
    import threading
    from turbo_flask import Turbo  # pip3 install turbo-flask
    from flask_bcrypt import Bcrypt  # for password (pip install flask-bcrypt)
    from flask_behind_proxy import FlaskBehindProxy
    # pip install flask-behind-proxy
except ImportError as e:
    print("Error: " + str(e))

try:
    app = Flask(__name__)
    # this gets the name of the file so Flask knows it's name
    proxied = FlaskBehindProxy(app)  # helps with reload
    app.config['SECRET_KEY'] = '67414c2f94271f30852f5623dbeb57b3'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db = SQLAlchemy(app)
    interval = 10
    FILE_NAME = "just_keep_swimming.wav"
    turbo = Turbo(app)
    bcrypt = Bcrypt(app)  # for password
except Exception as e:
    print("Fix your errors: " + str(e))
    sys.exit()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"


# this tells you the URL the method below is related to
@app.route("/")
def home():
    return render_template('home.html', subtitle='Home Page')


# this tells you the URL the method below is related to
@app.route("/about")
def about():
    return render_template('about.html', subtitle='About Page')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # checks if entries are valid
        password = form.password.data
        pw_hash = bcrypt.generate_password_hash(password)
        user = User(username=form.username.data, email=form.email.data,
                    password=pw_hash)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))  # if so - send to home page
    
    return render_template('register.html', title='Register', form=form)


@app.route("/captions")
def captions():
    try:
        TITLE = "English Numbers"
        return render_template('captions.html', songName=TITLE, file=FILE_NAME)
    except FileNotFoundError:
        print("cannot open "+FILE_NAME)


@app.before_first_request
def before_first_request():
    # resetting time stamp file to 0
    file = open("pos.txt", "w") 
    file.write(str(0))
    file.close()
    # starting thread that will time updates
    # threading.Thread(target=update_captions).start()
    threading.Thread(target=update_captions, daemon=True).start()


@app.context_processor
def inject_load():
    try:
        # getting previous time stamp
        file = open("pos.txt", "r")
        pos = int(file.read())
        file.close()

        # writing next time stamp
        file = open("pos.txt", "w")
        file.write(str(pos + interval))
        file.close()

        # returning captions
        return {'caption': printWAV(FILE_NAME, pos=pos, clip=interval)}
    except FileNotFoundError:
        print("cannot open " + FILE_NAME)


def update_captions():
    with app.app_context():
        while True:
            # timing thread waiting for the interval
            time.sleep(interval)

            # forcefully updating captionsPane with caption
            turbo.push(turbo.replace(render_template('captionsPane.html'),
                                     'load'))


'''
To View Users: run python3
>>> from app_py_file_name import db
>>> from app_py_file_name import User
>>> User.query.all()
'''

# Route for handling the login page logic
@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')
   
    
@app.route('/sign_in', methods=['POST'])
def sign_in_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it
    # compare it to the hashed password in the database
    if (user is None):
        flash('Please check your login details and try again')
        return redirect(url_for('sign_in')) 
        # if the user doesn't exist or password is wrong, reload the page
    else:
        authenticated_user = bcrypt.check_password_hash(user.password, password)
        if authenticated_user:
            # if the above check passes 
            # then we know the user has the right credentials
            flash(f'Account Login Success for {username}')
            return redirect(url_for('home'))
        else:
            flash('Please check your login details and try again')
            return redirect(url_for('sign_in'))


#   this should always be at the end
if __name__ == '__main__':
    app.run(host="0.0.0.0")
