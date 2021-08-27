from flask import Flask, request, render_template, session 
from flask.helpers import url_for 
from flask_session import Session
from tempfile import mkdtemp
import requests
from cs50 import SQL
import sqlite3
#from requests.sessions import session

from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect


from helpers import login_required, apology


app = Flask(__name__)

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
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///kurskollen.db")

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
            return redirect(url_for('register', msg = 'Account already exists.'))

        # if username doesn't exist AND passwords match, create new one.
        elif password != password2:
            return apology("passwords did not match", 400)

        # hash password before adding to database
        else:
            pw_hash = generate_password_hash(password)

            success = db.execute("INSERT INTO users (email, hash) VALUES(?,?);", email, pw_hash)

            # if successful creating send to login page
            if success:
                print('succses register')
                return redirect(url_for('login'))
            else:
                return apology("something went wrong", 403)

    # if request.method is GET, show user registration form.
    else:
        if request.args.get('msg'):
            return render_template("register.html", msg=request.args.get('msg'))
        return render_template('register.html')
   
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("email"):
            return render_template("login.html", msg='Email är obligatorisk')

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", msg='Fel mejladdress eller lösenord')

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("login.html")


@app.route('/write-review', methods=["GET", "POST"])
@login_required
def writeReview():
    if request.method == 'GET':
         return render_template('writeReview.html')


@app.route('/search-results', methods=["GET", "POST"])
def searchResults():
    if request.method == 'GET':
        # session['url'] = url_for('searchResults')
        data = requests.get('https://my-json-server.typicode.com/fika4life/KURSKOLLEN-web/courses')
        return render_template('searchResults.html', data = data.json())
    


@app.route('/course', methods = ['GET'])
def getCourse():
    if request.method == 'GET':
        data = requests.get('https://my-json-server.typicode.com/fika4life/KURSKOLLEN-web/courses')
        return render_template('course.html', data = data.json())


@app.route('/create-course', methods = ['GET', 'POST'])
def createCourse():
    if request.method == 'POST':
        courseName = request.form.get('courseName')
        university = request.form.get('university')
        credits = request.form.get('credits')  

        
        
        success = db.execute("INSERT INTO courses (name, university, credits, created_by) VALUES (?,?,?,?);", courseName, university, credits, session['user_id'])

       

        if success:
            data = requests.get('https://my-json-server.typicode.com/fika4life/KURSKOLLEN-web/courses')
            return render_template('course.html', data = data.json())
        else:
          return render_template('createCourse.html', msg='Error')
            
        
    else:
          return render_template('createCourse.html')
    


if __name__ == '__main__':
    app.run(debug=True)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)