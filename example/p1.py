import posix_ipc
import json

def send_to_queue(queue_name, message):
    # Create or open a named message queue
    mq = posix_ipc.MessageQueue(queue_name, posix_ipc.O_CREAT)
    
    # Convert message to JSON string and send
    mq.send(json.dumps(message))
    print(f"Message sent to the queue: {queue_name}")

    # Close the queue
    mq.close()

if __name__ == "__main__":
    queue_name = "/my_special_queue"  # POSIX message queues require names to start with '/'
    message = {"TerminalStatus": "BUSY", "TransactionStatus": "CMPT"}
    send_to_queue(queue_name, message)
