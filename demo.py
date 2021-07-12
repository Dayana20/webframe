from flask import Flask, render_template, url_for
app = Flask(__name__)                    # this gets the name of the file so Flask knows it's name

# @app.route("/")                          # this tells you the URL the method below is related to
# def hello_world():
#     return "<p>Hello, World!</p>"        # this prints HTML to the webpage
@app.route("/")                          # this tells you the URL the method below is related to
def home():
    return render_template('home.html', subtitle='Home Page')


@app.route("/about")                          # this tells you the URL the method below is related to
def about():
    return render_template('about.html', subtitle='About Page')
  
  
@app.route("/second_page")
def second_page():
    return render_template('second_page.html', subtitle='Second Page', text='This is the second page')
  
# put to byass manual environment variable setting
if __name__ == '__main__':               # this should always be at the end
    app.run(host="0.0.0.0")