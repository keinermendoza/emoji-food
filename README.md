# Emoji-Food

#### Video Demo: <pronto-subire-el-video>

#### Description

**Emoji Food** es una aplicacion web que muestra informacion y fotos de los alimentos representados por comidas, incluyendo aquellos que sin ser comidas estan relacionados con la comida.
Ademas de permitir guardar los "likes" que los usuarios den a determinados emojis, y mostrar los 5 emojis preferidos en la pagina junto con su respectivo conteo de "likes".

Dispone tambien de dos estilos intercambiables siendo un tema nocturno y un tema claro.

Envia un mensaje de Bienvenida al usuario recien registrado y tambien dispone de un servicio de recuperacion de acceso, por medio de la creacion de un token que es enviado al email del usuario.

El diseño de la pagina es responsivo lo que permite que el contenido se adapte al tamaño del dispositivo que el ususrio este utilizando.

* * *

### **Inspiracion**

Esta aplicacion ha sido realizado por mi, Keiner Mendoza, como proyecto final del curso CS50x. Es mi primer poyecto y tambien mi primera experiencia con el mundo de la programacion. No le habia prestado atencion a los emojis de comida hasta que en "the Lecture 10" una señora hizo una exposicion sobre los Emojis, y alli me di cuenta que hay muchos platos (especialmente de comida de oriente) que no era capaz de identificar. visite algunas paginas que tenian informacion sobre lo que podian ser esos platos, pero ninguna contenia explicaciones detalladas, es asi que decidi crear una pagina que intentara lograr esto.

* * *

### **Tecnologias**

+ Python 3
+ Flask
+ HTML
+ CSS
+ JavaScript
+ PostgreSQL

* * *

### **Login**

Desde esta pagina el usuario puede iniciar sesion con su correo y su contraseña, teniendo acceso a todas las rutas de la aplicacion.

Cuando un nuevo usuario accede al sitio de **Emoji Food** lo primero que ve es la pagina de Login, esto se debe a que se requiere haber iniciado sesion para tener acceso a la mayor parte de las rutas de este proyecto.

La funcion que garantiza que el usuario haya iniciado session es **login_required** y esta en:

> my_tools.py
>
> > login_required

Esta funcion es aplicada en las rutas:

+ "/"
+ "/acount"
+ "/change_password
+ "/favorites"
+ "/food_table"
+ "/serch"
+ "like_it"

No se aplica en las siguientes rutas para registrar nuevos usuarios, logiar o recuperar el acceso debido a la perdida de contraseña.

+ "/login"
+ "/register"
+ "/password_reset"
+ "/password_reset_verified"

El primer paso para un usuario nuevo es registrarse.
Desde la pagina **Login** el usuario puede acceser a la pagina register tanto por la "navbar" que esta en la parte superior de la pagina, como por medio del boton **Register** que esta en el cuerpo de la pagina.

* * *

### **Register**

La pagina Register permite registrar los nuevos usuarios.

Esta pagina posee una serie de validaciones logradas atraves de los atributos **required** y **pattern** en **html**. por ejemplo:

> requerid pattern="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,}$"

En la mayoria de los casos solo esta presente el atributo **requerid** para evitar enviar un formulario vacio.
este tipo de validacion se encuentra en los documentos:

+ register.html
+ change_password.html
+ login.html
+ send_reset_password.html

La ruta "/register" realiza por su parte la misma verificacion pero de forma distinta. por ejemplo:

```
email = request.form.get('email').lower()

        # Check if user give an email
        if not email:
            flash("Must give an email", 'error')
            return render_template("send_reset_password.html")
```

Mientras que para verificar que la contraseña cumpla con los requerimientos exigidos previamente por **pattern** se usa una funcion llamada **validation_password** que esta en:

> my_tools.py
>
> > validation_password

Esta funcion devuelvo "None" si no hay coincidencia con los requisitos y "True" en caso de que este conforme a los requisitos. Es empleada de la siguiente forma.

```
elif not validation_password(password):
    flash("the password does not meet the minimum requirements")
    return render_template("change_password.html")
```

