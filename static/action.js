// desplegar ultimo tema en uso 
// puede y debe ser antes de desplegar la ventana
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
    
    // using sun emoji for change the tema
    document.getElementById('sun').addEventListener('click', function(){
        document.querySelector('#mode input[type="checkbox"]').checked = false;
        document.documentElement.setAttribute('tema', 'sun');
        sessionStorage.mode = document.documentElement.getAttribute('tema');
    });
    
    // using moon emoji for change the tema
    document.getElementById('moon').addEventListener('click', function(){
        document.querySelector('#mode input[type="checkbox"]').checked = true;
        document.documentElement.setAttribute('tema', 'moon');
        sessionStorage.mode = document.documentElement.getAttribute('tema');
    });

    if(window.location.pathname == "/acount" || window.location.pathname == "/food_table" || window.location.pathname == "/favorites") 
    {
        
        // Moviendo la pantalla "scrolling" hasta el container
        function afterSelected() {
            window.scrollTo(0, document.body.scrollHeight);

            // changing funtion of like button for an delete button in acount page
            if(window.location.pathname == "/acount") {

                document.getElementById('form-like-and-delete').setAttribute('action', '/acount');
                document.getElementById('form-like-and-delete').setAttribute('method', 'post');
                document.getElementById('button-item-selected-like').innerHTML = "Delete";
            }
            
            // distinging if display the favorite page or food_table page after make click in "like" button.
            if(window.location.pathname == "/favorites") {
                document.getElementById('procedencia').setAttribute('value', 'favorites');
            }
        }
        // searching from emojis buttons. it works on the three pages (acount, food_table and favorites)
        const emojis = document.getElementsByClassName('imagen');
            for (i = 0; i < emojis.length; i++) {
                emojis[i].addEventListener('click', async function() {
                    let response = await fetch('/search?q=' + this.innerHTML);
                    let shows = await response.text();
                    document.getElementById('container-to-item-selected').innerHTML = shows;

                    afterSelected()
            });
        }
    }

    // this input is just on food_table page
    if(window.location.pathname == "/food_table" ) {
        
        // searching from input-box
        let searchButton = document.querySelector('#search-button');
        searchButton.addEventListener('click', async function() {
            let response = await fetch('/search?q=' + document.querySelector('#input-emoji').value);
            let shows = await response.text();
            document.getElementById('container-to-item-selected').innerHTML = shows;

            afterSelected()
        });
    }
    
    // Using emojis for show and hide the password

    // This if is for limit the aplication of this function. it works on login, register, and change_password pages 
    if(window.location.pathname != "/password_reset" && window.location.pathname != "/acount"
    && window.location.pathname != "/favorites" && window.location.pathname != "/food_table" && window.location.pathname != "/"
    && window.location.pathname != "/search"  && window.location.pathname != "/logout" && window.location.pathname != "/like_it") {
        // Using emojis for show and hide the password
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
    }

    // This if is for limit the aplication of this function. it works on register and change_password pages
    if(window.location.pathname != "/password_reset" && window.location.pathname != "/login" && window.location.pathname != "/acount"
    && window.location.pathname != "/favorites" && window.location.pathname != "/food_table" && window.location.pathname != "/"
    && window.location.pathname != "/search"  && window.location.pathname != "/logout" && window.location.pathname != "/like_it") {
        
        // Using emojis for show and hide the password
        document.getElementById('confirmation-emoji').addEventListener('click', function() {
            if (this.innerHTML == '🙈') {
                this.innerHTML = '👀';
                document.getElementById('confirmation').type = "text";    
            } 
            else
            {
                this.innerHTML = '🙈';
                document.getElementById('confirmation').type = "password";
            }
        });

        // checking if password an confirmation-password match on-live
        // I toke this function from https://flaviocopes.com/how-to-add-event-listener-multiple-elements-javascript/
            
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
                    match.innerHTML = "Password not valid yet &#129300";
                }

                else if (password == confirmation) {
                    match.innerHTML = "Password match &#128077";
                }
                else {
                    match.innerHTML = "Password not match yet &#129300";
                }

            })
        });

        //copied from an answer in https://stackoverflow.com/questions/19605150/regex-for-password-must-contain-at-least-eight-characters-at-least-one-number-a
        


    }


    // This if is for limit the aplication of this function. it just works on change_password page.
    if(window.location.pathname != "/password_reset" && window.location.pathname != "/login" && window.location.pathname != "/acount"
    && window.location.pathname != "/favorites" && window.location.pathname != "/food_table" && window.location.pathname != "/"
    && window.location.pathname != "/search"  && window.location.pathname != "/logout" && window.location.pathname != "/like_it"
    && window.location.pathname != "/register") {
        // Using emojis for show and hide the password
        document.getElementById('old_password-emoji').addEventListener('click', function() {
            if (this.innerHTML == '🙈') {
                this.innerHTML = '👀';
                document.getElementById('old_password').type = "text";    
            } 
            else
            {
                this.innerHTML = '🙈';
                document.getElementById('old_password').type = "password";
            }
        });
        
    }
}
