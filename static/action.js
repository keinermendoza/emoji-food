// desplegar ultimo tema en uso 
// puede y debe ser antes de desplegar la ventana
document.documentElement.setAttribute('tema', sessionStorage.mode);

window.onload = function() 
{   
    // Si el tema activo es 'moon' marcar chexkbox
    if (document.documentElement.getAttribute('tema') == 'moon') {
        document.querySelector('#mode input[type="checkbox"]').checked = true;
    }
    
    // Selecciono Box de Mode y agrego lamda
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
    
    // checking if password an confirmation-password match on-live
    // I toke this function from https://flaviocopes.com/how-to-add-event-listener-multiple-elements-javascript/
    var match = document.getElementById('password-state-match');
    
    [document.getElementById('password'), document.getElementById("confirmation")].forEach(item => {
        item.addEventListener('input', event => {
            password = document.getElementById('password').value;
            confirmation = document.getElementById("confirmation").value;
    
            if (password == "" || confirmation == "") {
                match.innerHTML = "";
            }
            else if (password == confirmation) {
                match.innerHTML = "Password match &#128077";
            }
            else {
                match.innerHTML = "Password not match yet &#129300";
            }
        })
    });
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

