from boto.s3.connection import S3Connection
import os

# database
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# helpers
from my_tools import reset_password_message, welcome_message, login_required, get_reset_token, verify_reset_token

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash

s3 = S3Connection(os.environ['HOSTING'], os.environ['MAIL_DEFAULT_SENDER'], os.environ['MAIL_PASSWORD'], os.environ['MAIL_USERNAME'], os.environ['SECRET_KEY'], os.environ['DATABASE'])

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

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
engine = create_engine(os.environ['DATABASE'])
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
            flash("Must give an email", 'error')
            return render_template("send_reset_password.html")

        # Check if email already exist in database
        user = db.execute("SELECT username, id FROM users WHERE email = :email", {"email":email}).fetchone()
        if not user:
            flash("It's not register", 'error')
            return render_template("send_reset_password.html")
        
        # making a token for restart password, using the user id and my_tools
        token = get_reset_token(user.id)
        
        # making and Mail object, whit a token inside, using my_tools
        message = reset_password_message(email, user.username, token)
        
        # sending email
        mail.send(message)
        
        # show message of success and redirect to login page
        flash("Check on your Mail Box", 'message')
        return render_template("send_reset_password.html") 

    # Show the restart-password form
    return render_template("send_reset_password.html")


# I toke the idea for this from https://medium.com/@stevenrmonaghan/password-reset-with-flask-mail-protocol-ddcdfc190968 
# and specially from https://www.youtube.com/watch?v=zYWpEJAHvaI

@app.route('/password_reset_verified/<token>', methods=['GET', 'POST'])
def reset_verified(token):
    
    user_id = verify_reset_token(token)
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if not user_id:
        flash("id no encontrado", "warning")
        return redirect(url_for('password_reset'))
    
    if request.method == "POST":
        # Ensure password was register
        if not password:
            flash("must register a password", "warning")
            return render_template("change_password.html", token=token)

        # Ensure confirm-password register
        elif not confirmation:
            flash("must confirm your password", "warning")
            return render_template("change_password.html", token=token)

        # Ensure password was submitted
        elif password != confirmation:
            flash("confirm password not macht", "warning")
            return render_template("change_password.html", token=token)
        
        # Storing data in database
        hash = generate_password_hash(password)
        db.execute("UPDATE users SET hash = :hash WHERE  id = :id", {"hash":hash, "id":user_id})
        db.commit()

        flash("Please check your email box, we'v send a link to restart your password", "message")
        return redirect(url_for('login'))

    # Show form
    return render_template("change_password.html", token=token)

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():


    if request.method == "POST":
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        old_password = request.form.get("old_password")
        
        # Ensure old_password was provide        
        if not old_password:
            flash("must provide your active password", "warning")
            return render_template("change_password.html")
        
        # asking for active password
        check = db.execute("SELECT hash FROM users WHERE id = :id", {"id":session["user_id"]}).fetchone()
        if not check_password_hash(check.hash, old_password):

            flash("incorrect password", "warning")
            return render_template("change_password.html")

        # Ensure password was register
        elif not password:
            flash("must register a password", "warning")
            return render_template("change_password.html")

        # Ensure confirm-password register
        elif not confirmation:
            flash("must confirm your password", "warning")
            return render_template("change_password.html")

        # Ensure password was submitted
        elif password != confirmation:
            flash("confirm password not macht", "warning")
            return render_template("change_password.html")
        
        # Storing data in database
        hash = generate_password_hash(password)

        db.execute("UPDATE users SET hash = :hash WHERE  id = :id", {"hash":hash, "id":session["user_id"]})
        db.commit()

        flash("Please check your email box, we'v send a link to restart your password", "message")
        return redirect("/login")

    # Show form
    return render_template("change_password.html")

@app.route("/acount", methods=["GET", "POST"])
def acount():
    return render_template("acount.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        email = request.form.get("email")
        password = request.form.get("password")

        if not email:
            flash("must provide an username", "error")
            return render_template("login.html")

        # Ensure password was submitted
        elif not password:
            flash("must provide password", "error")
            return render_template("login.html")

        # Query database for username
        user = db.execute("SELECT id, username, hash FROM users WHERE email = :email", {"email":email}).fetchone()
        
        # Ensure username exists and password is correct
        if user is None or not check_password_hash(user.hash, password):
            flash("invalid username and/or password", "error")
            return render_template("login.html")

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

        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        # Ensure email was register
        if not email:
            flash("must register an email", 'error')
            return render_template("register.html")

        # Ensure username was register
        elif not username:
            flash("must register an username", 'error')
            return render_template("register.html")

        # Ensure password was register
        elif not password:
            flash("must register a password", 'error')
            return render_template("register.html")

        # Ensure confirm-password register
        elif not request.form.get("confirmation"):
            flash("must confirm your password", 'error')
            return render_template("register.html")

        # Ensure password was submitted
        elif password != request.form.get("confirmation"):            
            flash("confirm password not macht", 'error')
            return render_template("register.html")

        # Ensure email was not exist in dataBase
        repeated_email = db.execute("SELECT email FROM users WHERE email = :email", {"email":email}).fetchone()

        if repeated_email:
            flash("This email already exist", 'error')
            return render_template("register.html")

        # Storing data in database
        password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, email, hash) VALUES (:username,:email,:password)", {"username":username, "email":email, "password":password})
        db.commit()

        # seending welcome email
        message = welcome_message(email, username)
        mail.send(message)

        #redirect to login page
        flash("Now you are register", 'message')
        return render_template("register.html")

    # displaying register form
    return render_template("register.html")


@app.route("/")
@login_required
def index():
    
    # displaying index page 
    return render_template("index.html")

@app.route("/food-table", methods=["GET", "POST"])
def foodTable():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM emojis").fetchall()   
        return render_template("food-table.html", imgs=rows)

@app.route("/search")
def search():
    emoji_input = request.args.get("q")
    # Uso hex(ord()) porque guarde los emojis con apariencia hexadecimal en la base de datos
    # Luego lo convierto en str para poder remplazar el "0" que ocupa el primer caracter 
    # un MILLON DE GRACIAS A https://www.otaviomiranda.com.br/2020/normalizacao-unicode-em-python/
    
    if emoji_input:
        emoji_html = str(hex(ord(emoji_input))).replace("0x", "x")
        print(emoji_html)

        emoji_data = db.execute("SELECT * FROM emojis WHERE hexa = :hexa", {"hexa":emoji_html}) 
        return render_template("search.html", emoji_data=emoji_data)

    return render_template("search.html")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)