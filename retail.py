import curses
import json
import os
import re
import ParameterSingleton
from StringUtily import TerminalStatus, TransactionStatus
from TransactionData import TransactionData
import sslclient as client
import threading
import time
import LoggerManager



# Options
mode_options = ['Start heartbeat', 'Stop heartbeat']
error_options = ['Enable Declines', 'Enable Cancellations', 'Stop Response','None']

#add terinal status options
terminal_status = ['IDLE','BUSY']

# Initialize selections
selected_radio = 0  # Default selected radio option
selected_error_radio = 3  # Default selected error option
selected_terminal_status = 0 # Default selected terminal status

button_selected = False  # Tracks if the start button is selected



# Amount details default values
amount_details = {
    "Tip": "0.00",
    "Cashback": "0.00",
    "Surcharge": "0.00",
    "Fee": "0.00"
}

# Default values
features = {
    "Send Signature": False,
    "Currency Code": "CAD",
    "Split Payment": False,
    "Split Amount": "0.00",
}


credentials = {
    "TID": "",
    "Auth Key": ""
}


# Function to validate and format amount input
def validate_amount_input(input_str):
    try:
        # Convert input to float and format to 2 decimal places
        formatted_amount = "{:.2f}".format(float(input_str))
        return formatted_amount
    except ValueError:
        return None  # Return None if the input is invalid

# Function to validate the Currency Code (alphanumeric, 3 characters)
def validate_currency_code(input_str):
    if len(input_str) == 3 and re.match("^[a-zA-Z0-9]{3}$", input_str):
        return input_str.upper()  # Convert to uppercase to ensure consistency
    return None  # Invalid input    


stop_event = None
def doThread(stop_event):
    while not stop_event.is_set():
        log = LoggerManager.LoggerManager().logger
        log.debug("Thread Running")        
        client.doTransaction()
        time.sleep(5)


