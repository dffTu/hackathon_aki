"use strict"

document.addEventListener("DOMContentLoaded", document_init);

function document_init() {
    const form = document.getElementById("profile_changing_form");
    const button = document.getElementById("change_profile_button");
    const form_elements = Array.from(form.elements);

    let profile_changing = false;

    form_elements.forEach((input) => {
        input.readOnly = true;
    });

    if (document.getElementById("form_has_errors") != null) {
        switch_button_view();
    }

    button.onmousedown = function() {
        if (!profile_changing) {
            switch_button_view();
        } else {
            form.submit();
        }
    }

    function switch_button_view() {
        profile_changing = true;
        button.firstChild.data = 'Сохранить профиль';

        form_elements.forEach((input) => {
            if (!input.hasAttribute('immutable')) {
                input.readOnly = false;
            }
        });
    }
}
