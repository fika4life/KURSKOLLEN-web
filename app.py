from flask import Flask, request, render_template


app = Flask(__name__)

app.debug = True

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
   
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

@app.route('/write-review', methods=["GET", "POST"])
def writeReview():
    if request.method == 'GET':
        return render_template('writeReview.html')


@app.route('/search-results', methods=["GET", "POST"])
def searchResults():
    if request.method =='GET':
        return render_template('searchResults.html')

if __name__ == '__main__':
    app.run(debug = True)