# Main function to handle curses
def main(stdscr):
    global selected_radio, selected_error_radio, button_selected
    global selected_terminal_status

    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Selected item
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Normal item
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Instruction text
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Start button color

    curses.curs_set(0)  # Hide cursor
    stdscr.keypad(True)  # Enable special keys
    curses.mousemask(curses.ALL_MOUSE_EVENTS)  # Enable all mouse events

    # Fields and navigation setup
    fields = list(amount_details.keys())
    current_field = 0  # Start from the first field

   
    current_features = 0
    current_credential = 0


    # Fields of the settings
    features_fields = list(features.keys())

    # Load credentials from the JSON file
    #credentials = load_credentials_from_json()

    params = ParameterSingleton.ParameterSingleton()

    credentials["TID"] = params.get_tid()
    credentials["Auth Key"] = params.get_auth_key()

    # Fields of the credentials
    credentials_fields = list(credentials.keys())

    log = LoggerManager.LoggerManager().logger
    log.debug("Start Thread")


    stop_event = threading.Event()

    # Start the thread , infinite loop
    thread = threading.Thread(target=doThread, args=(stop_event,))
    
    thread.start()


    # Set defualt terminal status
    TransactionData().terminalStatus = TerminalStatus.IDLE.name
    # Set  Tip amount
    # TransactionData().tid = ParameterSingleton.ParameterSingleton().get_tid()
    # TransactionData().authKey = ParameterSingleton.ParameterSingleton().get_auth_key()
    TransactionData().tipAmount = amount_details["Tip"]
    TransactionData().cashback = amount_details["Cashback"]
    TransactionData().surchargeFee = amount_details["Surcharge"]
    TransactionData().serviceFee = amount_details["Fee"]
    TransactionData().enableSignature = features["Send Signature"]
    TransactionData().currencyCode = features["Currency Code"]
    TransactionData().splitPayment = features["Split Payment"]
    TransactionData().splitAmount = features["Split Amount"]
    TransactionData().isRunning = True
    TransactionData().status = TransactionStatus.NoneStatus

  

    while True:
        stdscr.clear()

        # Instruction line
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(1, 10, "NUVEI Terminal Simulator. Press 'q' to quit.")
        stdscr.attroff(curses.color_pair(3))

        # Display radio options
        stdscr.addstr(3, 10, "Mode:")
        for idx, option in enumerate(mode_options):
            if idx == selected_radio:
                stdscr.attron(curses.color_pair(1))  # Highlight selected radio
                marker = "(X)"
            else:
                stdscr.attron(curses.color_pair(2))  # Normal color
                marker = "( )"
            stdscr.addstr(4 + idx, 12, f"{marker} {option}")
            stdscr.attroff(curses.color_pair(1 if idx == selected_radio else 2))
        
        # Set isRunning of TransactionData

        if selected_radio == 0:
            TransactionData().isRunning = True
        else:
            TransactionData().isRunning = False
        

        # Display error radio options
        stdscr.addstr(7, 10, "Errors/Declines:")
        for idx, option in enumerate(error_options):
            if idx == selected_error_radio:
                stdscr.attron(curses.color_pair(1))
                marker = "(X)"
            else:
                stdscr.attron(curses.color_pair(2))
                marker = "( )"
            stdscr.addstr(8 + idx, 12, f"{marker} {option}")
            stdscr.attroff(curses.color_pair(1 if idx == selected_error_radio else 2))

        # Set status of TransactionData 

        if selected_error_radio == 0:
            TransactionData().status = TransactionStatus.Decline
        elif selected_error_radio == 1:
            TransactionData().status = TransactionStatus.Cancellation
        elif selected_error_radio == 2:
            TransactionData().status = TransactionStatus.NoResponse
        elif selected_error_radio == 3:
            TransactionData().status = TransactionStatus.NoneStatus
        
        

        # Display input fields
        stdscr.addstr(13, 10, "Amount Detail:")
        for idx, field in enumerate(fields):
            if idx == current_field:
                stdscr.attron(curses.color_pair(1))  # Highlight current field
                stdscr.addstr(14 + idx, 12, f"{field}: {amount_details[field]}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.attron(curses.color_pair(2))  # Normal color
                stdscr.addstr(14 + idx, 12, f"{field}: {amount_details[field]}")
                stdscr.attroff(curses.color_pair(2))

        # Display input fields
        stdscr.addstr(19, 10, "Features:")
        for idx, field in enumerate(features_fields):
            if idx == current_features:
                stdscr.attron(curses.color_pair(1))  # Highlight current field
            else:
                stdscr.attron(curses.color_pair(2))  # Normal color
            
            # Checkbox fields
            if field in ["Send Signature", "Split Payment"]:
                checkbox = "[X]" if features[field] else "[ ]"
                stdscr.addstr(20 + idx, 12, f"{checkbox} {field} ")
            
            # Input fields
            elif field == "Currency Code":
                stdscr.addstr(20 + idx, 12, f"{field}: {features[field]}")
            
            elif field == "Split Amount":
                stdscr.addstr(20 + idx, 12, f"{field}: {features[field]}")

            stdscr.attroff(curses.color_pair(1))
            stdscr.attroff(curses.color_pair(2))
        
        # Display Credentials
        stdscr.addstr(25, 10, "Credentials:")
        for idx, field in enumerate(credentials_fields):

            if idx == current_credential:
                stdscr.attron(curses.color_pair(1))
            else:
                stdscr.attron(curses.color_pair(2))

            stdscr.addstr(26 + idx, 12, f"{field}: {credentials[field]}")
        
        # Display terminal status
        stdscr.addstr(29, 10, "Terminal Status:")
        for idx, option in enumerate(terminal_status):
            if idx == selected_terminal_status:
                stdscr.attron(curses.color_pair(1))  # Highlight selected radio
                marker = "(X)"
                # Update the terminal status
                
            else:
                stdscr.attron(curses.color_pair(2))  # Normal color
                marker = "( )"
            stdscr.addstr(30 + idx, 12, f"{marker} {option}")
            stdscr.attroff(curses.color_pair(1 if idx == selected_terminal_status else 2))

            # Update the terminal status
            if selected_terminal_status == 0:
                TransactionData().terminalStatus = TerminalStatus.IDLE.name
            else:
                TransactionData().terminalStatus = TerminalStatus.BUSY.name


        stdscr.refresh()

        # Handle input events
        key = stdscr.getch()
        if key == ord('q'):  # Quit program
            stop_event.set()
            break

        elif key == curses.KEY_MOUSE:
            _, x, y, _, _ = curses.getmouse()
            # Determine which option was clicked
            if 4 <= y < 4 + len(mode_options):
                selected_radio = y - 4
            elif 8 <= y < 8 + len(error_options):
                selected_error_radio = y - 8
            elif 14 <= y < 14 + len(fields):
                current_field = y - 14
            elif 20 <= y < 20 + len(features_fields):
                current_features = y - 20    
            elif 26 <= y < 26 + len(credentials):
                current_credential = y - 26
            elif 30 <= y < 30 + len(terminal_status):
                selected_terminal_status = y - 30

            transaction = TransactionData()
            log.debug(transaction.__str__())

        elif key == 10:  # Enter key
            curses.echo()  # Enable echoing of input

            if y < 20:
                stdscr.addstr(14 + current_field, 30, " " * 10)  # Clear previous input
                stdscr.move(14 + current_field, 30)  # Move cursor to input area
                new_value = stdscr.getstr(14 + current_field, 30, 10).decode('utf-8')
                
                formatted_value = validate_amount_input(new_value)
                if formatted_value is not None:
                    amount_details[fields[current_field]] = formatted_value

                    if fields[current_field] == "Tip":
                        TransactionData().tipAmount = formatted_value
                    elif fields[current_field] == "Cashback":
                        TransactionData().cashbackAmount = formatted_value
                    elif fields[current_field] == "Surcharge":
                        TransactionData().surchargeAmount = formatted_value
                    elif fields[current_field] == "Fee":
                        TransactionData().feeAmount = formatted_value
                else:
                    # Display error message for invalid input
                    stdscr.attron(curses.color_pair(3))
                    stdscr.addstr(24 + len(fields), 10, "Invalid amount. Please enter a valid number with 2 decimals.")
                    stdscr.attroff(curses.color_pair(3))
                    stdscr.getch()  # Wait for user to press a key  
                    curses.noecho()  # Disable echoing of input    
            elif 20 <= y < 26:

                if features_fields[current_features] in ["Send Signature", "Split Payment"]:
                    # Toggle checkbox for Send Signature or Split Payment
                    features[features_fields[current_features]] = not features[features_fields[current_features]]

                    if features_fields[current_features] == "Send Signature":
                        TransactionData().enableSignature = features[features_fields[current_features]]
                    elif features_fields[current_features] == "Split Payment":
                        TransactionData().splitPayment = features[features_fields[current_features]]

                elif features_fields[current_features] == "Currency Code":
                    curses.echo()  # Enable echoing of input
                    stdscr.addstr(20 + current_features, 30, " " * 10)  # Clear previous input
                    stdscr.move(20 + current_features, 30)  # Move cursor to input area
                    new_value = stdscr.getstr(20 + current_features, 30, 3).decode('utf-8')  # Limit input to 3 characters
                    valid_value = validate_currency_code(new_value)
                    if valid_value:
                        features[features_fields[current_features]] = valid_value
                        TransactionData().currencyCode = valid_value
                    else:
                        # Display error message for invalid input
                        stdscr.attron(curses.color_pair(3))
                        stdscr.addstr(24 + len(features_fields), 10, "Invalid Currency Code. Please enter exactly 3 alphanumeric characters.")
                        stdscr.attroff(curses.color_pair(3))
                        stdscr.getch()  # Wait for user to press a key
                    curses.noecho()  # Disable echoing of input
                elif features_fields[current_features] == "Split Amount":
                    curses.echo()  # Enable echoing of input
                    stdscr.addstr(20 + current_features, 30, " " * 10)  # Clear previous input
                    stdscr.move(20 + current_features, 30)  # Move cursor to input area
                    new_value = stdscr.getstr(20 + current_features, 32, 10).decode('utf-8')
                    formatted_value = validate_amount_input(new_value)
                    if formatted_value is not None:
                        features[features_fields[current_features]] = formatted_value
                        TransactionData().splitAmount = formatted_value
                    else:
                        # Display error message for invalid input
                        stdscr.attron(curses.color_pair(3))
                        stdscr.addstr(24 + len(features_fields), 10, "Invalid amount. Please enter a valid number with 2 decimals.")
                        stdscr.attroff(curses.color_pair(3))
                        stdscr.getch()  # Wait for user to press a key
                curses.noecho()  # Disable echoing of input    
            elif 26 <= y < 26 + len(credentials):
                if credentials_fields[current_credential] == "TID":
                    curses.echo()
                    stdscr.addstr(18 + current_credential, 30, " " * 12)
                else:
                    curses.echo()
                    stdscr.addstr(26 + current_credential, 22, " " * 36)
                stdscr.move(26 + current_credential, 30)
                new_value = stdscr.getstr(26 + current_credential, 30, 36).decode('utf-8')
                credentials[credentials_fields[current_credential]] = new_value

                # Save after modifying credentials

                if credentials_fields[current_credential] == "TID":
                    params.set_tid(new_value)
                elif credentials_fields[current_credential] == "Auth Key":
                    params.set_auth_key(new_value)
                
                curses.noecho()

        
          


# Run the curses application
if __name__ == '__main__':
    curses.wrapper(main)
