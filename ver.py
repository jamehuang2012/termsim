import asyncio
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

async def main():
    console = Console()
    version = "Version 1.0.0"
    
    async def generate_screen():
        while True:
            # Create and format title
            title = Text("Nuvei Terminal Simulator", style="bold cyan", justify="center")
            version_text = Text(f"\n{version}", style="bold magenta", justify="center")
            
            # Combine content into a panel
            panel = Panel.fit(
                title + version_text,
                border_style="green",
                title="Terminal Simulation",
                padding=(1, 2)  # Optional padding for aesthetics
            )
            
            # Center the panel on the screen
            centered_panel = Align.center(panel, vertical="middle")
            yield centered_panel  # Pass updated panel to Live
            
            await asyncio.sleep(0.5)  # Refresh rate

    # Use Rich's Live for continuous updates
    with Live(console=console, refresh_per_second=2, screen=True) as live:
        async for panel in generate_screen():
            live.update(panel)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[bold red]Simulation ended by user (Ctrl+C).[/bold red]")
