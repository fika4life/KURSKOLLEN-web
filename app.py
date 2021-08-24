from flask import Flask, request, render_template 
from flask_session import Session
from tempfile import mkdtemp
import requests

import sqlite3

from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect


from helpers import login_required, apology


app = Flask(__name__)

# turn on debug mode
app.debug = True

#auto reload templates
app.config['TEMPLATES_AND_RELOAD'] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure SQLite database
conn = sqlite3.connect('kurskollen.db')
c = conn.cursor()



conn.commit()

conn.close()

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        #access form inputs
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # check for blanks
        if not email or not password or not password2:
            return apology("must provide email and password", 400)
        
      # chekc dataabse to see if username already exists
        emails = db.execute("SELECT email FROM users WHERE email = ?", email)
        if emails:
            return apology("username already exists", 400)

        # if username doesn't exist AND passwords match, create new one.
        elif password != password2:
            return apology("passwords did not match", 400)

        # hash password before adding to database
        else:
            pw_hash = generate_password_hash(password)

            success = db.execute("INSERT INTO users (email, hash) VALUES(?,?);", email, pw_hash)

            # if successful creating send to login page
            if success:
                print(success)
                return redirect("/login")
            else:
                return apology("something went wrong", 403)

    #if get request
    else:
        return render_template("register.html")
   
@app.route('/login', methods=["GET", "POST"])
def login():



    if request.method == "GET":
        return render_template("login.html")

@app.route('/write-review', methods=["GET", "POST"])
# @login_required
def writeReview():
    if request.method == 'GET':
        return render_template('writeReview.html')


@app.route('/search-results', methods=["GET", "POST"])
def searchResults():
    if request.method == 'GET':
        data = requests.get('https://my-json-server.typicode.com/fika4life/KURSKOLLEN-web/courses')
        return render_template('searchResults.html', data = data.json())
    


@app.route('/course', methods = ['GET'])
def getCourse():
    if request.method == 'GET':
        data = requests.get('https://my-json-server.typicode.com/fika4life/KURSKOLLEN-web/courses')
        return render_template('course.html', data = data.json())


@app.route('/create-course', methods = ['GET'])
def createCourse():
    if request.method == 'GET':
          return render_template('createCourse.html')


if __name__ == '__main__':
    app.run(debug = True)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)