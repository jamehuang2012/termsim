import json
import os
import time
from rich.live import Live
from rich.table import Table
from rich.console import Console

FIFO_PATH = "/tmp/status_fifo"  # Path to the FIFO file
console = Console()

# Ensure FIFO exists
if not os.path.exists(FIFO_PATH):
    os.mkfifo(FIFO_PATH)

# Function to load data from the FIFO in non-blocking mode
def load_json_data():
    try:
        # Open FIFO in non-blocking mode
        with open(FIFO_PATH, "r", os.O_NONBLOCK) as fifo:
            message = fifo.read().strip()

            # close the file
            fifo.close()

            if not message:
                return None  # No new data; return None to keep the current table
            return json.loads(message)  # Deserialize the JSON data
    except (json.JSONDecodeError, ValueError):
        return {
            "TerminalStatus": "INVALID",
            "TransactionStatus": "UNKNOWN",
            "Response": "ERROR",
            "CancelStatus": "N/A"
        }
    except Exception as e:
        return {
            "TerminalStatus": "ERROR",
            "TransactionStatus": str(e),
            "Response": "NONE",
            "CancelStatus": "N/A"
        }

# Function to create the table
def create_table(data):
    # Create a new table aligned to the center
    table = Table(title="", show_lines=False, expand=True)

    table.add_column("Field", style="cyan", justify="left")
    table.add_column("Value", style="magenta", justify="center")

    # Define rows with conditional colors
    status_colors = {
        "IDLE": "green",
        "BUSY": "yellow",
        "ERROR": "red",
        "INVALID": "red"
    }

    trans_colors = {
        "INIT": "white",
        "ACPT": "cyan",
        "RSPN": "yellow",
        "CMPT": "green"
    }

    response_colors = {
        "APPR": "green",
        "DECL": "red"
    }

    cancel_colors = {
        "N/A": "cyan",
        "PEND": "red"
    }

    # Terminal Status
    terminal_status = data.get("TerminalStatus", "N/A")
    terminal_color = status_colors.get(terminal_status, "red")
    table.add_row("Terminal Status", f"[{terminal_color}]{terminal_status}[/{terminal_color}]")

    # Transaction Status
    transaction_status = data.get("TransactionStatus", "N/A")
    transaction_color = trans_colors.get(transaction_status, "yellow")
    table.add_row("Transaction Status", f"[{transaction_color}]{transaction_status}[/{transaction_color}]")

    # Response
    response = data.get("Response", "N/A")
    response_color = response_colors.get(response, "red")
    table.add_row("Response", f"[{response_color}]{response}[/{response_color}]")

    # Cancel Status
    cancel_status = data.get("CancelStatus", "N/A")
    cancel_color = cancel_colors[cancel_status]
    table.add_row("Cancel Status", f"[{cancel_color}]{'PEND' if cancel_status == 'PEND' else 'N/A'}[/{cancel_color}]")


    return table

# Main loop using rich.live.Live
def main():
    current_data = {
        "TerminalStatus": "NO DATA",
        "TransactionStatus": "UNKNOWN",
        "Response": "NONE",
        "IsCancelled": False
    }
    Console().clear()
    with Live(console=console, auto_refresh=False, refresh_per_second=1) as live:
        while True:
            new_data = load_json_data()
            if new_data:
                current_data = new_data  # Update only if new data is available
            table = create_table(current_data)
            live.update(table, refresh=True)
            time.sleep(1)  # Refresh rate

# Run the program
if __name__ == "__main__":
    main()
