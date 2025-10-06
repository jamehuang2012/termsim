import os
import json
import LoggerManager

# Enabled Status flag to enable status
ENABLE_STATUS = True

class FIFOStatusSender:
    def __init__(self, fifo_path: str = "/tmp/status_fifo"):
        self.fifo_path = fifo_path
        # Ensure the FIFO file exists
        if not os.path.exists(self.fifo_path):
            os.mkfifo(self.fifo_path)

    def send_status(self, status_data: dict):

        if not ENABLE_STATUS:
            return

        """Send a status dictionary to the FIFO."""
        try:
            with open(self.fifo_path, 'w') as fifo:
                fifo.write(json.dumps(status_data))  # Convert dict to JSON string
                fifo.flush()
                #print(f"Sent status data to FIFO: {status_data}")
        except Exception as e:
            log = LoggerManager.LoggerManager().logger
            log.error(f"Error sending data to FIFO: {e}")
        
        # close the file
        fifo.close()
        

# Example usage
if __name__ == "__main__":
    status_data = {
        "TerminalStatus": "INVALID",
        "TransactionStatus": "UNKNOWN",
        "Response": "ERROR",
        "CancelStatus": "N/A"
    }

    sender = FIFOStatusSender()
    sender.send_status(status_data)
