import posix_ipc
import asyncio
import json
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
import LoggerManager


async def read_message_queue(queue_name, console):
    try:
        # Ensure the old queue is removed before creating a new one
        posix_ipc.unlink_message_queue(queue_name)
    except posix_ipc.ExistentialError:
        pass  # Queue didn't exist

    # Open or create the named message queue with explicit permissions,max 20 messages, each up to 1024 bytes
    mq = posix_ipc.MessageQueue(queue_name, posix_ipc.O_CREAT | posix_ipc.O_NONBLOCK, mode=0o666)

    while True:
        try:
            message, _ = mq.receive()
            data = message.decode().strip()

            if data:
                #log = LoggerManager.LoggerManager().logger
                #log.debug("Raw data: " + data)
                
               

                parsed_data = json.loads(data)
                
                # Display title and data content
                title = parsed_data.get("title", "No Title")
                data_content = parsed_data.get("Data", {})

                parsed_data = json.loads(data_content)

                title_text = Text(title, style="bold yellow")
                json_syntax = Syntax(
                    json.dumps(parsed_data, indent=2),
                    "json",
                    theme="rrt",
                    line_numbers=False,
                    word_wrap=True
                )
                panel = Panel.fit(json_syntax, title=title_text, title_align="center", border_style="cyan", padding=(1, 2))
                console.clear()
                console.print(panel)

        except posix_ipc.BusyError:
            await asyncio.sleep(0.2)

async def main():
    console = Console()
    console.clear()
    queue_name = "/log_queue"
    await read_message_queue(queue_name, console)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[bold red]Program interrupted![/bold red]")
