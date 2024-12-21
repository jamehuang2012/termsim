from flask import Flask, request, jsonify
import threading
import time
import LoggerManager
from ParameterSingleton import ParameterSingleton
from StringUtily import TerminalStatus, TransactionStatus
from TransactionData import TransactionData
import sslclient as client

app = Flask(__name__)

# Store configurations for multiple TIDs
tid_instances = {}
threads = {}
stop_events = {}

# Default configuration
DEFAULT_CONFIG = {
    "amount_details": {
        "Tip": "0.00",
        "Cashback": "0.00",
        "Surcharge": "0.00",
        "Fee": "0.00"
    },
    "features": {
        "Send Signature": False,
        "Currency Code": "CAD",
        "Split Payment": False,
        "Split Amount": "0.00"
    },
    "terminal_status": "IDLE",
    "transaction_status": "NoneStatus"
}

def transaction_thread(tid, stop_event):
    """Thread to perform periodic transactions for a specific TID."""
    log = LoggerManager.LoggerManager().logger
    while not stop_event.is_set():
        log.debug(f"TID {tid}: Thread running.")
        client.doTransaction()
        time.sleep(5)

@app.route("/start_tid", methods=["POST"])
def start_tid():
    """Start a new TID instance."""
    data = request.json
    tid = data.get("TID")
    auth_key = data.get("Auth Key")

    if not tid or tid in tid_instances:
        return jsonify({"error": "Invalid or duplicate TID"}), 400

    # Initialize configuration
    tid_instances[tid] = {
        "config": DEFAULT_CONFIG.copy(),
        "auth_key": auth_key
    }

    # Start thread
    stop_event = threading.Event()
    thread = threading.Thread(target=transaction_thread, args=(tid, stop_event))
    threads[tid] = thread
    stop_events[tid] = stop_event
    thread.start()

    return jsonify({"message": f"TID {tid} started successfully."}), 200

@app.route("/stop_tid/<tid>", methods=["POST"])
def stop_tid(tid):
    """Stop a TID instance."""
    if tid not in tid_instances:
        return jsonify({"error": "TID not found"}), 404

    # Stop thread
    stop_events[tid].set()
    threads[tid].join()
    del tid_instances[tid]
    del threads[tid]
    del stop_events[tid]

    return jsonify({"message": f"TID {tid} stopped successfully."}), 200

@app.route("/update_config/<tid>", methods=["PUT"])
def update_config(tid):
    """Update configuration for a specific TID."""
    if tid not in tid_instances:
        return jsonify({"error": "TID not found"}), 404

    config = request.json
    tid_instances[tid]["config"].update(config)

    # Update TransactionData object
    transaction_data = TransactionData()
    transaction_data.tipAmount = tid_instances[tid]["config"]["amount_details"]["Tip"]
    transaction_data.cashback = tid_instances[tid]["config"]["amount_details"]["Cashback"]
    transaction_data.surchargeFee = tid_instances[tid]["config"]["amount_details"]["Surcharge"]
    transaction_data.serviceFee = tid_instances[tid]["config"]["amount_details"]["Fee"]
    transaction_data.currencyCode = tid_instances[tid]["config"]["features"]["Currency Code"]
    transaction_data.splitPayment = tid_instances[tid]["config"]["features"]["Split Payment"]
    transaction_data.splitAmount = tid_instances[tid]["config"]["features"]["Split Amount"]
    transaction_data.terminalStatus = tid_instances[tid]["config"]["terminal_status"]
    transaction_data.status = getattr(TransactionStatus, tid_instances[tid]["config"]["transaction_status"], TransactionStatus.NoneStatus)

    return jsonify({"message": f"TID {tid} configuration updated successfully."}), 200

@app.route("/status/<tid>", methods=["GET"])
def status(tid):
    """Get the status of a specific TID."""
    if tid not in tid_instances:
        return jsonify({"error": "TID not found"}), 404

    return jsonify(tid_instances[tid]), 200

@app.route("/list_tids", methods=["GET"])
def list_tids():
    """List all active TIDs."""
    return jsonify({"active_tids": list(tid_instances.keys())}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
