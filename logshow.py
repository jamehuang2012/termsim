import os
import asyncio
import json
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax

import LoggerManager

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

                    log = LoggerManager.LoggerManager().logger
                    log.debug("Success:" + data)
                    # Parse the JSON data
                    parsed_data = json.loads(data)

                    # Extract the title and data content
                    title = parsed_data.get("title", "No Title")
                    data_content = parsed_data.get("Data", {})

                    # Display title in yellow
                    title_text = Text(title, style="bold yellow")

                    # Use rich's Syntax to pretty-print the data content (monokai theme)
                    json_syntax = Syntax(
                        json.dumps(data_content, indent=2),
                        "json",
                        theme="paraiso-dark",
                        line_numbers=False,
                        word_wrap=True
                    )

                    # Create a panel to display the formatted content
                    panel = Panel.fit(
                        json_syntax,
                        title=title_text,
                        title_align="center",
                        border_style="cyan",
                        padding=(1, 2)
                    )

                    # Clear screen and display content
                    console.clear()
                    console.print(panel)

                except json.JSONDecodeError as e:
                    log = LoggerManager.LoggerManager().logger
                    log.debug("Fail:" + data)

                    console.print(f"[bold red]Error parsing JSON: {e}[/bold red]")
            
        except BlockingIOError:
            # If no data is available, just continue and check again later
            pass

        # Refresh the screen every 0.5 seconds
        await asyncio.sleep(0.5)

    # Close the FIFO file descriptor when done
    os.close(fifo_fd)

# Main function to run the async loop
async def main():
    console = Console()
    console.clear()
    
    fifo_path = "/tmp/log_fifo"  # Change this to your actual FIFO path
    
    # Check if FIFO exists, and create if it doesn't
    if not os.path.exists(fifo_path):
        os.mkfifo(fifo_path)

    # Start reading and displaying data from the FIFO
    await read_fifo(fifo_path, console)

if __name__ == "__main__":
    try:
        # Run the main asyncio function
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[bold red]Program interrupted![/bold red]")
