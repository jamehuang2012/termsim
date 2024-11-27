import posix_ipc
import json

def receive_from_queue(queue_name):
    # Open an existing named message queue
    mq = posix_ipc.MessageQueue(queue_name)
    
    # Receive message (returns a tuple: (message, priority))
    message, _ = mq.receive()
    
    # Deserialize and print the message
    data = json.loads(message.decode())
    print(f"Message received from the queue: {queue_name}")
    print(data)
    
    # Close the queue
    mq.close()

if __name__ == "__main__":
    queue_name = "/my_special_queue"
    receive_from_queue(queue_name)
