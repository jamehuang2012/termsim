#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mqueue.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <ncurses.h>
#include <jansson.h>

#define MQ_NAME "/log_queue"
#define MAX_MSG_SIZE 1024 * 8
#define MAX_MSG_COUNT 20

// Function to display JSON in ncurses
void display_json(const char *json_str) {
    json_error_t error;
    json_t *root = json_loads(json_str, 0, &error);  // Parse the JSON string

    if (!root) {
        fprintf(stderr, "Error parsing JSON: %s\n", error.text);
        return;
    }

    // Initialize ncurses
    initscr();
    start_color();
    init_pair(1, COLOR_YELLOW, COLOR_BLACK);
    init_pair(2, COLOR_CYAN, COLOR_BLACK);
    cbreak();
    noecho();

    // Title formatting
    attron(COLOR_PAIR(1));
    printw("Title: %s\n", json_string_value(json_object_get(root, "title")));
    attroff(COLOR_PAIR(1));

    // JSON data formatting
    attron(COLOR_PAIR(2));
    printw("Data:\n");

    // Get the JSON object "Data" from the root object
    json_t *data = json_object_get(root, "Data");
    if (!json_is_object(data)) {
        fprintf(stderr, "Error: Data is not an object\n");
        return;
    }

    // Pretty print JSON data using jansson
    char *pretty_json = json_dumps(data, JSON_INDENT(2));
    printw("%s\n", pretty_json);
    free(pretty_json);

    attroff(COLOR_PAIR(2));

    refresh();
    getch();  // Wait for user input to exit
    endwin();  // End ncurses window

    // Free the JSON root object
    json_decref(root);
}

void read_message_queue(const char *queue_name) {
    mqd_t mq;
    char buffer[MAX_MSG_SIZE];
    ssize_t bytes_read;

    // Open or create the message queue
    mq = mq_open(queue_name, O_CREAT | O_NONBLOCK, 0666, NULL);
    if (mq == -1) {
        perror("mq_open");
        exit(1);
    }

    while (1) {
        // Receive messages from the queue
        bytes_read = mq_receive(mq, buffer, MAX_MSG_SIZE, NULL);
        if (bytes_read >= 0) {
            buffer[bytes_read] = '\0';  // Null-terminate the message
            printf("Raw data: %s\n", buffer);

            // Display JSON content
            display_json(buffer);
        } else {
            if (errno == EAGAIN) {
                // No message available, wait for a moment and retry
                printf("No messages available. Retrying...\n");
                sleep(1);  // Sleep before retrying
            } else {
                // If there's an error other than "no messages", print it
                perror("mq_receive");
                sleep(1);  // Retry after 1 second if there's an error
            }
        }
    }

    // Close and unlink the message queue
    mq_close(mq);
    mq_unlink(queue_name);
}

int main() {
    // Read from the message queue
    read_message_queue(MQ_NAME);

    return 0;
}
