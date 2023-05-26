let modal = document.getElementById("authorize-window");

let authorize_window = document.getElementById("authorize-content");
let register_window = document.getElementById("register-content");
let log_in_window = document.getElementById("log-in-content");

let open_user_button = document.getElementById("open-user");

let register_button = document.getElementById("register");
let log_in_button = document.getElementById("log-in");

let organizer_client_buttons = document.getElementById("buttons_ar");

let register_client_button = document.getElementById("register-client");
let register_organizer_button = document.getElementById("register-organizer");

let register_client_window = document.getElementById("register-window-client");
let register_organizer_window = document.getElementById("register-window-organizer");

function setDefaultValues() {
    localStorage.setItem("modal_style_display", "none");
    localStorage.setItem("authorize_window_style_display", "none");
    localStorage.setItem("register_window_style_display", "none");
    localStorage.setItem("log_in_window_style_display", "none");
    localStorage.setItem("register_client_window_style_display", "none");
    localStorage.setItem("register_organizer_window_style_display", "none");
    localStorage.setItem("organizer_client_buttons_style_display", "none");

    modal.style.display = "none";
    authorize_window.style.display = "none";
    register_window.style.display = "none";
    log_in_window.style.display = "none";
    register_client_window.style.display = "none";
    register_organizer_window.style.display = "none";
    organizer_client_buttons.style.display = "none";
}

window.onload = function() {
    let drop_localstorage = document.getElementById("drop_localstorage");
    if (drop_localstorage != null) {
        setDefaultValues();
    } else {
        let res = localStorage.getItem("modal_style_display");
        if (res === null) {
            modal.style.display = "none";
        } else {
            modal.style.display = res;
        }

        res = localStorage.getItem("authorize_window_style_display");
        if (res === null) {
            authorize_window.style.display = "none";
        } else {
            authorize_window.style.display = res;
        }

        res = localStorage.getItem("register_window_style_display");
        if (res === null) {
            register_window.style.display = "none";
        } else {
            register_window.style.display = res;
        }

        res = localStorage.getItem("log_in_window_style_display");
        if (res === null) {
            log_in_window.style.display = "none";
        } else {
            log_in_window.style.display = res;
        }

        res = localStorage.getItem("register_client_window_style_display");
        if (res === null) {
            register_client_window.style.display = "none";
        } else {
            register_client_window.style.display = res;
        }

        res = localStorage.getItem("register_organizer_window_style_display");
        if (res === null) {
            register_organizer_window.style.display = "none";
        } else {
            register_organizer_window.style.display = res;
        }

        res = localStorage.getItem("organizer_client_buttons_style_display");
        if (res === null) {
            organizer_client_buttons.style.display = "none";
        } else {
            organizer_client_buttons.style.display = res;
        }
    }
}

function open_user_button_onclick_func() {
    modal.style.display = "flex";
    authorize_window.style.display = "inline-block";
    log_in_window.style.display = "flex";

    localStorage.setItem("modal_style_display", "flex");
    localStorage.setItem("authorize_window_style_display", "inline-block");
    localStorage.setItem("log_in_window_style_display", "flex");
}

open_user_button.onclick = open_user_button_onclick_func;

register_button.onclick = function () {
    organizer_client_buttons.style.display = "flex";
    register_window.style.display = "flex";
    log_in_window.style.display = "none";localStorage.setItem("register_window_style_display", "flex");
    localStorage.setItem("log_in_window_style_display", "none");
    localStorage.setItem("organizer_client_buttons_style_display", "flex");
}

register_client_button.onclick = function () {
    register_client_window.style.display = "flex";
    register_organizer_window.style.display = "none";

    localStorage.setItem("register_client_window_style_display", "flex");
    localStorage.setItem("register_organizer_window_style_display", "none");
}

register_organizer_button.onclick = function () {
    register_organizer_window.style.display = "flex";
    register_client_window.style.display = "none";

    localStorage.setItem("register_client_window_style_display", "none");
    localStorage.setItem("register_organizer_window_style_display", "flex");
}

log_in_button.onclick = function () {
    log_in_window.style.display = "flex";
    register_window.style.display = "none";
    register_organizer_window.style.display = "none";
    register_client_window.style.display = "none";

    localStorage.setItem("register_window_style_display", "none");
    localStorage.setItem("log_in_window_style_display", "flex");
    localStorage.setItem("register_client_window_style_display", "none");
    localStorage.setItem("register_organizer_window_style_display", "none");
}

window.onclick = function(event) {
    if (event.target === modal) {
        setDefaultValues();
    }
}