let button_prev_month = document.getElementById("button_prev_month");
let button_next_month = document.getElementById("button_next_month");

let calendar_window = document.getElementById("calendar-window");
let confirm_deletion_window = document.getElementById("confirm_delete_window");
//let adding_comment_window = document.getElementById("adding_comment_window");

let month1 = document.getElementById("month_table_1");
let month2 = document.getElementById("month_table_2");
let month3 = document.getElementById("month_table_3");

let update_price_button = document.getElementById("update_price_button");

let login_calendar_registrate_button = document.getElementById("login_calendar_registrate_button");
let delete_platform_button = document.getElementById("delete_platform");
let cancel_deletion_button = document.getElementById("cancel_delete_button");
//let add_comment_button = document.getElementById("add_comment_button");

function timetable_button_click(clicked_button) {
    document.getElementById('date-paragraph-calendar-window-form').textContent =
        clicked_button.getAttribute("event_day") + " " + clicked_button.getAttribute("event_month_text");
    document.getElementById('price-paragraph-calendar-window-form').textContent =
        clicked_button.getAttribute("event_price") + " рублей";
    document.getElementById('file-paragraph-calendar-window-form').textContent = "Скачать оферту";
    calendar_window.style.display = "flex";

    if (document.getElementById("user-organizer-register-form") != null) return;

    document.getElementById("__day").value = clicked_button.getAttribute("event_day");
    document.getElementById("__month").value = clicked_button.getAttribute("event_month");
    document.getElementById("__year").value = clicked_button.getAttribute("event_year");

    if (document.getElementById("own-platform-form")) {
        document.getElementById("form_price_field").value = clicked_button.getAttribute("event_price");
    }
}

if (button_prev_month) {
    button_prev_month.onclick = function () {
        if (get_current_month() === month1) return;
        if (get_current_month() === month2) {
            set_data(month1, month2);
        } else {
            set_data(month2, month3);
        }
    }
}

if (update_price_button) {
    update_price_button.onclick = function() {
        document.getElementById("form_price_field").readOnly = false;
        if (update_price_button.textContent === "Сохранить") {
            update_price_button.type = "submit";
        } else {
            update_price_button.textContent = "Сохранить";
        }
    }
}

if (button_next_month) {
    button_next_month.onclick = function () {
        if (get_current_month() === month3) return;
        if (get_current_month() === month2) {
            set_data(month3, month2);
        } else {
            set_data(month2, month1);
        }
    }
}

function set_data(x, y) {
    x.style.display = "block";
    y.style.display = "none";
}

function get_current_month() {
    if (month1.style.display !== "none") return month1;
    if (month2.style.display !== "none") return month2;
    return month3;
}

window.onclick = function (event) {
    if (event.target === modal) {
        setDefaultValues();
    }
    if (event.target === calendar_window) {
        calendar_window.style.display = "none";
    }
    if (event.target === confirm_deletion_window) {
        confirm_deletion_window.style.display = "none";
    }
}

if (delete_platform_button) {
    delete_platform_button.onclick = function () {
        confirm_deletion_window.style.display = "flex";
    }
}

if (cancel_deletion_button) {
    cancel_deletion_button.onclick = function () {
        confirm_deletion_window.style.display = "none";
    }
}

if (login_calendar_registrate_button) {
    login_calendar_registrate_button.onclick = function () {
        calendar_window.style.display = "none";
        open_user_button_onclick_func();
    }
}

