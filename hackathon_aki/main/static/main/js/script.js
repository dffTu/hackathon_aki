var modal = document.getElementById("authorize-window");

var authorize_window = document.getElementById("authorize-content");
var register_window = document.getElementById("register-content");
var log_in_window = document.getElementById("log-in-content");

var open_user_button = document.getElementById("open-user");

var register_button = document.getElementById("register");
var log_in_button = document.getElementById("log-in");

var register_client_button = document.getElementById("register-client");
var register_organizer_button = document.getElementById("register-organizer");

var register_client_window = document.getElementById("register-window-client");
var register_organizer_window = document.getElementById("register-window-organizer");

open_user_button.onclick = function () {
    modal.style.display = "block";
    authorize_window.style.display = "flex";
    log_in_window.style.display = "flex";
}

register_button.onclick = function () {
    register_window.style.display = "flex";
    log_in_window.style.display = "none";
}

register_client_button.onclick = function () {
    register_client_window.style.display = "flex";
    register_organizer_window.style.display = "none";
}

register_organizer_button.onclick = function () {
    register_organizer_window.style.display = "flex";
    register_client_window.style.display = "none";
}


log_in_button.onclick = function () {
    log_in_window.style.display = "flex";
    register_window.style.display = "none";
    register_organizer_window.style.display = "none";
    register_client_window.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
        authorize_window.style.display = "none";
        register_window.style.display = "none";
        log_in_window.style.display = "none";
    }
}