Esta forma de verificacion tambien esta presente en las rutas:

+ "/login"
+ "/password_reset"
+ "/password_reset_verified"

* * *

### **Mostrar y Ocultar Contraseña**

En todas las paginas en las que se solicita ingresar la contraseña es posible mostrar y ocultar la misma por medio de hacer "click" en el emoji de un pequeño mono, que esta al margen derecho de la caja de texo de la contraseña. al hacer *"click"* la contraseña se mostrara y el emoji del mono cambiara por un emoji de dos ojos y viceversa.

Este efecto es logrado con *Javascript*.

Tuve dificultades para factorizar la funcion que logra ese efecto, por lo cual aparece varias veces en el documento **action.js** sin embargo un claro ejemplo de su funconamiento se presenta a continuacion:

```
document.getElementById('password-emoji').addEventListener('click', function() { 
            if (this.innerHTML == '🙈') {
                this.innerHTML = '👀';
                document.getElementById('password').type = "text";    
            } 
            else
            {
                this.innerHTML = '🙈';
                document.getElementById('password').type = "password";
            }
        });
```

Este efecto es aplicado en las siguientes documentos:

+ login.html
+ register.html
+ change_password.html

percibiendo el usuario su efecto en las siguientes rutas:

+ "/login"
+ "/register"
+ "/change_password"
+ "/password_reset_verified"

* * *

### **Texto de Verificacion de Contraseña**

Cuando el usuario comienza a escribir la confirmacion de su contraseña se despliega un texto al fondo del formulario con tres posibles textos:

> 1. the password does not meet the minimum requirements yet
>
> 2. Password not match yet
> 3. Password match

Esta funcion es una adaptacion de otra funcion que consegui en <https://flaviocopes.com/how-to-add-event-listener-multiple-elements-javascript/>

A continuacion se presenta tal como esta en el documento **action.js**

```
var match = document.getElementById('password-state-match');
        
        [document.getElementById('password'), document.getElementById("confirmation")].forEach(item => {
            item.addEventListener('input', event => {
                const password = document.getElementById('password').value;
                const confirmation = document.getElementById("confirmation").value;
                const validation = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,}$/;
                const verify = password.match(validation);
            
                if (password == "" || confirmation == "") {
                    match.innerHTML = "";
                }
                
                else if (verify == null) {
                    match.innerHTML = "the password does not meet the minimum requirements yet &#129300";
                }

                else if (password == confirmation) {
                    match.innerHTML = "Password match &#128077";
                }
                else {
                    match.innerHTML = "Password not match yet &#129300";
                }

            })
        });

    }
```

La funcion anterior se ejecuta en las rutas:

+ "/register"
+ "/change_password"
+ "/password_reset_verified"

### **Register and Login**

Cuando el usuario termine de llenar los campos del formulario del formulario, la pagina permitira enviar el mismo haciendo click en el boton **Register and Login**.

Luego la ruta "/Register" realizara las siguientes validaciones:

> + Cada campo haya sido llenado
> + Las contraseñas cumplan con los requisitos de seguridad
> + Las contraseñas coincidan entre si.
> + El correo no exista previamente en la base de Datos

Si se cumplen los creiterios la ruta  guaradara los datos del usuario en la tabla *users* de la base de datos y ridereccionara con metodo *POST* hacia la ruta **"/login"** mediante el siguiente coidigo:

```
    return redirect(url_for("login"), code=307)
```

Consiguiendo con esto que el usuario no tenga que rellenar nuevamente el formulario de **"/login"** para iniciar sesion.
* * *
### **Index**

Para llegar a la ruta index **"/"** es necesario pasar la validacion que realiza la ruta **"/login"** esta ultima verifica que la contraseña coinsida con la creada por el usuario, utilizando el correo del usuario como criterio para realizar la busqueda en la base de datos.

Una vez validado el usuario inicia sesion y es redirigido a la ruta **"/"** cuyo unico proposito es desplegar el documento **index.html**.

**index.html** ofrece una explicacion sobre como navegar por la aplicacion web, asi como que funciones pueden ser encotradas en las principales partes.

