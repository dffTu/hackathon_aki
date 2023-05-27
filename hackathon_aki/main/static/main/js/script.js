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

let forget_password_link = document.getElementById('forget_password_link');
let forget_password_hint = document.getElementById('forget_password_hint');
let login_form_password = document.getElementById('login_form_password');
let login_form_password_label = document.getElementById('login_form_password_label');

function drop_password_reset_form() {
    login_form_button.firstChild.data = 'Войти';
    is_password_reset_input.value = '';

    forget_password_link.style.display = 'block';
    login_form_password.style.display = 'block';
    login_form_password_label.style.display = 'block';
    forget_password_hint.style.display = 'none';

    let login_form_errors = document.getElementById('login_form_errors');
    if (login_form_errors) {
        login_form_errors.style.display = 'block';
    }
}

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

    drop_password_reset_form();
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
            drop_password_reset_form();
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

function open_user_button_onmousedown_func() {
    modal.style.display = "flex";
    authorize_window.style.display = "inline-block";
    log_in_window.style.display = "flex";

    localStorage.setItem("modal_style_display", "flex");
    localStorage.setItem("authorize_window_style_display", "inline-block");
    localStorage.setItem("log_in_window_style_display", "flex");
}

if (open_user_button) {
    open_user_button.onmousedown = open_user_button_onmousedown_func;
}

if (register_button) {
    register_button.onmousedown = function () {
        organizer_client_buttons.style.display = "flex";
        register_window.style.display = "flex";
        log_in_window.style.display = "none";
        drop_password_reset_form();
        localStorage.setItem("register_window_style_display", "flex");
        localStorage.setItem("log_in_window_style_display", "none");
        localStorage.setItem("organizer_client_buttons_style_display", "flex");
    }
}

if (register_client_button) {
    register_client_button.onmousedown = function () {
        register_client_window.style.display = "flex";
        register_organizer_window.style.display = "none";

        localStorage.setItem("register_client_window_style_display", "flex");
        localStorage.setItem("register_organizer_window_style_display", "none");
    }
}

if (register_organizer_button) {
    register_organizer_button.onmousedown = function () {
        register_organizer_window.style.display = "flex";
        register_client_window.style.display = "none";

        localStorage.setItem("register_client_window_style_display", "none");
        localStorage.setItem("register_organizer_window_style_display", "flex");
    }
}

if (log_in_button) {
    log_in_button.onmousedown = function () {
        log_in_window.style.display = "flex";
        register_window.style.display = "none";
        register_organizer_window.style.display = "none";
        register_client_window.style.display = "none";

        localStorage.setItem("register_window_style_display", "none");
        localStorage.setItem("log_in_window_style_display", "flex");
        localStorage.setItem("register_client_window_style_display", "none");
        localStorage.setItem("register_organizer_window_style_display", "none");
    }
}

window.onmousedown = function(event) {
    if (event.target === modal) {
        setDefaultValues();
    }
}