from flask import Flask, render_template, redirect, request, session
import urllib3
import json
import os
import sqlite3
import checkers

app = Flask(__name__)
app.secret_key = os.urandom(32)

# get APOD
http = urllib3.PoolManager()
r = http.request(
    'GET', 'https://api.nasa.gov/planetary/apod?api_key=PxL3Eff2wvlbpZ9B6gF6Z1ORyovxbYCMdarvELIz')
imgurl = json.loads(r.data.decode('utf-8')).get("hdurl")
i = open("static/images/APOD.jpg", "wb")
i.write(http.request('GET', imgurl).data)

MAIN_DB = "users.db"

# database
db = sqlite3.connect(MAIN_DB)
c = db.cursor()

# table creation
c.execute("""
CREATE TABLE IF NOT EXISTS USERS (
    ROWID       INTEGER PRIMARY KEY,
    USERNAME    TEXT    NOT NULL,
    HASH        TEXT    NOT NULL,
    PFP         TEXT   
);""")

db.commit()
db.close()


def isAlphaNum(string):
    """
    returns whether a string is alphanumeric
    """
    for char in string:
        o = ord(char)
        if not ((0x41 <= o <= 0x5A) or (0x61 <= o <= 0x7A) or (0x30 <= o <= 0x39)):
            return False
    return True


# Home page
@app.route("/")
def index():
    return render_template("index.html", user=session.get('username'))


# Play
@app.route("/play")
def play():
    return render_template("play.html")


# Signup function
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    """
        If method = GET, render page to new username & password
        If method = POST, attempts to sign up user, if successful renders login data
    """
    # Obtaining query from html form
    if request.method == "POST":
        print(request.form['username'] + " - " + request.form['password'])
        # Checking if required values in query exist using key values
        if 'username' in request.form and 'password' in request.form:
            db = sqlite3.connect(MAIN_DB)
            c = db.cursor()
            # Obtaining data from database
            c.execute("""SELECT USERNAME FROM USERS WHERE USERNAME = ?;""",
                      (request.form['username'],))
            exists = c.fetchone()
            # Checking to see if the username that the person signing up gave has not been made
            if (exists == None):
                username = (request.form['username']).encode('utf-8')
                # Check to see if user follows formatting
                if isAlphaNum(username.decode('utf-8')) == None:
                    db.close()
                    return render_template("login.html", user=session.get('username'), action="/signup", name="Sign Up", error="Username can only contain alphanumeric characters.")
                # Check to see if username is of proper length
                if len(username) < 5 or len(username) > 15:
                    db.close()
                    return render_template("login.html", user=session.get('username'), action="/signup", name="Sign Up", error="Usernames must be between 5 and 15 characters long")
                password = request.form['password']
                # Checking for illegal characters in password
                if ' ' in list(password) or '\\' in list(password):
                    db.close()
                    return render_template("login.html", action="/signup", name="Sign Up", error="Passwords cannot contain spaces or backslashes.")
                password = str(password)
                # Checking to see if password follows proper length
                if len(password) > 7 and len(password) <= 50:
                    r = http.request(
                        'GET', "http://dog.ceo/api/breeds/image/random")
                    pfpurl = ""
                    if r.status == 200:
                        pfpurl = json.loads(r.data).get('message')
                    c.execute("""INSERT INTO USERS (USERNAME,HASH,PFP) VALUES (?,?,?)""",
                              (request.form['username'], password, pfpurl,))
                    db.commit()
                    c.execute(
                        """SELECT USERNAME FROM USERS WHERE USERNAME = ?;""", (request.form['username'],))
                    exists = c.fetchone()
                    db.close()
                    if (exists != None):
                        return render_template("login.html", action="/login", name="Login", success="Signed up successfully!")
                    else:
                        return render_template("login.html", action="/signup", name="Sign Up", error="Some error occurred. Please try signing up again.")
                else:
                    db.close()
                    return render_template("login.html", action="/signup", name="Sign Up", error="Password must be between 8 and 50 characters long")
            else:
                db.close()
                return render_template("login.html", action="/signup", name="Sign Up", error="Username already exists")
        else:
            return render_template("login.html", action="/signup", name="Sign Up", error="Some error occurred. Please try signing up again.")
    else:
        return render_template("login.html", action="/signup", name="Sign Up")


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
        If method = GET, render page to enter login info
        If method = POST, attempts to login user with posted data
    """
    if request.method == "POST":
        if 'username' in session:
            return render_template("index.html", user=session.get('username'), message="Already logged in!")
        if 'username' in request.form and 'password' in request.form:
            db = sqlite3.connect(MAIN_DB)
            c = db.cursor()
            c.execute("""SELECT HASH FROM USERS WHERE USERNAME = ?;""",
                      (request.form['username'],))
            hashed = c.fetchone()  # [0]
            db.close()
            if (hashed == None):
                return render_template("login.html", name="Login", action="/login", error="User does not exist.")
            else:
                if hashed[0] == request.form['password']:
                    session['username'] = request.form['username']
                    return redirect('/')
                else:
                    return render_template("login.html", name="Login", action="/login", error="Password is incorrect")
        else:
            return render_template("login.html", name="Login", action="/login", error="An error occurred. Please try logging in again.")
    else:
        return render_template("login.html", action="/login", name="Login")

# Logout function
@app.route("/logout")
def logout():
    """ 
        Logouts user 
    """
    session.pop('username', default=None)
    return redirect("/")

# Profile function
@app.route("/profile")
def profile():
    if 'username' in session:
        return render_template("profile.html", user = session['username'])
    else:
        return redirect("/login")

if __name__ == "__main__":
    app.debug = True
    app.run()
