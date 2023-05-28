let button_prev_month = document.getElementById("button_prev_month");
let button_next_month = document.getElementById("button_next_month");

let calendar_window = document.getElementById("calendar-window");

let confirm_deletion_platform_window = document.getElementById("confirm_delete_platform_window");
let confirm_deletion_entry_window = document.getElementById("confirm_deletion_entry_window");
let confirm_deletion_registration_window = document.getElementById("confirm_deletion_registration_window");

let adding_comment_window = document.getElementById("adding_comment_window");

let desc_import_calendar_button = document.getElementById('desc_import_calendar_button');
let button_description_window = document.getElementById("button_description_window");

let month1 = document.getElementById("month_table_1");
let month2 = document.getElementById("month_table_2");
let month3 = document.getElementById("month_table_3");

let login_calendar_registrate_button = document.getElementById("login_calendar_registrate_button");

let delete_platform_button = document.getElementById("delete_platform");

let change_price_button = document.getElementById("change_price_button");
let delete_entry_button = document.getElementById("delete_entry_button");
let delete_registration_button = document.getElementById("delete_registration_button");
let add_entry_button = document.getElementById("add_entry_button");
let add_registration_button = document.getElementById("add_registration_button");

let cancel_deletion_platform_button = document.getElementById("cancel_deletion_platform_button");
let cancel_deletion_entry_button = document.getElementById("cancel_deletion_entry_button");
let cancel_deletion_registration_button = document.getElementById("cancel_deletion_registration_button");
let cancel_change_price_button = document.getElementById("cancel_change_price_button");

let add_comment_button = document.getElementById("add_comment_button");

let get_arendator_info_button = document.getElementById("get_arendator_info_button");

if (button_prev_month) {
    button_prev_month.onmousedown = function () {
        if (get_current_month() === month1) return;
        if (get_current_month() === month2) {
            set_data(month1, month2);
        } else {
            set_data(month2, month3);
        }
    }
}

