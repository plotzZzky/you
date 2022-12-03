//LoginTabs
function show_login(tab) {
    set_tabs_inactive();
    document.getElementById("Login").style.display = "block";
    tab.id = "tab-active";
    document.getElementById("Signup").style.display = "none";
}


function show_signup(tab) {
    set_tabs_inactive();
    document.getElementById("Login").style.display = "none";
    tab.id = "tab-active";
    document.getElementById("Signup").style.display = "block";
}

function set_tabs_inactive() {
    var elements = document.getElementsByClassName('tablinks');
    for (var i in elements) {
        if (elements.hasOwnProperty(i)) {
        elements[i].id = " ";
    }
    }
}


//forma validation
function validSignup(form) {
    var username = form['username'].value;
    var password = form['password'].value;
    var pwd = form['pwd'].value;
    var email = form['email'].value;

    if (validUsername(username) != true) {
        alert('O Nome do usario deve ter no minimo 3 caracteres');
        return false;
    }

    if (validPassword(password) != true){
        alert("Senha deve ter no minimo 3 caractres")
        return false;
    }

    if (validPassword(pwd) != true) {
        alert("Senha deve ter no minimo 3 caractres")
        return false;
    }

    if (validEmail(email) != true) {
        alert("Email invalido!")
        return false;
    }
}

function validLogin(form) {
    var username = form['username'].value;
    var password = form['password'].value;

    if (validUsername(username) != true) {
        alert('O Nome do usario deve ter no minimo 3 caracteres');
        return false;
    }

    if (validPassword(password) != true){
        alert("Senha deve ter no minimo 3 caractres")
        return false;
    }
}


function validPassword(pwd){
    var min = 3;
    if (pwd.length >= min){
        return true;
    } else {
        return false;
    }
}

function validUsername(username) {
    if (username.length >= 3) {
        return true;
    } else {
        return false;
    }
}

function validEmail(email){
    if (email.length >= 11){
        return true;
    } else {
        return false;
    }
}
