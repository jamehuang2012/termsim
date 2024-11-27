import json
import time
from rich.console import Console
from rich.syntax import Syntax
import random

# Initialize rich console
console = Console()

def generate_json_data():
    """Simulates dynamic JSON data changes."""
    return {
        "name": f"User{random.randint(1, 10)}",
        "age": random.randint(20, 40),
        "email": f"user{random.randint(1, 10)}@example.com",
        "is_active": random.choice([True, False]),
        "roles": random.choices(["user", "admin", "guest"], k=2),
        "details": {
            "city": random.choice(["New York", "Los Angeles", "Chicago"]),
            "country": "USA"
        }
    }

# Simulate `tail -f` by continuously printing new data every few seconds
try:
    while True:
        # Generate random JSON data
        data = generate_json_data()
        
        # Convert to JSON string with pretty formatting
        json_str = json.dumps(data, indent=2)
        
        # Print the "Network -> Cloud" with yellow color
        console.print("[bold yellow]Network -> Cloud[/bold yellow]")

        # Pretty-print the formatted JSON with syntax highlighting
        syntax = Syntax(json_str, "json", theme="paraiso-dark", line_numbers=False)
        console.print(syntax)
        
        # Wait for a short period before updating
        time.sleep(2)  # Update every 2 seconds
except KeyboardInterrupt:
    console.print("\nStopped.")
