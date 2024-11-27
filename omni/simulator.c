#include <ncurses.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

// Options and data structures
#define NUM_MODES 2
#define NUM_ERRORS 4
#define NUM_AMOUNT_FIELDS 4
#define NUM_FEATURES 4
#define NUM_CREDENTIALS 2

char *mode_options[NUM_MODES] = {"Retail", "Pay at Table"};
char *error_options[NUM_ERRORS] = {"Enable Declines", "Enable Cancellations", "Stop Response", "None"};

typedef struct {
    char tip[10];
    char cashback[10];
    char surcharge[10];
    char fee[10];
} AmountDetails;

typedef struct {
    int send_signature;
    char currency_code[4];
    int split_payment;
    char split_amount[10];
} Features;

typedef struct {
    char TID[20];
    char auth_key[20];
} Credentials;

AmountDetails amount_details = {"0.00", "0.00", "0.00", "0.00"};
Features features = {0, "CAD", 0, "0.00"};
Credentials credentials = {"", ""};

// State tracking
int selected_mode = 0;
int selected_error = NUM_ERRORS - 1;
int current_field = 0;

// Function prototypes
void display_menu(WINDOW *win);
void get_input(char *field, int max_len);

int main() {
    initscr();
    noecho();
    cbreak();
    curs_set(0);
    keypad(stdscr, TRUE);

    start_color();
    init_pair(1, COLOR_YELLOW, COLOR_BLACK);
    init_pair(2, COLOR_CYAN, COLOR_BLACK);
    init_pair(3, COLOR_GREEN, COLOR_BLACK);

    int ch;
    while (1) {
        clear();
        attron(COLOR_PAIR(3));
        mvprintw(1, 10, "NUVEI Terminal Simulator. Press 'q' to quit.");
        attroff(COLOR_PAIR(3));

        // Display Modes
        mvprintw(3, 10, "Mode:");
        for (int i = 0; i < NUM_MODES; i++) {
            if (i == selected_mode) {
                attron(COLOR_PAIR(1));
                mvprintw(4 + i, 12, "(X) %s", mode_options[i]);
                attroff(COLOR_PAIR(1));
            } else {
                attron(COLOR_PAIR(2));
                mvprintw(4 + i, 12, "( ) %s", mode_options[i]);
                attroff(COLOR_PAIR(2));
            }
        }

        // Display Errors
        mvprintw(7, 10, "Errors/Declines:");
        for (int i = 0; i < NUM_ERRORS; i++) {
            if (i == selected_error) {
                attron(COLOR_PAIR(1));
                mvprintw(8 + i, 12, "(X) %s", error_options[i]);
                attroff(COLOR_PAIR(1));
            } else {
                attron(COLOR_PAIR(2));
                mvprintw(8 + i, 12, "( ) %s", error_options[i]);
                attroff(COLOR_PAIR(2));
            }
        }

        // Display input fields
        mvprintw(13, 10, "Amount Details:");
        mvprintw(14, 12, "Tip: %s", amount_details.tip);

        refresh();
        ch = getch();
        if (ch == 'q') {
            break;
        }
    }
    
    endwin();
    return 0;
}