* * *
### **"/food_table"**

Sus unicos propositos son desplegar el documento food_table.html y servir de contenedor para desplegar en ella el contenido de la ruta **"/search"**. trabaja solo con el metodo *GET*.

Sin embargo es muy util, atraves de ella el usuario puede consultar todos los emojis relacionados con comidas, tanto por medio de los botones que se despliegan en la pagina como por medio de la caja de texto que esta en la parte superior de la misma.

Mas informacion al respecto en la parte que trata sobre  **Base de Datos** y la ruta **"/like_it"**.

* * *
### **"/acount"**

Inicialemente despliega el documento acount.html y serve de contenedor para desplegar en ella el contenido de la ruta **"/search"**. 

En acount se despliegan los emojis a los que el usuario ha dado "like" en forma de botones, con el mismo formato de los botones presentes en  **"/food_table"**, con la diferencia de que el contenido desplegado por **"/serch"** cambia el boton de *like* por uno de *delete*.

la eliminacion de los emojis se logra por medio de la misma ruta **"/acount"** cuando esta es ejecutada con el metodo *POST*

Mas informacion al respecto en la parte que trata sobre la Base de Datos.
* * *

### **"/favorites"**

Sus unicos propositos son desplegar el documento favorites.html y servir de contenedor para desplegar en ella el contenido de la ruta **"/search"**. trabaja solo con el metodo *GET*.

En favorites se despliega un conteo sobre los 5 emojis con mas likes en la pagina, ordenados de mayor a menor.

* * *

## **Base de Datos**

### **img.csv y reader.py**
Inicialmente cree una base de datos en Sqlite3 tal como se implementan en las ultimas clases de CS50x, sin embargo cuando intente llevar mi base de Datos a Heroku, consegui el siguiente articulo
<a><https://devcenter.heroku.com/articles/sqlite3></a> que explica que es mejor utilizar Postgre en su Lugar.
Asi leyendo y buscando en la web tuve la suerte de encontrar el siguiente <a href="https://www.youtube.com/watch?v=gu980iXwY5c">video</a> que explica como implementar una base de datos PostgreSQL en Heroku.
En la carpeta "extra" de este repositorio se encuentran dos archivos "img.csv" y "reader.py" estos fueron utilizados en el proceso de creacion de la base de datos.
img.csv tiene toda la informacion que se utiliza para la
Tabla "emojis".

### **Columna "hexa"**

la primera columna de este archivo es el codigo hexadecimal en formato de "string" del respectivo emojii y termina ocupando la segunda columna de la tabla emojis en la base de datos.
Esta columna "hexadecimal" es utilizada para desplegar contenido en los documentos **food_table.html**, **favorites.html** y **acount.html**.
esto por medio de bucles escritos en *"Jinja"*

```
{% for img in imgs %}
    <button class="imagen" translate="no" 
        value="&#{{img.hexa}">
        &#{{img.hexa}}
    </button>    
{% endfor %}
```

### **"/search"**

la ruta **"/search"** sirve para buscar la informacion de un emoji convirtiendo la entrada de un emoji a formato string compatible con la columna **hexa** almacenada en la base de datos.

**"/search"** siempre regresa el documento **search.html** este documento es generado dinamicamente por medio de sintaxis *Jinja* por lo que si no se consigue coincidencia la ruta devuelve el documento **search.html** vacio.

la ruta **"/search"** es llamada desde los documentos:

> + food_table.html
> + favorites.html
> + acount.html

### **Fotos y Texto descriptivo**

La segunda columna del documento "img.csv" contiene los nombres de los emojis, estos solo sirven para desplegarlos dentro del archivo **search.html** que a su vez es desplegado por medio de una de dos fuciones asioncronas dentro de los archivos dentro de los tres archivos arriba mencionados. especificamente dentro del container.

````
    <div id="container-to-item-selected"></div>
````

la funciones asincronas que relaizan esta accion se encuentra entre la linea 60 y 85 del documento "action.js" y este a su vez esta en la carpeta "static" del presente repositorio.
es practicamente la misma expliacada en la la lecture 9 del curso CS50x.


