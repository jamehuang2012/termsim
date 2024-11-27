import json
import os

fifo_path = "/tmp/sta_fifo"

def create_fifo_and_write():
    # Ensure the FIFO exists
    if not os.path.exists(fifo_path):
        os.mkfifo(fifo_path)

    # Prepare data to write
    data = json.dumps({"TerminalStatus": "BUSY", "TransactionStatus": "CMPT"}).encode()

    # Open FIFO in write mode
    with open(fifo_path, "w") as fifo:
        fifo.write(data.decode())  # Decode bytes to a string before writing
        print(f"Data written to FIFO: {fifo_path}")

if __name__ == "__main__":
    create_fifo_and_write()
