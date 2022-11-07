# enviorment variables
from boto.s3.connection import S3Connection
import os

# database
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# "own" functions
from my_tools import reset_password_message, welcome_message, login_required, get_reset_token, verify_reset_token

# flask 
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
    """Manage the password forgive link of "/login" route"""
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


@app.route('/password_reset_verified/<token>', methods=['GET', 'POST'])
def reset_verified(token):
    """Verify the token sended on "/password_reset"""

    # I toke the idea for this from https://medium.com/@stevenrmonaghan/password-reset-with-flask-mail-protocol-ddcdfc190968 
    # and specially from https://www.youtube.com/watch?v=zYWpEJAHvaI
    
    # creating variables for short the lines
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
    """Manage the change password of "/acount" route."""

    if request.method == "POST":

        # creating variables for short the lines
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

        # Redirect to login
        flash("Please check your email box, we'v send a link to restart your password")
        return redirect("/login")

    # Show form
    return render_template("change_password.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """For login"""
    # For secure that user cannot login two different session
    if "user_id" in session:
        return redirect("/logout")
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        email = request.form.get("email").lower()
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

        username = request.form.get("username").title()
        password = request.form.get("password")
        email = request.form.get("email").lower()

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
        flash("Now you are register, you can login. We have send an welcome message to your email")
        return redirect(url_for("login"))

    # displaying register form
    return render_template("register.html")


@app.route("/")
@login_required
def index():
    
    # displaying index page 
    return render_template("index.html")

@app.route("/food_table", methods=["GET", "POST"])
@login_required
def foodTable():
    """DISPLAY TWO WAYS FOR SEARCH EMOJI-FOODS"""

    if request.method == "GET":
        rows = db.execute("SELECT * FROM emojis").fetchall()   
        return render_template("food_table.html", imgs=rows)

@app.route("/search")
@login_required
def search():
    """TAKES THE EMOJI_ID AND USES IT TO RETURN ALL IT'S DATA IN AN ASYNC PROCESS"""

    emoji_input = request.args.get("q")
    
    # Uses (ord()) because I recorded the emojis whit look hexadecimal on the database
    # Then i convert to str for replace the "0" in the "first character" 
    # I learn about this in https://www.otaviomiranda.com.br/2020/normalizacao-unicode-em-python/

    if emoji_input:
        emoji_html = str(hex(ord(emoji_input))).replace("0x", "x")
        emoji_data = db.execute("SELECT * FROM emojis WHERE hexa = :hexa", {"hexa":emoji_html})         
        return render_template("search.html", emoji_data=emoji_data)
    
    # if the input is invalid also return the serach.html empty 
    return render_template("search.html")

@app.route("/like_it")
@login_required
def likeIt():
    """RECORD THE "LIKES" ON DATABASE"""

    # take the emoj_id from the value of the like buttom
    emoji_id = request.args.get("emoji_id")

    # if it is not the emoji_id break return message error 
    if not emoji_id:
        flash("Something is break, Please contact to Web Master.")
        return redirect(url_for("foodTable"))
    
    # check if this preference already exist for this user
    emoji = db.execute("SELECT emoji_id FROM preferences WHERE user_id = :user_id AND emoji_id = :emoji_id", {"user_id":session["user_id"], "emoji_id":emoji_id}).fetchone()
    
    # store the "like"
    if not emoji:
        db.execute("INSERT INTO preferences (user_id, emoji_id) VALUES (:user_id, :emoji_id)", {"user_id":session["user_id"], "emoji_id":emoji_id})
        db.commit()    
    # return a succes message
    flash("Emoji store as favorite in ""My Acount"".")
    return redirect(url_for("foodTable"))


@app.route("/acount", methods=["GET", "POST"])
@login_required
def acount():
    # this method is for delete a particular item from preferences
    if request.method == "POST":
        emoji_id = request.form.get("emoji_id")

        # if it is not the emoji_id break return message error 
        if not emoji_id:
            flash("Something is break, Please contact to Web Master.")
            return redirect(url_for("foodTable"))
        
        # deleting the emoji from the preferences of the user.
        db.execute("DELETE FROM preferences WHERE user_id = :user_id AND emoji_id = :emoji_id", {"user_id":session["user_id"], "emoji_id":emoji_id})
        db.commit()


    # verifying that exist records for this user
    emoji_list = db.execute("SELECT emoji_id FROM preferences WHERE user_id = :user_id ", {"user_id":session["user_id"]}).fetchone()
    
    # if aren't recording returning a simple page
    if not emoji_list:
        return render_template("acount.html")
    
    # if are recordings select and return in a list
    user_favorites = db.execute("SELECT * FROM emojis WHERE id IN (SELECT emoji_id FROM preferences WHERE user_id = :user_id)", {"user_id":session["user_id"]}).fetchall()
    return render_template("acount.html", user_favorites=user_favorites)

@app.route("/favorites")
@login_required
def favorites():
    """Show the 5 most popular emojis"""
    favorite = db.execute("SELECT hexa, COUNT(emoji_id) AS vote FROM emojis INNER JOIN preferences ON emojis.id = preferences.emoji_id GROUP BY emojis.hexa ORDER BY COUNT(emoji_id) DESC LIMIT 5").fetchall()
    return render_template("favorites.html", favorite=favorite)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
