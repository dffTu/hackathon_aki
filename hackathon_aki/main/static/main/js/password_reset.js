"use strict"

document.addEventListener("DOMContentLoaded", document_init);

function document_init() {
    let forget_password_link = document.getElementById('forget_password_link');
    let forget_password_hint = document.getElementById('forget_password_hint');
    let login_form_password = document.getElementById('login_form_password');
    let login_form_password_label = document.getElementById('login_form_password_label');
    let login_form_button = document.getElementById('login_form_button');
    let is_password_reset_input = document.getElementById('is_password_reset_input');

    forget_password_hint.style.display = 'none';

    forget_password_link.onclick = function() {
        login_form_button.firstChild.data = 'Восстановить пароль';
        is_password_reset_input.value = 'Y';

        forget_password_hint.style.display = 'block';

        login_form_password.style.display = 'none';
        login_form_password_label.style.display = 'none';
        forget_password_link.style.display = 'none';

        let login_form_errors = document.getElementById('login_form_errors');
        if (login_form_errors) {
            login_form_errors.style.display = 'none';
        }
    }
}
