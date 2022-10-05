# importing my credencias from env
from decouple import config
# database
from cs50 import SQL
# helpers
from my_tools import messenger, apology, login_required, usd

from flask import Flask, flash, redirect, render_template, request, session, g
from flask_session import Session
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# For send emails
app.config["MAIL_DEFAULT_SENDER"] = config("MAIL_DEFAULT_SENDER")
app.config["MAIL_PASSWORD"] = config("MAIL_PASSWORD")
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = config("MAIL_USERNAME")
mail = Mail(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///test.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/rest-pass", methods=["GET", "POST"])
def restPass():
    
    if request.method == "POST":
        email = request.form.get('email')
        # Check if user give an email
        if not email:
            noemail = "Must give an email"
            return render_template("restart-password.html", noemail=noemail)

        # Check if email already exist in database
        username_hash = db.execute("SELECT username, hash FROM users WHERE email = ?", email)
        if not username_hash:
            noregister = "It's not register"
            return render_template("restart-password.html", noregister=noregister, emailError=email)
        
        message = messenger(email, username_hash[0]["username"], "restart-password")
        mail.send(message)
        succes = "Check on your Mail Box"
        return render_template("restart-password.html", succes=succes) 

    # Show the restart-password form
    return render_template("restart-password.html")


"""THIS IS AN REMAKE OF MY FINANCE PROJECT"""
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure username was register
        if not request.form.get("username"):
            noname = "must register an username"
            return render_template("register.html", noname=noname)

        # Ensure email was register
        elif not request.form.get("email"):
            noemail = "must register an email"
            return render_template("register.html", noemail=noemail)

        # Ensure password was register
        elif not request.form.get("password"):
            nopass = "must register a password"
            return render_template("register.html", nopass=nopass)

        # Ensure confirm-password register
        elif not request.form.get("confirmation"):
            noconfirm = "must confirm your password"
            return render_template("register.html", noconfirm=noconfirm)

        # Ensure password was submitted
        elif request.form.get("password") != request.form.get("confirmation"):
            nomatch = "confirm password not macht"
            return render_template("register.html", nomatch=nomatch)

        # Ensure username was not exist in dataBase
        username = request.form.get("username")
        repeat_name = db.execute("SELECT username FROM users WHERE username = ?", username)

        if repeat_name:
            return render_template("register.html", username=username, repeat_name=repeat_name)

        # Ensure email was not exist in dataBase
        email = request.form.get("email")
        repeat_email = db.execute("SELECT email FROM users WHERE username = ?", email)

        if repeat_email:
            return render_template("register.html", email=email, repeat_email=repeat_email)

        # Storing data in database
        password = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, email, hash) VALUES (?,?,?)", username, email, password)

        #redirect to login page
        return redirect("/login")

    # displaying register form
    return render_template("register.html")


@app.route("/")
@login_required
def index():
    
    # displaying index page 
    return render_template("index.html")

