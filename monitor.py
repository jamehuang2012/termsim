import posix_ipc
import time
import logging
import json

class Monitor:
    def __init__(self, payload, title, max_retries=5, retry_delay=0.5):
        self.queue_name = "/log_queue"
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = logging.getLogger("MonitorLogger")
        self.payload = payload
        self.title = title

    def send_to_message_queue(self):
        try:
            # Open the message queue
            mq = posix_ipc.MessageQueue(self.queue_name, posix_ipc.O_CREAT)
        except posix_ipc.ExistentialError as e:
            self.logger.error(f"Failed to open queue: {e}")
            return

        log_entry = json.dumps({'title': self.title, 'Data': self.payload})
        for attempt in range(self.max_retries):
            try:
                mq.send(log_entry, timeout=1)  # Send with a 1-second timeout
                self.logger.info(f"Message sent successfully: {log_entry}")
                break  # Exit retry loop if successful
            except posix_ipc.BusyError:
                self.logger.warning(f"Queue full. Retry {attempt + 1}/{self.max_retries}")
                time.sleep(self.retry_delay)  # Wait before retrying
            except Exception as e:
                self.logger.error(f"Error sending message: {e}")
                break  # Exit on unexpected errors
        else:
            self.logger.error("Queue full. Message discarded after max retries.")

        # Ensure the message queue is closed
        mq.close()

# Function to log messages
def log_monitor(title, payload):
    monitor = Monitor(payload, title)
    monitor.send_to_message_queue()

# Example logger configuration (if not configured elsewhere)
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    log_monitor("TestMessage", {"status": "OK"})
