import curses
import re

# Default values
settings = {
    "Send Signature": False,
    "Currency Code": "",
    "Split Payment": False,
    "Split Amount": "0.00",
}

# Function to validate the split amount (ensure two decimals)
def validate_amount_input(input_str):
    try:
        formatted_amount = "{:.2f}".format(float(input_str))
        return formatted_amount
    except ValueError:
        return None  # Invalid input

# Function to validate the Currency Code (alphanumeric, 3 characters)
def validate_currency_code(input_str):
    if len(input_str) == 3 and re.match("^[a-zA-Z0-9]{3}$", input_str):
        return input_str.upper()  # Convert to uppercase to ensure consistency
    return None  # Invalid input

# Main function to handle curses
def main(stdscr):
    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Highlighted item
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Normal item
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)     # Error message color
    curses.curs_set(1)  # Show cursor
    stdscr.keypad(True)  # Enable special keys
    curses.mousemask(curses.ALL_MOUSE_EVENTS)  # Enable mouse events

    # Fields and navigation setup
    fields = list(settings.keys())
    current_field = 0  # Start from the first field

    while True:
        stdscr.clear()
        stdscr.addstr(1, 10, "NUVEI Terminal Simulator - Payment Settings", curses.color_pair(1))
        stdscr.addstr(2, 10, "Press 'q' to quit. Use arrow keys or mouse to navigate. Enter to edit.", curses.color_pair(2))

        # Display input fields
        for idx, field in enumerate(fields):
            if idx == current_field:
                stdscr.attron(curses.color_pair(1))  # Highlight current field
            else:
                stdscr.attron(curses.color_pair(2))  # Normal color
            
            # Checkbox fields
            if field in ["Send Signature", "Split Payment"]:
                checkbox = "[X]" if settings[field] else "[ ]"
                stdscr.addstr(4 + idx, 12, f"{checkbox} {field} ")
            
            # Input fields
            elif field == "Currency Code":
                stdscr.addstr(4 + idx, 12, f"{field}: {settings[field]}")
            
            elif field == "Split Amount":
                stdscr.addstr(4 + idx, 12, f"{field}: {settings[field]}")

            stdscr.attroff(curses.color_pair(1))
            stdscr.attroff(curses.color_pair(2))

        stdscr.refresh()

        # Handle user input
        key = stdscr.getch()
        if key == ord('q'):  # Quit the program
            break
        elif key == curses.KEY_DOWN:
            current_field = (current_field + 1) % len(fields)
        elif key == curses.KEY_UP:
            current_field = (current_field - 1) % len(fields)
        elif key == curses.KEY_MOUSE:
            _, x, y, _, _ = curses.getmouse()
            # Determine which field was clicked
            for idx in range(len(fields)):
                if 4 + idx == y and 12 <= x <= 30:  # Check if click is on a field
                    current_field = idx
                    break
            for idx, field in enumerate(fields):
                if field in ["Send Signature", "Split Payment"]:
                    # Check if the mouse click is within the bounds of the checkbox
                    if 4 + idx == y and 12 <= x <= 30:  # Checkbox region
                        current_field = idx
                        break
                    else:
                        # Check if the mouse click is within the bounds of the input field
                        if 4 + idx == y and 12 <= x <= 40:  # Input field region
                            current_field = idx
                            break    
        elif key == 10:  # Enter key to edit the current field
            if fields[current_field] in ["Send Signature", "Split Payment"]:
                # Toggle checkbox for Send Signature or Split Payment
                settings[fields[current_field]] = not settings[fields[current_field]]
            elif fields[current_field] == "Currency Code":
                curses.echo()  # Enable echoing of input
                stdscr.addstr(4 + current_field, 30, " " * 10)  # Clear previous input
                stdscr.move(4 + current_field, 30)  # Move cursor to input area
                new_value = stdscr.getstr(4 + current_field, 30, 3).decode('utf-8')  # Limit input to 3 characters
                valid_value = validate_currency_code(new_value)
                if valid_value:
                    settings[fields[current_field]] = valid_value
                else:
                    # Display error message for invalid input
                    stdscr.attron(curses.color_pair(3))
                    stdscr.addstr(8 + len(fields), 10, "Invalid Currency Code. Please enter exactly 3 alphanumeric characters.")
                    stdscr.attroff(curses.color_pair(3))
                    stdscr.getch()  # Wait for user to press a key
                curses.noecho()  # Disable echoing of input
            elif fields[current_field] == "Split Amount":
                curses.echo()  # Enable echoing of input
                stdscr.addstr(4 + current_field, 30, " " * 10)  # Clear previous input
                stdscr.move(4 + current_field, 30)  # Move cursor to input area
                new_value = stdscr.getstr(4 + current_field, 30, 10).decode('utf-8')
                formatted_value = validate_amount_input(new_value)
                if formatted_value is not None:
                    settings[fields[current_field]] = formatted_value
                else:
                    # Display error message for invalid input
                    stdscr.attron(curses.color_pair(3))
                    stdscr.addstr(8 + len(fields), 10, "Invalid amount. Please enter a valid number with 2 decimals.")
                    stdscr.attroff(curses.color_pair(3))
                    stdscr.getch()  # Wait for user to press a key
                curses.noecho()  # Disable echoing of input

# Run the curses application
if __name__ == '__main__':
    curses.wrapper(main)