````
let searchButton = document.querySelector('#search-button');
        searchButton.addEventListener('click', async function() {
            let response = await fetch('/search?q=' + document.querySelector('#input-emoji').value);
            let shows = await response.text();
            document.getElementById('container-to-item-selected').innerHTML = shows;

            afterSelected()
        });
````
ambas funciones realizan el mismo trabajo, la diferencia esta en que una de ellas se activa por medio de los botones desplegados en los archivos "food_table.html", "favorites.html" y "acount.html".
mientras que la otra lo hace desde un boton de "search" que esta presente exclusivamente en la parte superior del archivo "food_table.html".

la tercera columna del documento "img.csv" contiene las rutas de las imagenes a ser desplegadas dentro del archivo "search.html". especificamente en la linea 12.
````
    <img translate="no" class="img-serched" src="{{data.img}}" alt="{{data.name}}">
````

la cuarta y ultima linea del documento "img.csv" contiene el texto descriptivo. especificamente en la linea 15.
````
    <p>{{data.description}}</p>
````

Por su vez el archivo reader.py tiene el proposito de cargar los datos del cumento "img.csv" en la base de datos.
esto fue realizado antes de implementar esta aplicacion por lo que la presencia de ambos archivos "img.csv" y "reader.py" es meramente ilustrativa.

la base de datos posee 2 tablas adicionales:
 "users" que sirve para almacenar el id, nombre, email y la contraseña de los usuarios.
 "preferences" que sirve para hacer un seguimiento de a cuales emojis un suario a dado "like". posee solo dos columnas, una para el "user_id" del usuario y otra para el "emoji_id" del emoji.

* * *

### **"/like_it"**

Esta ruta guarda en la tabla *preferences* de la base de datos el *id* del usuario y el *id* del emoji al que el usuario acaba de dar *like*.

se accede a la ruta **"/like_it"** por medio de un formulario que esta dentro del documento **search.html** por lo que es posible tener acceso a dicha ruta en:

+ "/food_table"
+ "/faovrites"

la siguiente funcion modifica el atributo de la ruta de **search.html** en el caso de estar en **"/acount"**

Linea 48 de **action.js**

````
    if(window.location.pathname == "/acount") {

                document.getElementById('form-like-and-delete').setAttribute('action', '/acount');
                document.getElementById('form-like-and-delete').setAttribute('method', 'post');
                document.getElementById('button-item-selected-like').innerHTML = "Delete";
            }
````

Esto impide que se tenga acceso a la ruta **"/like_it"** dentro de la ruta **"/acount"**.

* * *

### **"/password_reset"**

se accede a esta ruta por medio de un link que se encuentra justo abajo de la caja de texto de *contraseña* en la pagina de **login**.

Despliega el documento **send_reset_password.html** con el fin de que el usuario pueda obtener un email con un link que le permita reingresar a la aplicacion.

para que funcione que dicho mensaje sea enviado el usuario debe ingresar su email en la caja de texto y hacer click en *Submit Email*.

en caso que el email coincida con alguno registrado en la base de datos se aplicaran las siguientes funciones:
> my_tools.py
> > get_reset_token
> 
> > reset_password_message

* * *

### **get_reset_token**

toma como entrada el *id* del usuario. a su vez el *id* se obtiene usando como criterio de busqueda el *email* proporsionado por el usuario.

codifica el *id* convirtiendolo en un token bastante largo.

* * *

### **reset_password_message**

Toma como entrada:

+ destinatario
+ nombre del usuario
+ token

regresa un Message object, con varias tags en *html* y estilo incorporado, pero lo mas importante que lleva es el *token* creado por  **get_reset_token**.

* * *

### **"/password_reset_verified"**

Se puede llegar a esta ruta desde el link incorporado en el email enviado por **reset_password_message**.

Se encarga de identificar de que usuario se tarata para asi poder cambiar la clave de acceso y que el usuario pueda iniciar sesion con su nueva contraseña.

esto se logra por medio de la funcion **verify_reset_token** la cual decodifica el token *extrayeno* el *id*.

