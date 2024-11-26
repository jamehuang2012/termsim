import os
import json

import LoggerManager

class Monitor:
    def __init__(self, payload, title):
        self.payload = payload
        self.title = title

    def send_to_log_fifo(self):
        fifo_path = '/tmp/log_fifo'
        if not os.path.exists(fifo_path):
            os.mkfifo(fifo_path)
        
        with open(fifo_path, 'w') as fifo:
            # clear the log file first 
            fifo.truncate(0)

            log_entry = json.dumps({'title': self.title, 'Data': self.payload})
            fifo.write(log_entry + '\n')
            fifo.flush()  # Ensure data is written

# Example usage
def log_monitor(title, payload):

    #log = LoggerManager.LoggerManager().logger
    #log.debug("payload" + payload)
    monitor = Monitor(payload, title)
    monitor.send_to_log_fifo()


