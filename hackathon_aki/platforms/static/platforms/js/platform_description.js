let button_prev_month = document.getElementById("button_prev_month");
let button_next_month = document.getElementById("button_next_month");

let calendar_window = document.getElementById("calendar-window");

let confirm_deletion_platform_window = document.getElementById("confirm_delete_platform_window");
let confirm_deletion_entry_window = document.getElementById("confirm_delete_entry_window");

let adding_comment_window = document.getElementById("adding_comment_window");

let month1 = document.getElementById("month_table_1");
let month2 = document.getElementById("month_table_2");
let month3 = document.getElementById("month_table_3");

let update_price_button = document.getElementById("update_price_button");

let login_calendar_registrate_button = document.getElementById("login_calendar_registrate_button");

let delete_platform_button = document.getElementById("delete_platform");
let delete_entry_button = document.getElementById("delete_entry_button");

let cancel_deletion_platform_button = document.getElementById("cancel_deletion_platform_button");
let cancel_deletion_entry_button = document.getElementById("cancel_deletion_entry_button");

let add_comment_button = document.getElementById("add_comment_button");

let get_arendator_info_button = document.getElementById("get_arendator_info_button");

function timetable_button_click(clicked_button) {
    document.getElementById('date-paragraph-calendar-window-form').textContent =
        clicked_button.getAttribute("event_day") + " " + clicked_button.getAttribute("event_month_text");
    document.getElementById('price-paragraph-calendar-window-form').textContent =
        clicked_button.getAttribute("event_price") + " рублей";
    document.getElementById('file-paragraph-calendar-window-form').textContent = "Скачать оферту";
    calendar_window.style.display = "flex";

    if (document.getElementById("__day")) {
        document.getElementById("__day").value = clicked_button.getAttribute("event_day");
        document.getElementById("__month").value = clicked_button.getAttribute("event_month");
        document.getElementById("__year").value = clicked_button.getAttribute("event_year");
    }

    if (document.getElementById("arendator_slot_info_form")) {
        document.getElementById("div_for_get_arendator_info_button").style.display = "";
        document.getElementById("div_for_delete_entry_button").style.display = "";

        let user_link = clicked_button.getAttribute("event_user_link");
        let delete_link = clicked_button.getAttribute("event_delete_link");
        if (user_link != null && delete_link != null) {
            if (document.getElementById("confirm_entry_delete_form")) {
                document.getElementById("confirm_entry_delete_form").action = delete_link;
            }
            document.getElementById("get_arendator_info_button").setAttribute("user_link", user_link);
            document.getElementById("delete_entry_button").setAttribute("delete_link", delete_link);
        }
    }

}

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

if (update_price_button) {
    update_price_button.onmousedown = function() {
        document.getElementById("form_price_field").readOnly = false;
        if (update_price_button.textContent === "Сохранить") {
            update_price_button.type = "submit";
        } else {
            update_price_button.textContent = "Сохранить";
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

if (get_arendator_info_button) {
    get_arendator_info_button.onmousedown = function () {
        window.location.href = get_arendator_info_button.getAttribute("user_link");
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
}

if (delete_entry_button) {
    delete_entry_button.onmousedown = function() {
        confirm_deletion_entry_window.style.display = "flex";
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

if (cancel_deletion_entry_button) {
    cancel_deletion_entry_button.onmousedown = function () {
        confirm_deletion_entry_window.style.display = "none";
    }
}

if (login_calendar_registrate_button) {
    login_calendar_registrate_button.onmousedown = function () {
        calendar_window.style.display = "none";
        open_user_button_onmousedown_func();
    }
}

if (add_comment_button) {
    add_comment_button.onmousedown = function () {
        adding_comment_window.style.display = "flex";
    }
}

