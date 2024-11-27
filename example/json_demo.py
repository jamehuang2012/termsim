from rich.console import Console
from rich.json import JSON

# Create a console object
console = Console()

# Example JSON data
data = {
    "title": "Network --> Cloud",
    "Data": {
        "OCSessionManagementRequest": {
            "header": {
                "messageFunction": "SASQ",
                "protocolVersion": "3.0",
                "exchangeIdentification": "ac10aad8-10ce-4abd-87ae-0af27b76de0b",
                "creationDateTime": "2024-11-25T19:49:27.322769+00:00",
                "initiatingParty": {
                    "identification": "12000337",
                    "authenticationKey": "fe0d12c9-2b21-41d1-abe3-cbabfbdff567",
                    "type": "TID"
                }
            },
            "sessionManagementRequest": {
                "POIComponent": {
                    "POIGroupIdentification": {
                        "exchangeAction": "NOTI"
                    },
                    "state": "IDLE"
                }
            }
        }
    }
}

# Print the JSON data using rich's built-in JSON renderer
console.print(JSON(data), style="bold cyan")
