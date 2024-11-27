import curses

def main(stdscr):
    # Initialize curses settings
    curses.curs_set(0)  # Hide the cursor
    curses.mousemask(curses.ALL_MOUSE_EVENTS)  # Enable all mouse events
    
    stdscr.clear()
    
    # Form fields with default values
    fields = [
        {"label": "Mode:", "options": ["Retail", "Pay at Table"], "value": 0},
        {"label": "Interval (Integer):", "value": "2000"},
        {"label": "TID:", "value": "12345678"},
        {"label": "Auth Key:", "value": "8623579e-ac0f-43dd-a775-fd0a9c300dd2"},
        {"label": "Tip:", "value": "0.00"},
        {"label": "Cashback:", "value": "0.00"},
        {"label": "Surcharge:", "value": "0.00"},
        {"label": "Fee:", "value": "0.00"},
    ]
    
    # Checkbox fields
    checkboxes = [
        {"label": "Send Signature", "value": False},
        {"label": "Split Payment", "value": False},
        {"label": "Enable Declines", "value": False},
        {"label": "Enable Cancellations", "value": False},
        {"label": "Stop Response", "value": False},
    ]
    
    current_field = 0  # Track selected field
    current_checkbox = 0  # Track selected checkbox
    
    while True:
        stdscr.clear()
        
        # Draw fields
        for idx, field in enumerate(fields):
            label = field['label']
            value = field['options'][field['value']] if 'options' in field else field['value']
            stdscr.addstr(idx + 1, 2, f"{label} {value}")
        
        # Draw checkboxes
        for idx, box in enumerate(checkboxes):
            label = box['label']
            status = "[X]" if box['value'] else "[ ]"
            stdscr.addstr(len(fields) + idx + 3, 2, f"{status} {label}")
        
        stdscr.refresh()
        
        # Handle keyboard input
        key = stdscr.getch()

        if key == curses.KEY_DOWN:
            # Move down through fields or checkboxes
            if current_field < len(fields) - 1:
                current_field += 1
            elif current_field == len(fields) - 1:
                current_field = len(fields)  # Jump to checkboxes
            else:
                current_field = 0  # Go back to the first field
        
        elif key == curses.KEY_UP:
            # Move up through fields or checkboxes
            if current_field > 0:
                current_field -= 1
            elif current_field == len(fields):
                current_field = len(fields) - 1  # Go back to the last field
            else:
                current_field = len(fields) - 1  # Go to the last field

        elif key == ord('q'):
            # Exit the program when 'q' is pressed
            break
        
        elif key == 10:  # Enter key
            # Toggle a checkbox if in the checkbox list
            if current_field >= len(fields):
                checkbox_index = current_field - len(fields)
                checkboxes[checkbox_index]["value"] = not checkboxes[checkbox_index]["value"]

        # Handle mouse events
        event = stdscr.getch()
        if event == curses.KEY_MOUSE:
            _, x, y, _, button = curses.getmouse()
            # Check if a mouse click occurred
            if button == 1:  # Left click
                if y < len(fields) + 3:  # If clicked within the field area
                    # Determine which field was clicked and update its value or focus
                    clicked_field = y - 1
                    if clicked_field < len(fields):
                        current_field = clicked_field
                elif y >= len(fields) + 3:  # If clicked in checkbox area
                    clicked_checkbox = y - len(fields) - 3
                    if clicked_checkbox < len(checkboxes):
                        checkboxes[clicked_checkbox]["value"] = not checkboxes[clicked_checkbox]["value"]

        # Refresh screen after processing input
        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)
