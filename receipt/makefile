# Compiler and flags
CC = gcc
CFLAGS = -Wall -Wextra -std=c11
LDFLAGS = -lncurses

# Target executable
TARGET = read_fifo

# Source files
SRCS = read_fifo.c

# Build target
all: $(TARGET)

# Rule to build the executable
$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) $(SRCS) -o $(TARGET) $(LDFLAGS)

# Clean up the build artifacts
clean:
	rm -f $(TARGET)

# Phony targets (not actual files)
.PHONY: all clean