luego de extraer el *id* se despliega el documento **change_password.html** el cual contiene un formulario para resetear la contraseña. 

finalmente, si la contraseña pasa las validaciones (las mismas vistas en **"/register"**) la contraseña es actualizada en la base de datos y el usuario es redireccionado a **"/login"** para que pueda iniciar sesion.

en caso de que el token que acompaña la ruta **"/password_reset_verified"** no sea valido el usuario sera reidirigido a **"/password_reset"**.


I toke the idea from https://medium.com/@stevenrmonaghan/password-reset-with-flask-mail-protocol-ddcdfc190968 

and specially from https://www.youtube.com/watch?v=zYWpEJAHvaI
* * *

### **"/change_password"**

Esta ruta despliega el documento **change_password.html**. En este caso el documento incluira una tercera caja de texto la cual es generada con sitaxis *Jinja* en caso de que se este accediendo al mismo sin que el token este presente, es decir, con sesion iniciada. 

se puede acceder a esta ruta por medio del boton *change password* que se encuentra en la pagina *My acount*.

permite cambiar la contraseña siempre y cuando se proporcione la contraseña actual y se cumplan los criterios de validacion para la nueva contraseña.

* * *

### **Modo Claro-Nocturno**

para crear el cambio de apariencia utilice variables de CSS. No sabia que existian variables en CSS, supe de ellas por un comentario en un video de otro tema.
buscando consegui este ejemplo, que me sirvio de guia <a href=""></a>.

con esto esto declaro en estas "variables" en la raiz, asignando los valores a correspondientes al tema claro.
en la linea 21 de "style.css"

````
:root {
  --back--color: #A5F1E9;
  --let--color: rgb(0, 0, 0);
  --bord--color: #7FBCD2;
  --pad--color: #A5FF4B;
  --key-word--color: blue;
  --let--size: 1.4rem;
}
````

luego aplico esas variables a lo largo del documento style.css. por ejemplo, en la linea 39.

````
body {
  background-color: var(--back--color);
  color: var(--let--color);
}
````

a continuacion defino propiamente los valores de los temas claro y nocturno. los cuales llame "sun" and "moon".
````
/*Un atributo que creare en la root del html (creo) con en js*/
[tema="sun"]{
  --back--color: #A5F1E9;
  --let--color: rgb(0, 0, 0);
  --bord--color: #7FBCD2;
  --pad--color: #A5FF4B;
  --key-word--color: blue;
}

/*Un atributo que creare en la root del html (creo) con en js*/
[tema="moon"] {
  --back--color: #4C0033;
  --let--color: white;
  --bord--color: #AF0171;
  --pad--color: #E40DC8;
  --key-word--color: #A5F1E9;
}
````

Para poder cambiar de temas intente sin exito hacer una funcion en "app.py" para guardar el tema que el usuario eligio.
despues de buscar bastante tuve la suerte de encontrar un ejemplo esclarecedor en  <a href=""></a>.

````
document.documentElement.setAttribute('tema', sessionStorage.mode);

window.onload = function() {
    // Si el tema activo es 'moon' marcar chexkbox
    if (document.documentElement.getAttribute('tema') == 'moon') {
        document.querySelector('#mode input[type="checkbox"]').checked = true;
    }

    // Selecciono Box de Mode y agrego function
    document.querySelector('#mode input[type="checkbox"]').addEventListener('input', function(e){
        // Si activan moon-mode establecer atributo en root, activara css
        if(e.target.checked) {
            document.documentElement.setAttribute('tema', 'moon');
            
            // guarado tema de forma local en variable recien creada "mode"
            sessionStorage.mode = document.documentElement.getAttribute('tema');
        } 
        else {
            document.documentElement.setAttribute('tema', 'sun');
            sessionStorage.mode = document.documentElement.getAttribute('tema');   
        }
    });
````

## About the programmer

Soy Keiner Mendoza.
Este es mi primer proyecto. No he tenido colaboradores.
Lo considero un proyecto terminado, actualmente esta disponible en Heroku, pero debido al cierre de las cuentas gratuitas espero pasarlo pronto a otro hosting.