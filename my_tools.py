import os
# importing my credencias from env
from boto.s3.connection import S3Connection

from flask_mail import Message
from flask import redirect, render_template, request, session, url_for
from functools import wraps
import jwt

def messenger(destiny, name, reason, token=0):
    
    # Config a Message object for send to user email
        if reason == "register":
            message = Message("Hello "+name+" and Wellcome to Expenses and Savings", recipients=[destiny])    
            message.body = 'We are really happy, if this message arrive in the spam folder we ask you for mark it like not-spam.'
            
            return message

        if reason == "restart-password":
            message = Message("Restarting your password", recipients=[destiny])
            
            # Buildng a personal message using api.memegen
            message.html =f''' <h2>Hello {name}</h2>
            <img src="https://api.memegen.link/images/jim/don't_worry_{name}_this_happens_all_the_time/Just_click_on_the_link_bellow_for_restart_your_password.png">
            <p>Click on the link bellow for restart your password</p>
            <a href="{url_for('reset_verified', token=token,_external=True)}">This link contains a token to reset your password</a>
            '''
            return message
          

# I toke an example from https://pyjwt.readthedocs.io/en/latest/usage.html
# make a token using jwt.
def get_reset_token(user_id):
    return jwt.encode({"id": user_id}, S3Connection(os.environ['SECRET_KEY']), algorithm="HS256")

# load a token
def verify_reset_token(token):
    try:
        user_id = jwt.decode(token, S3Connection(os.environ['SECRET_KEY']), algorithms="HS256")["id"]
    except:
        return None
    return user_id 

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
