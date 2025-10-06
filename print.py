import argparse
import os
import asyncio
import json
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax

# Async function to read FIFO and display content
async def read_fifo(fifo_path, console):
    # Open FIFO file in non-blocking mode using os.open
    fifo_fd = os.open(fifo_path, os.O_RDONLY | os.O_NONBLOCK)

    while True:
        try:
            # Read from the FIFO file descriptor
            data = os.read(fifo_fd, 4096*2).decode().strip()  # Adjust size as necessary
            if data:
                try:
                    # Create a panel to display the formatted content
                    content = data.replace('|', '\n') if data else "[bold yellow]No data available, waiting...[/bold yellow]"

                    panel = Panel.fit(
                        content,
                        title="Receipt",
                        title_align="center",
                        border_style="cyan",
                    )

                    # Clear screen and display content
                    console.clear()
                    console.print(panel)

                except json.JSONDecodeError as e:
                    console.print(f"[bold red]Error parsing JSON: {e}[/bold red]")
            
        except BlockingIOError:
            # If no data is available, just continue and check again later
            pass

        # Refresh the screen every 0.5 seconds
        await asyncio.sleep(0.5)

    # Close the FIFO file descriptor when done
    os.close(fifo_fd)

# write fifo


async def write_receipt_fifo(fifo_path,data):
    
    # Check if the FIFO exists, create it if it doesn't
    if not os.path.exists(fifo_path):
        os.mkfifo(fifo_path)

    # Open the FIFO in write mode synchronously
    with open(fifo_path, 'w') as fifo:
        fifo.write(data + '\n')
    
    # close the file
    fifo.close()
        

# Main function to run the async loop
async def main(fifo_path):
    console = Console()
    console.clear()
    
    # Check if FIFO exists, and create if it doesn't
    if not os.path.exists(fifo_path):
        os.mkfifo(fifo_path)

    # Start reading and displaying data from the FIFO
    await read_fifo(fifo_path, console)

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Display data from a FIFO using Rich.")
        parser.add_argument("fifo_path", help="Path to the FIFO file.")
        args = parser.parse_args()

        # Ensure the FIFO exists; create it if it doesn't
        if not os.path.exists(args.fifo_path):
            os.mkfifo(args.fifo_path)

        Console().clear()  # Clear the console before starting

        # Run the main asyncio function
        asyncio.run(main(args.fifo_path))
    except KeyboardInterrupt:
        print("\n[bold red]Program interrupted![/bold red]")