if (button_next_month) {
    button_next_month.onmousedown = function () {
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

if (add_comment_button) {
    add_comment_button.onmousedown = function () {
        adding_comment_window.style.display = "flex";
    }
}

function timetable_button_click(clicked_button) {
    document.getElementById('date-paragraph-calendar-window-form').textContent =
        clicked_button.getAttribute("event_day") + " " + clicked_button.getAttribute("event_month_text");
    document.getElementById('price-paragraph-calendar-window-form').textContent =
        clicked_button.getAttribute("event_price") + " тыс. ₽";
    document.getElementById('file-paragraph-calendar-window-form').textContent = "Скачать оферту";
    calendar_window.style.display = "flex";


    let registration_link = clicked_button.getAttribute("event_add_registration_link")
    let user_link = clicked_button.getAttribute("event_user_link");
    let delete_entry_link = clicked_button.getAttribute("event_delete_entry_link");
    let add_entry_link = clicked_button.getAttribute("event_add_entry_link");
    let delete_registration_link = clicked_button.getAttribute("event_delete_registration_link");
    let change_price_link = clicked_button.getAttribute("event_change_price_link");

    if (document.getElementById("user_client_register_form")) {
        document.getElementById("user_client_register_form").action = registration_link;
        document.getElementById("__day").value = clicked_button.getAttribute("event_day");
        document.getElementById("__month").value = clicked_button.getAttribute("event_month");
        document.getElementById("__year").value = clicked_button.getAttribute("event_year");
    }

    if (document.getElementById("organizers_fields_div")) {
        let is_booked = clicked_button.getAttribute("event_is_booked");
        let is_defined = clicked_button.getAttribute("event_is_defined");

        document.getElementById("div_for_get_arendator_info_button").style.display = "";
        document.getElementById("div_for_delete_entry_button").style.display = "";
        document.getElementById("div_for_delete_registration_button").style.display = "";
        document.getElementById("div_for_add_entry_button").style.display = "";
        document.getElementById("div_for_change_price_button").style.display = "";

        if (add_entry_link != null) {
            document.getElementById("add_entry_button").setAttribute("add_entry_link",  add_entry_link);
        }

        if (change_price_link != null) {
            document.getElementById("change_price_form").action = change_price_link;
        }

        if (user_link != null) {
            document.getElementById("get_arendator_info_button").setAttribute("user_link",  user_link);
        }

        if (delete_entry_link != null) {
            document.getElementById("delete_entry_button").setAttribute("delete_entry_link",  delete_entry_link);
        }

        if (delete_registration_link != null) {
            document.getElementById("delete_registration_button").setAttribute("delete_registration_link",  delete_registration_link);
        }

        if (is_booked === "True") {
            document.getElementById("div_for_add_entry_button").style.display = "none";
            document.getElementById("div_for_change_price_button").style.display = "none";
            document.getElementById("div_for_delete_entry_button").style.display = "none";

        }
        else if (is_defined === "True") {
            document.getElementById("div_for_add_entry_button").style.display = "none";
            document.getElementById("div_for_get_arendator_info_button").style.display = "none";
            document.getElementById("div_for_delete_registration_button").style.display = "none";
        } else {
            document.getElementById("div_for_change_price_button").style.display = "none";
            document.getElementById("div_for_delete_registration_button").style.display = "none";
            document.getElementById("div_for_get_arendator_info_button").style.display = "none";
            document.getElementById("div_for_delete_entry_button").style.display = "none";
        }
    }

}

if (change_price_button) {
    change_price_button.onmousedown = function() {
        document.getElementById("change_price_window").style.display = "flex";
    }
}

if (cancel_change_price_button) {
    cancel_change_price_button.onmousedown = function() {
        document.getElementById("change_price_window").style.display = "none";
    }
}

if (get_arendator_info_button) {
    get_arendator_info_button.onmousedown = function () {
        window.location.href = get_arendator_info_button.getAttribute("user_link");
    }
}

if (add_entry_button) {
    add_entry_button.onmousedown = function() {
        window.location.href = add_entry_button.getAttribute("add_entry_link");
    }
}

window.onmousedown = function (event) {
    if (event.target === modal) {
        setDefaultValues();
    }
    if (event.target === calendar_window) {
        calendar_window.style.display = "none";
    }
    if (event.target === confirm_deletion_platform_window) {
        confirm_deletion_platform_window.style.display = "none";
    }
    if (event.target === confirm_deletion_entry_window) {
        confirm_deletion_entry_window.style.display = "none";
    }
    if (event.target === adding_comment_window) {
        adding_comment_window.style.display = "none";
    }
    if (event.target === button_description_window) {
        button_description_window.style.display = "none";
    }
}

if (desc_import_calendar_button) {
    desc_import_calendar_button.onmousedown = function() {
        button_description_window.style.display = "flex";
    }
}

if (delete_entry_button) {
    delete_entry_button.onmousedown = function() {
        confirm_deletion_entry_window.style.display = "flex";
        document.getElementById("confirm_deletion_entry_form").action = delete_entry_button.getAttribute("delete_entry_link");
    }
}

if (cancel_deletion_entry_button) {
    cancel_deletion_entry_button.onmousedown = function () {
        confirm_deletion_entry_window.style.display = "none";
    }
}

if (delete_registration_button) {
    delete_registration_button.onmousedown = function() {
        confirm_deletion_registration_window.style.display = "flex";
        document.getElementById("confirm_deletion_registration_form").action = delete_registration_button.getAttribute("delete_registration_link");
    }
}

if (cancel_deletion_registration_button) {
    cancel_deletion_registration_button.onmousedown = function () {
        confirm_deletion_registration_window.style.display = "none";
    }
}


if (delete_platform_button) {
    delete_platform_button.onmousedown = function () {
        confirm_deletion_platform_window.style.display = "flex";
    }
}

if (cancel_deletion_platform_button) {
    cancel_deletion_platform_button.onmousedown = function () {
        confirm_deletion_platform_window.style.display = "none";
    }
}

if (login_calendar_registrate_button) {
    login_calendar_registrate_button.onmousedown = function () {
        calendar_window.style.display = "none";
        open_user_button_onmousedown_func();
    }
}
