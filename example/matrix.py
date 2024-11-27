import curses
import random
import time

def main(stdscr):
    # Initialize the screen
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(True)  # Non-blocking input
    stdscr.timeout(100)  # Refresh rate in milliseconds

    # Define colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Get screen dimensions
    height, width = stdscr.getmaxyx()

    # Create a list to store the positions of each column
    columns = [random.randint(0, height - 1) for _ in range(width)]

    # Main loop
    while True:
        stdscr.clear()

        # Show "Nuvei Terminal Simulator" at the top with color green   
        title = "Nuvei Terminal Simulator"
        stdscr.addstr(0, (width - len(title)) // 2, title, curses.color_pair(1))


        # Show Version # "1.0.0" at the top
        version = "Version 1.0.0"

        # Show the version with red color
        stdscr.addstr(1, (width - len(version)) // 2, version)

        # Refresh the screen
        stdscr.refresh()

        # Delay 0.5 seconds
        time.sleep(1)


        # Handle exit on key press
        # Only Ctrl+C exits the program
        key = stdscr.getch()
        if key == 3:
            break


      


# Run the program
curses.wrapper(main)
