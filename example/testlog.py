import os
import subprocess
import time

# Define the path to the FIFO
fifo_path = '/tmp/log_fifo'

# JSON data to be written to the FIFO
json_data = '''{
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
}'''

# Ensure the FIFO exists
if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

# Use subprocess to echo the data into the FIFO
def write_to_fifo(data):
    with subprocess.Popen(['echo', data], stdout=subprocess.PIPE) as proc:
        with open(fifo_path, 'w') as fifo:
            fifo.write(data)

# Write JSON data into the FIFO
write_to_fifo(json_data)

# Wait a bit for the data to be written
time.sleep(1)

print("Data written to FIFO.")
