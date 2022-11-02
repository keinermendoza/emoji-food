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
    
}

