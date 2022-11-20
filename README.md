# Emoji-Food

#### Video Demo: <https://www.youtube.com/watch?v=5QIUln4EdlY[](https://www.youtube.com/watch?v=5QIUln4EdlY)>

#### Description:

**Emoji Food** is a web application that displays information and photos of food represented by food, including those that are not food-related.
In addition to allowing you to save the "likes" that users give to certain emojis, and display the 5 favorite emojis on the page along with their respective "likes" count.

It also has two interchangeable styles being a night theme and a light theme.

It sends a Welcome message to the newly registered user and also has an access recovery service, through the creation of a token that is sent to the user's email.

The design of the page is responsive, which allows the content to adapt to the size of the device that the user is using.

* * *

### **Inspiration**

This application has been made by me, Keiner Mendoza, as a final project of the CS50x course. It is my first project and also my first experience with the world of programming. I had not paid attention to food emojis until in "the Lecture 10" a lady made a presentation about Emojis, and there I realized that there are many dishes (especially oriental food) that I was not able to identify. I visited some pages that had information about what those dishes could be, but none of them contained detailed explanations, so I decided to create a page that will try to achieve this.

* * *

### **Technologies**

+ Python 3
+ Flask
+ HTML
+ CSS
+ javascript
+ PostgreSQL

* * *

### **Login**

From this page the user can log in with his email and password, having access to all the routes of the application.

When a new user accesses the **Emoji Food** site, the first thing they see is the Login page, this is because a session is required to access most of the routes of this project.

The function that ensures the user is logged in is **login_required** and is in:

> my_tools.py
>
> > login_required

This function is applied on routes:

+ "/"
+ "/account"
+ "/change_password
+ "/favourites"
+ "/food_table"
+ "/search"
+ "like_it"

It does not apply to the following routes for registering new users, logging in, or regaining access due to lost password.

+ "/ login"
+ "/register"
+ "/password_reset"
+ "/password_reset_verified"

The first step for a new user is to register.
From the **Login** page the user can access the register page both through the "navbar" that is at the top of the page, and through the **Register** button that is in the body of the page .

* * *

### **Register**

The Register page allows you to register new users.

This page has a series of validations achieved through the **required** and **pattern** attributes in **html**. for instance:

> required pattern="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{6,}$"

In most cases only the **required** attribute is present to avoid submitting an empty form.
This type of validation is found in the documents:

+ register.html
+ change_password.html
+ login.html
+ send_reset_password.html

The route "/register" performs the same verification but in a different way. for instance:

```
email = request.form.get('email').lower()

        # Check if user give an email
        if not email:
            flash("Must give an email", 'error')
            return render_template("send_reset_password.html")
```

While to verify that the password meets the requirements previously demanded by **pattern**, a function called **validation_password** is used, which is in:

> my_tools.py
>
> > validation_password

This function returns "None" if the requirements are not matched and "True" if the requirements are met. It is used in the following way.

```
elif not validation_password(password):
    flash("the password does not meet the minimum requirements")
    return render_template("change_password.html")
```

This form of verification is also present in routes:

+ "/ login"
+ "/password_reset"
+ "/password_reset_verified"

* * *

### **Show and Hide Password**

In all the pages where you are asked to enter the password, it is possible to show and hide it by clicking on the emoji of a little monkey, which is on the right side of the password text box. by *"clicking"* the password will be displayed and the monkey emoji will change to a two-eyed emoji and vice versa.

This effect is achieved with *Javascript*.

I had difficulties factoring the function that achieves this effect, which is why it appears several times in the **action.js** document, however a clear example of its operation is presented below:

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

This effect is applied in the following documents:

+ login.html
+ register.html
+ change_password.html

the user perceiving its effect on the following routes:

+ "/ login"
+ "/register"
+ "/change_password"
+ "/password_reset_verified"

* * *

### **Password Verification Text**

When the user begins to write the confirmation of his password, a text is displayed at the bottom of the form with three possible texts:

> 1. the password does not meet the minimum requirements yet
>
> 2. Password not match yet
> 3.Password match

This function is an adaptation of another function I got from <https://flaviocopes.com/how-to-add-event-listener-multiple-elements-javascript/>

The following is presented as it is in the document **action.js**

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

The above function is executed on the routes:

+ "/register"
+ "/change_password"
+ "/password_reset_verified"

### **Register and Login**

When the user finishes filling in the fields of the form, the page will allow them to submit the form by clicking the **Register and Login** button.

Then the route "/Register" will perform the following validations:

