"use strict"

document.addEventListener("DOMContentLoaded", document_init);

function document_init() {
    const form = document.getElementById("profile_form");
    const form_elements = Array.from(form.elements);

    form_elements.forEach((input) => {
        input.readOnly = true;
    });
}
