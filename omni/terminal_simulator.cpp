#include <ncurses.h>
#include <iostream>
#include <map>
#include <vector>
#include <string>
#include <iomanip>
#include <sstream>
#include <regex>

// Options and initial values
std::vector<std::string> mode_options = {"Retail", "Pay at Table"};
std::vector<std::string> error_options = {"Enable Declines", "Enable Cancellations", "Stop Response", "None"};
int selected_radio = 0;
int selected_error_radio = 3;

// Amount details
std::map<std::string, std::string> amount_details = {
    {"Tip", "0.00"},
    {"Cashback", "0.00"},
    {"Surcharge", "0.00"},
    {"Fee", "0.00"}
};

// Features
std::map<std::string, std::string> features = {
    {"Send Signature", "false"},
    {"Currency Code", "CAD"},
    {"Split Payment", "false"},
    {"Split Amount", "0.00"}
};

// Credentials
std::map<std::string, std::string> credentials = {
    {"TID", ""},
    {"Auth Key", ""}
};

// Validate and format amount input
std::string validate_amount_input(const std::string &input) {
    try {
        float amount = std::stof(input);
        std::ostringstream stream;
        stream << std::fixed << std::setprecision(2) << amount;
        return stream.str();
    } catch (...) {
        return "";
    }
}

// Validate currency code (3 alphanumeric characters)
std::string validate_currency_code(const std::string &input) {
    if (input.length() == 3 && std::regex_match(input, std::regex("^[A-Za-z0-9]{3}$"))) {
        std::string uppercase_input = input;
        for (auto &c : uppercase_input) c = toupper(c);
        return uppercase_input;
    }
    return "";
}

// Function to handle mouse click events
void handle_mouse_click(int mouse_x, int mouse_y) {
    if (mouse_y >= 4 && mouse_y < 6) {
        // Mode options area
        if (mouse_x >= 12 && mouse_x <= 30) {
            selected_radio = (mouse_y - 4);
        }
    }
    else if (mouse_y >= 8 && mouse_y < 12) {
        // Error options area
        if (mouse_x >= 12 && mouse_x <= 30) {
            selected_error_radio = (mouse_y - 8);
        }
    }
    else if (mouse_y >= 14 && mouse_y < 18) {
        // Amount detail fields
        if (mouse_x >= 12 && mouse_x <= 30) {
            int index = mouse_y - 14;
            std::string input;
            echo();
            mvprintw(14 + index, 30, "          ");  // Clear previous input area
            mvgetnstr(14 + index, 30, input.data(), 10);
            std::string formatted_value = validate_amount_input(input);
            if (!formatted_value.empty()) {
                amount_details[std::vector<std::string>{"Tip", "Cashback", "Surcharge", "Fee"}[index]] = formatted_value;
            } else {
                mvprintw(19, 10, "Invalid input. Please enter a valid number.");
            }
            noecho();
        }
    }
}

// Main function for the ncurses interface
void main_menu() {
    initscr();
    start_color();
    curs_set(0);  // Hide cursor
    keypad(stdscr, TRUE);
    noecho();
    mousemask(ALL_MOUSE_EVENTS | REPORT_MOUSE_POSITION, NULL);  // Enable mouse events
    init_pair(1, COLOR_YELLOW, COLOR_BLACK);
    init_pair(2, COLOR_CYAN, COLOR_BLACK);
    init_pair(3, COLOR_GREEN, COLOR_BLACK);

    int current_field = 0;
    std::vector<std::string> amount_fields = {"Tip", "Cashback", "Surcharge", "Fee"};

    while (true) {
        clear();
        mvprintw(1, 10, "NUVEI Terminal Simulator. Press 'q' to quit.");

        // Display mode options
        mvprintw(3, 10, "Mode:");
        for (size_t i = 0; i < mode_options.size(); ++i) {
            if (i == selected_radio) attron(COLOR_PAIR(1));
            mvprintw(4 + i, 12, "[%c] %s", (i == selected_radio) ? 'X' : ' ', mode_options[i].c_str());
            if (i == selected_radio) attroff(COLOR_PAIR(1));
        }

        // Display error options
        mvprintw(7, 10, "Errors/Declines:");
        for (size_t i = 0; i < error_options.size(); ++i) {
            if (i == selected_error_radio) attron(COLOR_PAIR(1));
            mvprintw(8 + i, 12, "[%c] %s", (i == selected_error_radio) ? 'X' : ' ', error_options[i].c_str());
            if (i == selected_error_radio) attroff(COLOR_PAIR(1));
        }

        // Display amount details
        mvprintw(13, 10, "Amount Detail:");
        for (size_t i = 0; i < amount_fields.size(); ++i) {
            if (i == current_field) attron(COLOR_PAIR(1));
            mvprintw(14 + i, 12, "%s: %s", amount_fields[i].c_str(), amount_details[amount_fields[i]].c_str());
            if (i == current_field) attroff(COLOR_PAIR(1));
        }

        refresh();

        int ch = getch();
        if (ch == 'q') break;
        if (ch == KEY_MOUSE) {  // Handle mouse event
            MEVENT event;
            if (getmouse(&event) == OK) {
                handle_mouse_click(event.x, event.y);
            }
        }
    }
    endwin();
}

int main() {
    main_menu();
    return 0;
}