> + Each field has been filled
> + Passwords meet security requirements
> + The passwords match each other.
> + The email does not previously exist in the database

If the criteria are met, the route will save the user's data in the *users* table of the database and will route with the *POST* method to the route **"/login"** using the following code:

```
    return redirect(url_for("login"), code=307)
```

Getting with this that the user does not have to fill out the **"/login"** form again to start session.
* * *
### **Index**

To reach the route index **"/"** it is necessary to pass the validation carried out by the route **"/login"**, the latter verifies that the password coincides with the one created by the user, using the user's email as criteria for searching the database.

Once validated, the user logs in and is redirected to the route **"/"** whose sole purpose is to display the **index.html** document.

**index.html** offers an explanation of how to navigate the web application, as well as what functions can be found in the main parts.

* * *
### **"/food_table"**

Its sole purpose is to display the food_table.html document and serve as a container to display the content of the route **"/search"**. works only with the *GET* method.

However, it is very useful, through it the user can consult all the emojis related to food, both through the buttons that are displayed on the page and through the text box that is at the top of it.

More information about it in the part that deals with **Database** and the route **"/like_it"**.

* * *

### **"/acount"**

Initially, it displays the acount.html document and serves as a container to display the content of the route **"/search"**.

In acount, the emojis that the user has "liked" are displayed in the form of buttons, with the same format as the buttons present in **"/food_table"**, with the difference that the content displayed by ** "/serch"** changes the *like* button to a *delete* button.

deletion of emojis is achieved via the same route **"/acount"** when it is executed with the *POST* method

More information about it in the part that deals with the Database.
* * *

### **"/favourites"**

Its sole purpose is to display the favorites.html document and serve as a container to display the contents of the path **"/search"**. works only with the *GET* method.

In favorites, a count is displayed of the 5 emojis with the most likes on the page, ordered from highest to lowest.

* * *

## **Database**

### **img.csv and reader.py**
I initially created a database in Sqlite3 as implemented in the latest CS50x classes, however when I tried to port my database to Heroku, I got the following article
<a><https://devcenter.heroku.com/articles/sqlite3></a> which explains that it is better to use Postgre instead.
So reading and searching the web I was lucky enough to find the following <a href="https://www.youtube.com/watch?v=gu980iXwY5c">video</a> that explains how to implement a PostgreSQL database in Heroko.
In the "extra" folder of this repository there are two files "img.csv" and "reader.py" these were used in the database creation process.
img.csv has all the information that is used for the
Emoji table.

### **Column "hexa"**

the first column of this file is the hexadecimal code in "string" format of the respective emojii and ends up occupying the second column of the emojis table in the database.
This "hexadecimal" column is used to display content in the **food_table.html**, **favorites.html** and **acount.html** documents.
this by means of loops written in *"Jinja"*

```
{% for img in imgs %}
    <button class="image" translate="no"
        value="&#{{img.hexa}">
        &#{{img.hexa}}
    </button>
{% endfor %}
```

### **"/search"**

the route **"/search"** is used to search for the information of an emoji by converting the input of an emoji to a string format compatible with the column **hexa** stored in the database.

**"/search"** always returns the document **search.html** this document is dynamically generated using *Jinja* syntax so if no match is found the route returns the document **search.html* * empty.

the route **"/search"** is called from the docs:

> + food_table.html
> + favorites.html
> + account.html
> 
### **Photos and descriptive text**

The second column of the "img.csv" document contains the names of the emojis, these are only used to display them within the **search.html** file, which in turn is displayed through one of two asionochronous functions within the files within the three files mentioned above. specifically inside the container.

````
    <div id="container-to-item-selected"></div>
````

The asynchronous functions that perform this action are found between line 60 and 85 of the "action.js" document and this in turn is in the "static" folder of this repository.
it is practically the same explained in lecture 9 of the CS50x course.


````
let searchButton = document.querySelector('#search-button');
        searchButton.addEventListener('click', async function() {
            let response = await fetch('/search?q=' + document.querySelector('#input-emoji').value);
            let shows = await response.text();
            document.getElementById('container-to-item-selected').innerHTML = shows;

            afterSelected()
        });
````
both functions perform the same job, the difference is that one of them is activated by means of the buttons displayed in the files "food_table.html", "favorites.html" and "acount.html".
while the other does it from a "search" button that is present exclusively at the top of the "food_table.html" file.

