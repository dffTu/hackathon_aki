let button_prev_month = document.getElementById("button_prev_month");
let button_next_month = document.getElementById("button_next_month");

let calendar_window = document.getElementById("calendar-window")

let month1 = document.getElementById("month_table_1");
let month2 = document.getElementById("month_table_2");
let month3 = document.getElementById("month_table_3");

function timetable_button_click(clicked_button) {
    let description_block = document.createElement('div');

    description_block.id = "new_form_for_button";
    description_block.style.zIndex = "1";
    description_block.style.position = "fixed";
    description_block.style.display = "flex";
    description_block.style.overflow = "auto";
    description_block.style.background = "red";
    description_block.style.width = "40%";
    description_block.style.height = "30%";
    description_block.innerText = "Дата: " + clicked_button.getAttribute("event_day") +
        " " + clicked_button.getAttribute("event_month") + "\n" +
    "Цена: " + clicked_button.getAttribute("event_price") + "\n" +
    "Статус: " + clicked_button.getAttribute("event_status") + "\n" +
    "Документ (оферта): " + "здесь должна быть какая-то ссылка";


    calendar_window.style.display = "flex";
    calendar_window.append(description_block);
}

button_prev_month.onclick = function () {
    if (get_current_month() === month1) return;
    if (get_current_month() === month2) {
        set_data(month1, month2);
    } else {
        set_data(month2, month3);
    }
}

button_next_month.onclick = function () {
    if (get_current_month() === month3) return;
    if (get_current_month() === month2) {
        set_data(month3, month2);
    } else {
        set_data(month2, month1);
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
        document.getElementById("new_form_for_button").remove();
        calendar_window.style.display = "none";
    }
}