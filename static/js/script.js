btnLogin = document.getElementById("enviar-btn");


async function login() {

    await fetch('http://localhost:8080/login', {
        method: 'POST',
        body: JSON.stringify({
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        }),
        headers: {
            "Content-type": "application/json"
        }
    })
        .then(response => response.json())
        .then(response => {
            if (response.status == 'error' || response.status == 'fail') {
                throw new Error(response.message);
            }

            if (response.user.registered == true) {
                console.log(response);
                user = {
                    id: response.user.localId,
                    nombre: response.datos.nombre,
                    documento: response.datos.id,
                    email: response.datos.email,
                    perfil: response.datos.role
                }
                localStorage.setItem('user', JSON.stringify(user));
            } else {
                throw new Error("Error iniciando sesión");
            }
            window.location.href = "http://localhost:8080/opciones/";
        })
        .then(json => console.log(json))
}

btnLogin.addEventListener("click", login)