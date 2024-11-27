from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import re, json

console = Console()
SETTINGS_FILE = 'settings_combined.json'

# Options
mode_options = ['Retail', 'Pay at Table']
error_options = ['Enable Declines', 'Enable Cancellations', 'Stop Response', 'None']

# Default settings
selected_radio, selected_error_radio = 0, 3
amount_details = {"Tip": "0.00", "Cashback": "0.00", "Surcharge": "0.00", "Fee": "0.00"}
features = {"Send Signature": False, "Currency Code": "CAD", "Split Payment": False, "Split Amount": "0.00"}
credentials = {"TID": "", "Auth_Key": ""}

def validate_amount_input(input_str):
    try: return "{:.2f}".format(float(input_str))
    except ValueError: return None

def validate_currency_code(input_str):
    return input_str.upper() if re.fullmatch(r"[a-zA-Z0-9]{3}", input_str) else None

def display_table():
    console.clear()
    def print_options(title, options, selected):  # Unified display function
        console.print(f"\n[bold cyan]{title}:[/bold cyan]")
        for idx, option in enumerate(options):
            console.print(f"[{'X' if idx == selected else ' '}] {option}")

    print_options("Mode Options", mode_options, selected_radio)
    print_options("Error Options", error_options, selected_error_radio)

    for title, data, colors in [("Amount Details", amount_details, ("magenta", "green")),
                                ("Features", features, ("yellow", "blue")),
                                ("Credentials", credentials, ("red", "white"))]:
        table = Table(title=title)
        for col, color in zip(["Field", "Value"], colors): table.add_column(col, style=color)
        for field, value in data.items(): table.add_row(field, "[X]" if value is True else str(value))
        console.print(table)

def main():
    global selected_radio, selected_error_radio
    while True:
        display_table()
        options = ["Select Mode", "Select Error Option", "Update Amount Details", "Toggle Features", "Update Credentials", "Exit and Save"]
        console.print("\n" + "\n".join([f"{i + 1}. {opt}" for i, opt in enumerate(options)]) + "\n")

        choice = Prompt.ask("Enter your choice", choices=[str(i + 1) for i in range(6)])
        if choice == "1": selected_radio = int(Prompt.ask("Select Mode (0 for Retail, 1 for Pay at Table)"))
        elif choice == "2": selected_error_radio = int(Prompt.ask("Select Error Option (0-3)"))
        elif choice == "3":
            field = Prompt.ask("Enter the field to update (Tip, Cashback, Surcharge, Fee)")
            if field in amount_details:
                if (new_value := validate_amount_input(Prompt.ask(f"Enter new value for {field}"))):
                    amount_details[field] = new_value
                else: console.print("[bold red]Invalid amount![/bold red]")
        elif choice == "4":
            feature = Prompt.ask("Enter feature to toggle (Send Signature, Split Payment, Currency Code, Split Amount)")
            if feature in features:
                if feature in ["Send Signature", "Split Payment"]:
                    features[feature] = not features[feature]
                elif feature == "Currency Code":
                    if (valid_value := validate_currency_code(Prompt.ask("Enter 3-letter currency code"))):
                        features[feature] = valid_value
                    else: console.print("[bold red]Invalid Currency Code![/bold red]")
                else:
                    if (formatted_value := validate_amount_input(Prompt.ask("Enter split amount"))):
                        features[feature] = formatted_value
                    else: console.print("[bold red]Invalid amount![/bold red]")
        elif choice == "5":
            cred = Prompt.ask("Enter credential to update (TID, Auth_Key)")
            if cred in credentials: credentials[cred] = Prompt.ask(f"Enter new value for {cred}")
        elif choice == "6":
            with open(SETTINGS_FILE, 'w') as f:
                json.dump({"mode": mode_options[selected_radio], "error": error_options[selected_error_radio],
                           "amount_details": amount_details, "features": features, "credentials": credentials}, f, indent=4)
            console.print("[bold green]Settings saved! Exiting...[/bold green]")
            break

if __name__ == '__main__':
    main()
