# THIS CODE IS FROM HELPERS.PY CS50
from flask_mail import Message
from flask import redirect, render_template, request, session
from functools import wraps

# importing my credencias from env
from decouple import config

def messenger(destiny, name, reason):
    # Config a Message object for send to user email
        if reason == "register":
            message = Message("Hello"+name+"and Wellcome to Expenses and Savings", recipients=[destiny])    
            message.body = 'We are really happy, if this message arrive in the spam folder we ask you for mark it like not-spam.'
            
            return message

        if reason == "restart-password":
            message = Message("Restarting your password", recipients=[destiny])
            # Buildng a personal message using api.memegen
            textToImg0 ='<img src="https://api.memegen.link/images/jim/'
            textToImg1 = "don't_worry_"
            textToImg2 ='_this_happens_all_the_time/Just_click_on_the_link_above_for_restart_your_password.png">'
            img = textToImg0 + textToImg1 + name + textToImg2
            message.body = 'here will be soon a lonk to restart your password'
            message.html = img 
    
            return message


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
