import os


from flask_mail import Message
from flask import redirect, render_template, request, session, url_for
from functools import wraps
import jwt


def reset_password_message(destiny, name, token):
    message = Message("Restarting your password", recipients=[destiny])
    # Buildng a personal message using api.memegen
    message.html =f''' <h2>Hello {name}</h2>
    <img src="https://api.memegen.link/images/jim/don't_worry_{name}_this_happens_all_the_time/Just_click_on_the_link_bellow_for_restart_your_password.png">
    <p>Click on the link bellow for restart your password</p>
    <a href="https://emoji-food.herokuapp.com/password_reset_verified/{token}">This is a token to reset your password</a>
    '''
    return message
            

def welcome_message(destiny, name):
    message = Message("Hello {name} and Wellcome to Emoji Food", recipients=[destiny])    
    message.html =f'''
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link crossorigin="anonymous" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" rel="stylesheet">
    <script crossorigin="anonymous" src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"></script>
</head>
<body style="font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;" class="container-fluid text-center">
    <div 
        style="max-width: 50rem;
        text-justify: center;
        margin: 1rem auto auto auto;
        background-color:rgb(28, 153, 224);
        padding: 2rem;
        border-radius: 1rem;">
        <form action="https://emoji-food.herokuapp.com" method="get">
            <h2><span style="font-size: 2rem;">&#129395</span> Hello {name}. Wellcome to Emoji Food <span style="font-size: 2rem;">&#128513</span></h2>
            <h4>Tenemos las explicaciones de todos los emojis de comida, con fotos que estan para chuparse los dedos <span style="font-size: 2rem;">&#128523</span></h4>
            <h6>Puedes visitar nuestro site haciendo click en el boton que dejamos a continuacion</h6>
    
            <button style="margin: 1rem auto 2rem auto;" class="btn btn-warning" type="submit">Go to Emoji Food</button>
            <p><span style="color: yellow; font-weight: bold;">Nota Importante:</span style="font-size: 2rem;"> en caso de que haya recibido este mensaje
                dentro de su caja de espam por favor seleccione la opcion "informar que no es spam".
                esto ayudara en caso de que mas adelante olvide su contraseña.</p>
            <p><span style="font-size: 2rem;">&#127775</span> Esperamos tu visita. <span style="font-size: 2rem;">&#127775</span></p>
        </form>
        <p>En caso que el boton no funcione puede copiar el siguiente link, o directamente hacer click en el <span>
        <a style="color: yellow; font-weight: bold;" href="https://emoji-food.herokuapp.com">https://emoji-food.herokuapp.com</a></span></p>
    </div>
</body>
    '''
    return message
    
                  
# I toke an example from https://pyjwt.readthedocs.io/en/latest/usage.html
# make a token using jwt.
def get_reset_token(user_id):
    return jwt.encode({"id": user_id}, os.environ['SECRET_KEY'], algorithm="HS256")

# load a token
def verify_reset_token(token):
    try:
        user_id = jwt.decode(token, os.environ['SECRET_KEY'], algorithms="HS256")["id"]
    except:
        return None
    return user_id 


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
