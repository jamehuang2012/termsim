#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <sys/stat.h>

#define BUFFER_SIZE 1024
#define REFRESH_RATE 100000  // 100 ms in microseconds

void read_fifo(const char *fifo_path) {
    char buffer[BUFFER_SIZE];

    while (1) {
        // Open FIFO in read-only mode
        int fifo_fd = open(fifo_path, O_RDONLY);
        if (fifo_fd == -1) {
            printf("\033[33mError opening FIFO: %s\033[0m\n", strerror(errno)); // Yellow color
            fflush(stdout);
            usleep(REFRESH_RATE);
            continue;
        }

        // Read data from FIFO
        ssize_t bytes_read = read(fifo_fd, buffer, BUFFER_SIZE - 1);
        if (bytes_read > 0) {
            buffer[bytes_read] = '\0';  // Null-terminate the string

            // Replace '|' with '\n'
            for (int i = 0; i < bytes_read; i++) {
                if (buffer[i] == '|') buffer[i] = '\n';
            }

            // Clear screen (ANSI escape code)
            printf("\033[2J\033[H");

            // Display each line of formatted data
            printf("\033[33m%s\033[0m", buffer); // Yellow color
            fflush(stdout);
        } else {
            printf("\033[33mNo data available, waiting...\033[0m\n");
            fflush(stdout);
        }

        close(fifo_fd);  // Close FIFO
        usleep(REFRESH_RATE);  // Wait before the next read
    }
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <fifo_path>\n", argv[0]);
        return EXIT_FAILURE;
    }

    const char *fifo_path = argv[1];

    // Create FIFO if it doesn't exist
    if (access(fifo_path, F_OK) == -1) {
        if (mkfifo(fifo_path, 0666) == -1) {
            perror("Error creating FIFO");
            return EXIT_FAILURE;
        }
    }

    // Start reading the FIFO
    read_fifo(fifo_path);

    return EXIT_SUCCESS;
}
