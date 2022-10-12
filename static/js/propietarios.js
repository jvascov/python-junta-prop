addAptoBtn = document.getElementById("add-apto-btn");
addPropBtn = document.getElementById("add-prop-btn");
propietariosMnu = document.getElementById("propietarios-mnu");

apartamentos = [];
idApto = 0;

function formatoMayusculaInicial(frase) {
    if (typeof frase != 'string') {
        throw TypeError('El argumento debe ser una cadena de caracteres (texto).');
    }

    let palabras = frase.split(' ');

    return palabras.map(p => p[0].toUpperCase() + p.slice(1)).join(' ');
}

function listarPropietario(propietario) {
    tblPropietarios = document.getElementById('tbl-propietarios');

    let fila = document.createElement("tr");
    //fila.setAttribute("class", 'reg-contacto');
    fila.setAttribute("id", `reg-${propietario.id}`);

    let cmpNombre = document.createElement("td");
    cmpNombre.innerHTML = `${formatoMayusculaInicial(propietario.nombre)}`;
    fila.appendChild(cmpNombre);

    let cmpCelular = document.createElement("td");
    cmpCelular.innerHTML = propietario.celular;
    fila.appendChild(cmpCelular);

    let cmpEmail = document.createElement("td");
    cmpEmail.innerHTML = propietario.email;
    fila.appendChild(cmpEmail);

    let cmpRole = document.createElement("td");
    cmpRole.innerHTML = formatoMayusculaInicial(propietario.role);
    fila.appendChild(cmpRole);

    let cmpOpciones = document.createElement("td");
    cmpOpciones.innerHTML = `<a href="#contenedor-edicion" onclick="buscarContacto('${propietario.id}')" >
    <span class="material-icons-outlined material-icons icono-accion">
    edit
    </span></a> <a href="#contenedor-edicion" onclick="buscarContacto('${propietario.id}')" >
    <span class="material-icons-outlined material-icons icono-accion">
    zoom_in
    </span></a>`;
    fila.appendChild(cmpOpciones);

    tblPropietarios.appendChild(fila);
}

function mostrarFormAgregar() {
    document.getElementById('contenedor-edicion').style.display = 'grid';
    document.getElementById('opciones-btn').style.display = 'none';
    apartamentos = [];
    document.getElementById('cedula-add').value = '';
    document.getElementById('nombre-add').value = '';
    document.getElementById('celular-add').value = '';
    document.getElementById('email-add').value = '';
    document.getElementById('aptos-tbl').innerHTML = `<tr>
    <th>Torre</th>
    <th>Número</th>
</tr>
`;


    //document.getElementById('titulo-modal').innerHTML = 'Adicionar Contacto';
    //document.getElementById('nombre-add').value = '';
    /*document.getElementById('datos-canal-tbl').innerHTML = `<tr>
    <th>
        Canal
    </th>
    <th>
        Cuenta
    </th>
    <th>
        Preferencia
    </th>
    <th>
    </th>
</tr>`;
    
    idCanal = 0;
    */
}

function borrarApartamento(id) {
    console.log('id ', id);
    const aptosTbl = document.getElementById('aptos-tbl');

    filaApto = document.getElementById(`apto-${id}`);

    console.log(filaApto);
    aptosTbl.removeChild(filaApto);

    apartamentos.forEach(function (apto, index, object) {
        if (apto.id == id) {
            object.splice(index, 1);
            //alert('borra');
        }
    });

    console.log('apartamentos ', apartamentos);
}

function mostrarApartamento(apartamento) {
    let aptoTbl = document.getElementById('aptos-tbl');
    let fila = document.createElement("tr");
    fila.setAttribute("id", `apto-${apartamento.id}`);
    console.log('apartamento ', apartamento);
    let cmpTorreApto = document.createElement("td");
    cmpTorreApto.innerHTML = apartamento.torre;
    fila.appendChild(cmpTorreApto);

    let cmpNumApto = document.createElement("td");
    cmpNumApto.innerHTML = apartamento.numero
    fila.appendChild(cmpNumApto);

    let cmpBorrarApto = document.createElement("td");
    cmpBorrarApto.innerHTML = `<span class="material-icons-outlined material-icons icono-accion" onclick="borrarApartamento(${apartamento.id})">
    delete
    </span>`;
    fila.appendChild(cmpBorrarApto);

    aptoTbl.appendChild(fila);

    document.getElementById('torre-add').value = '';
    document.getElementById('num-add').value = '';
}

function adicionarApartamento() {
    torreCmp = document.getElementById('torre-add').value;
    numeroCmp = document.getElementById('num-add').value;
    if (torreCmp == '' || numeroCmp == '') {
        alert('Por favor ingrese los datos del apartamento')
        return
    }

    idApto++;
    apartamento = {
        torre: torreCmp,
        numero: numeroCmp,
        id: idApto
    }
    apartamentos.push(apartamento);
    mostrarApartamento(apartamento)
}

function adicionarPropietario(propietario) {
    console.log('propietario', propietario);
    fetch('http://localhost:8080/propietarios', {
        method: 'POST',
        body: JSON.stringify(propietario),
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(response => {
            console.log(response);
            if (response.status == 'error' || response.status == 'fail') {
                throw new Error(response.message);
            }

            inicializar();
            mostrarFormAgregar();
            document.getElementById('contenedor-edicion').style.display = 'none';
            document.getElementById('opciones-btn').style.display = 'inline-block';

        }).catch(error => {

            console.error('Error:', error);
            alert('Error guardando propietario: ' + error.message);
        });
}

function inicializar() {

    document.getElementById('tbl-propietarios').innerHTML = `<tr>
    <th>
        <div class="titulo">
            <span>Nombre</span>
        </div>
    </th>
    <th>
        <div class="titulo">
            Celular
        </div>
    </th>
    <th>
        <div class="titulo">Email
        </div>
    </th>
    <th>
        <div class="titulo">Role
        </div>
    </th>
    <th>
    </th>
</tr>
`;
    fetch('http://localhost:8080/propietarios', {
        method: 'GET'
    })
        .then(response => response.json())
        .then(response => {
            if (response.status == 'error' || response.status == 'fail') {
                throw new Error(response.message);
            }

            for (i = 0; i < response.length; i++) {
                propietario = {
                    id: response[i].id,
                    nombre: response[i].nombre,
                    celular: response[i].celular,
                    email: response[i].email,
                    role: response[i].role,
                }

                listarPropietario(propietario);
            }

        })

}

addAptoBtn.addEventListener("click", adicionarApartamento)

addPropBtn.addEventListener("click", e => {
    let propietario = {};
    propietario.id = document.getElementById('cedula-add').value;
    propietario.nombre = document.getElementById('nombre-add').value;
    propietario.celular = document.getElementById('celular-add').value;
    propietario.email = document.getElementById('email-add').value;
    propietario.role = document.getElementById('role-add').value;
    propietario.password = '123456';
    if (propietario.nombre == '' || propietario.celular == '' || propietario.email == '' || propietario.cedula == '') {
        alert('Por favor ingrese todos los datos del propietario')
        return
    }


    propietario.apartamento = apartamentos;

    adicionarPropietario(propietario);
})

propietariosMnu.addEventListener("click", () => {
    window.location.href = "http://localhost:8080/propietarios/";
})

inicializar();