the third column of the "img.csv" document contains the paths of the images to be displayed within the "search.html" file. specifically on line 12.
````
    <img translate="no" class="img-serched" src="{{data.img}}" alt="{{data.name}}">
````

the fourth and last line of the "img.csv" document contains the descriptive text. specifically on line 15.
````
    <p>{{data.description}}</p>
````

In turn, the reader.py file has the purpose of loading the data of the "img.csv" document in the database.
this was done before implementing this application so the presence of both "img.csv" and "reader.py" files is merely illustrative.

the database has 2 additional tables:
 "users" that is used to store the id, name, email and password of the users.
 "preferences" that is used to keep track of which emojis a user has "liked". It has only two columns, one for the "user_id" of the user and one for the "emoji_id" of the emoji.

* * *

### **"/like_it"**

This route saves in the *preferences* table of the database the *id* of the user and the *id* of the emoji that the user just *liked*.

The route **"/like_it"** is accessed through a form that is inside the **search.html** document, so it is possible to access said route in:

+ "/food_table"
+ "/faovrites"

the following function modifies the route attribute of **search.html** in the case of being in **"/acount"**

Line 48 of **action.js**

````
    if(window.location.pathname == "/acount") {

                document.getElementById('form-like-and-delete').setAttribute('action', '/acount');
                document.getElementById('form-like-and-delete').setAttribute('method', 'post');
                document.getElementById('button-item-selected-like').innerHTML = "Delete";
            }
````

This prevents the path **"/like_it"** from being accessed within the path **"/acount"**.

* * *

### **"/password_reset"**

This route is accessed through a link found just below the *password* text box on the **login** page.

It displays the document **send_reset_password.html** so that the user can get an email with a link that allows him to re-enter the application.

For this message to be sent, the user must enter their email in the text box and click on *Submit Email*.

In case the email coincides with one registered in the database, the following functions will be applied:
> my_tools.py
> > get_reset_token
>
> > reset_password_message

* * *

### **get_reset_token**

takes as input the *id* of the user. in turn, the *id* is obtained using the *email* provided by the user as search criteria.

encodes the *id* into a fairly long token.

* * *

### **reset_password_message**

Take as input:

+ recipient
+ username
+ token

it returns a Message object, with various *html* tags and built-in styling, but the most important thing it carries is the *token* created by **get_reset_token**.

* * *

### **"/password_reset_verified"**

This path can be reached from the link embedded in the email sent by **reset_password_message**.

It is responsible for identifying which user is tarata in order to be able to change the access code and that the user can log in with his new password.

this is achieved via the **verify_reset_token** function which decodes the token *extracts* the *id*.

After extracting the *id*, the document **change_password.html** is displayed, which contains a form to reset the password.

finally, if the password passes the validations (same views in **"/register"**) the password is updated in the database and the user is redirected to **"/login"** so that he can log in .

In case the token that accompanies the route **"/password_reset_verified"** is not valid, the user will be redirected to **"/password_reset"**.


I toke the idea from https://medium.com/@stevenrmonaghan/password-reset-with-flask-mail-protocol-ddcdfc190968

and specially from https://www.youtube.com/watch?v=zYWpEJAHvaI
* * *

### **"/change_password"**

This path displays the **change_password.html** document. In this case, the document will include a third text box which is generated with *Jinja* syntax in case it is being accessed without the token being present, that is, with a session started.

This route can be accessed through the *change password* button found on the *My account* page.

allows changing the password as long as the current password is provided and the validation criteria for the new password are met.

* * *

### **Clear-Night Mode**

to create the appearance change use CSS variables. I didn't know there were variables in CSS, I found out about them from a comment on a video on another topic. here is some documentation https://developer.mozilla.org/es/docs/Web/CSS/Using_CSS_custom_propertie

with this I declare in these "variables" in the root, assigning the values ​​to corresponding to the clear theme.
in line 21 of "style.css"

````
:root {
  --back--color: #A5F1E9;
  --let--color: rgb(0, 0, 0);
  --border--color: #7FBCD2;
  --pad--color: #A5FF4B;
  --key-word--color: blue;
  --let--size: 1.4rem;
}
````

then I apply those variables throughout the style.css document. for example, on line 39.

````
body {
  background-color: var(--back--color);
  color: var(--let--color);
}
````

Next I properly define the values ​​of the light and night themes. which I call "sun" and "moon".

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

In order to change themes I tried unsuccessfully to make a function in "app.py" to save the theme the user chose.

finally after some googling i found out something about how to save some data on the client side using something called **"sessionStorage.mode"**.
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
