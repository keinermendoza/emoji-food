from boto.s3.connection import S3Connection
import os

# database
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# helpers
from my_tools import messenger, apology, login_required, usd, get_reset_token, verify_reset_token

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash

s3 = S3Connection(os.environ['MAIL_DEFAULT_SENDER'], os.environ['MAIL_PASSWORD'], os.environ['MAIL_USERNAME'], os.environ['SECRET_KEY'])

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure send emails
app.config["MAIL_DEFAULT_SENDER"] = os.environ['MAIL_DEFAULT_SENDER']
app.config["MAIL_PASSWORD"] = os.environ['MAIL_PASSWORD']
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ['MAIL_USERNAME']
mail = Mail(app)

# Configure Postrge Heroku as database
engine = create_engine(os.environ['DATABASE_URL'])
db = scoped_session(sessionmaker(bind=engine))

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/password_reset", methods=["GET", "POST"])
def password_reset():

    if request.method == "POST":
        email = request.form.get('email')

        # Check if user give an email
        if not email:
            noemail = "Must give an email"
            return render_template("send_reset_password.html", noemail=noemail)

        # Check if email already exist in database
        user = db.execute("SELECT username, id FROM users WHERE email = :email", {"email":email}).fetchone()
        if not user:
            noregister = "It's not register"
            return render_template("send_reset_password.html", noregister=noregister, emailError=email)
        
        # making a token for restart password, using my_tools
        token = get_reset_token(user.id)
        
        # making and Mail object, whit a token inside, using my_tools
        message = messenger(user.email, "restart-password", token)
        
        # sending email
        mail.send(message)
        
        # show message of success and redirect to login page
        flash("Check on your Mail Box", "warning")
        return render_template("send_reset_password.html") 

    # Show the restart-password form
    return render_template("send_reset_password.html")


# I toke the idea for this from https://medium.com/@stevenrmonaghan/password-reset-with-flask-mail-protocol-ddcdfc190968 
# and specially from https://www.youtube.com/watch?v=zYWpEJAHvaI

@app.route('/password_reset_verified/<token>', methods=['GET', 'POST'])
def reset_verified(token):
    
    user_id = verify_reset_token(token)
    if not user_id:
        flash("id no encontrado", "warning")
        return redirect(url_for('password_reset'))
    
    if request.method == "POST":
        # Ensure password was register
        if not request.form.get("password"):
            nopass = "must register a password"
            return render_template("change_password.html", nopass=nopass, token=token)

        # Ensure confirm-password register
        elif not request.form.get("confirmation"):
            noconfirm = "must confirm your password"
            return render_template("change_password.html", noconfirm=noconfirm, token=token)

        # Ensure password was submitted
        elif request.form.get("password") != request.form.get("confirmation"):
            nomatch = "confirm password not macht"
            return render_template("change_password.html", nomatch=nomatch, token=token)
        
        # Storing data in database
        password = generate_password_hash(request.form.get("password"))
        db.execute("UPDATE users SET hash = :hash WHERE  id = :id", {"hash":password, "id":user_id})
        db.commit()

        flash("Please check your email box, we'v send a link to restart your password", "message")
        return redirect(url_for('login'))

    # Show form
    return render_template("change_password.html", token=token)

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        old_password = request.form.get("old_password")
        
        # Ensure old_password was provide        
        if not old_password:
            nooldpass = "must provide your active password"
            return render_template("change_password.html", nooldpass=nooldpass)
        
        # asking for active password
        check = db.execute("SELECT hash FROM users WHERE id = :id", {"id":session["user_id"]}).fetchone()
        if not check_password_hash(check.hash, old_password):
            nocheck = "incorrect password"
            return render_template("change_password.html", nocheck=nocheck)

        # Ensure password was register
        elif not request.form.get("password"):
            nopass = "must register a password"
            return render_template("change_password.html", nopass=nopass)

        # Ensure confirm-password register
        elif not request.form.get("confirmation"):
            noconfirm = "must confirm your password"
            return render_template("change_password.html", noconfirm=noconfirm)

        # Ensure password was submitted
        elif request.form.get("password") != request.form.get("confirmation"):
            nomatch = "confirm password not macht"
            return render_template("change_password.html", nomatch=nomatch)
        
        # Storing data in database
        password = generate_password_hash(request.form.get("password"))

        db.execute("UPDATE users SET hash = :hash WHERE  id = :id", {"hash":password, "id":session["user_id"]})
        db.commit()

        flash("Please check your email box, we'v send a link to restart your password", "message")
        return redirect("/login")

    return render_template("change_password.html")

@app.route("/acount", methods=["GET", "POST"])
def acount():
    return render_template("acount.html")


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
        user = db.execute("SELECT * FROM users WHERE username = :username", {"username":request.form.get("username")}).fetchall()

        # Ensure username exists and password is correct
        if user is None or not check_password_hash(user.hash, request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = user.id

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
        repeat_name = db.execute("SELECT username FROM users WHERE username = :username", {"username":username}).fetchone()

        if repeat_name:
            return render_template("register.html", username=username, repeat_name=repeat_name)

        # Ensure email was not exist in dataBase
        email = request.form.get("email")
        repeat_email = db.execute("SELECT email FROM users WHERE email = :email", {"email":email}).fetchone()

        if repeat_email:
            return render_template("register.html", email=email, repeat_email=repeat_email)

        # Storing data in database
        password = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, email, hash) VALUES (:username,:email,:hash)", {"username":username, "email":email, "password":password})
        db.commit()
        #redirect to login page
        return redirect("/login")

    # displaying register form
    return render_template("register.html")


@app.route("/")
@login_required
def index():
    
    # displaying index page 
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)