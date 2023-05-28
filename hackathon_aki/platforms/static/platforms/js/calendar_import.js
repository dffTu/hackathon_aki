"use strict"

document.addEventListener("DOMContentLoaded", document_init);

function document_init() {
    let mport_calendar_form = document.getElementById("mport_calendar_form");
    let import_calendar_button = document.getElementById("import_calendar_button");
    let file_field = document.getElementById("calendar_importing_file_field");

    file_field.style.display = 'none';

    if (import_calendar_button) {
        import_calendar_button.onmousedown = function () {
            if (import_calendar_button.firstChild.data == 'Импортировать') {
                import_calendar_button.firstChild.data = 'Сохранить';
                file_field.style.display = 'block';
                file_field.click();
            } else {
                mport_calendar_form.submit();
            }
        }
    }
}
