import os


from flask_mail import Message
from flask import redirect, render_template, request, session, url_for
from functools import wraps
import jwt
                  
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


def reset_password_message(destiny, name, token):
    message = Message("Restarting your password", recipients=[destiny])
    # Buildng a personal message using api.memegen
    message.html =f''' <body style="font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; ">
    <div style="max-width: 40rem;
                font-size: 1rem;
                margin: 1rem auto auto auto;
                background-color:rgb(28, 153, 224);
                padding: 2rem;
                text-align: center;
                border-radius: 1rem;
                margin: auto;">
        
        <h1>Hello {name}</h1>
        <h2>🕵 Este es un email para resetear tu contraseña.</h2>
            
        <img style="width: 80%;
                    margin: 0 auto;"
                src="https://api.memegen.link/images/jim/don't_worry_{name}_this_happens_all_the_time/Just_click_on_the_button_bellow_for_reset_your_password.png">
            
        <form action="https://emoji-food.herokuapp.com/password_reset_verified/{token}" method="get">
            
            <button 
                style="margin: 1rem auto 2rem auto;
                        padding: 1rem;
                        background-color: rgb(160, 19, 160);
                        border-radius: 0.5rem;
                        font-weight: bold;
                        color:white;" 

                    type="submit">🔑 Reset Your Password 🔐</button>

            <p><a 
                style="color: rgb(160, 19, 160);
                        font-weight: bold;
                        margin-top: 1rem;"

                    href="https://emoji-food.herokuapp.com/password_reset_verified/{token}">
                    Tambien puedes resetear tu contraseña haciendo click aqui 🗝</a></p>
        </form>
    </div>
</body>
'''
    return message
            

def welcome_message(destiny, name):
    message = Message(f"Hello {name} and Wellcome to Emoji Food", recipients=[destiny])    
    message.html =f'''
<body style="font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;">
    <div 
        style="max-width: 40rem;
            font-size: 1rem;
            margin: 1rem auto auto auto;
            background-color:rgb(28, 153, 224);
            padding: 2rem;
            text-align: center;
            border-radius: 1rem;
            margin: auto;">

        <h3 style="text-justify: center;"><span style="font-size: 2rem;">🥳</span> Hello {name}. Wellcome to Emoji Food <span style="font-size: 2rem;">😁</span></h3>
        <h5>Tenemos las explicaciones de todos los emojis de comida, con fotos que estan para chuparse los dedos <span>😋</span></h5>
        <h4>Puedes visitar nuestro site haciendo click en el boton que dejamos a continuacion</h4>
                
        <form action="https://emoji-food.herokuapp.com" method="get">
            
            <button style="margin: 1rem auto 2rem auto;
                        padding: 1rem;
                        background-color: yellow;
                        border-radius: 0.5rem;
                        font-weight: bold;" 
                    type="submit">Go to Emoji Food</button>

            <p><span style="color: yellow;
                     font-weight: bold;">Nota Importante:</span style="font-size: 2rem;"> en caso de que haya recibido este mensaje
                
                dentro de su caja de espam por favor seleccione la opcion "informar que no es spam".
                esto ayudara en caso de que mas adelante olvide su contraseña.</p>
            <p>🌟 Esperamos tu visita. 🌟</p>
        </form>
        <p>En caso que el boton no funcione puede copiar el siguiente link, o directamente hacer click en el <span>
            <a style="color: yellow;
                font-weight: bold;" href="https://emoji-food.herokuapp.com">https://emoji-food.herokuapp.com</a></span></p>
    </div>
</body>
    '''
    return message