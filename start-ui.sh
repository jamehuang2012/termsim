#!/usr/bin/env bash

MODE=$1

if [ "x$MODE" == "xdaemon" ]; then
    while true; do bash; done
    exit
fi

# Define session and window names
session="Termsim"

# Get terminal dimensions
lines="$(tput lines)"
columns="$(tput cols)"

function create-ui() {
    echo "Creating UI..."

    # Kill any existing session with the same name
    tmux has-session -t "$session" 2>/dev/null
    if [ $? != 0 ]; then
        tmux -2 new-session -d -x "$columns" -y "$lines" -s "$session" 'echo "step -1"; bash'
    else
        # If session exists, kill it and create a new one
        tmux kill-session -t "$session"
        tmux -2 new-session -d -x "$columns" -y "$lines" -s "$session" 'echo "step -1"; bash'
    fi

    # Enable mouse support
    tmux set-option -g mouse on

    # Create a new window for logs
    tmux new-window -t "$session:1" -n 'Logs' 'sleep 2; python3 ver.py' || exit

    # Split the window into multiple panes
    tmux split-window -t "$session:1" -h -p 30 -d 'python3 logshow.py /tmp/log_fifo'
    tmux split-window -t "$session:1" -h -p 55 -d 'sleep 2;python3 retail.py'

    # Split the top-left pane into vertical panes
    tmux split-window -t "$session:1.0" -v -p 85 -d 'python3 print.py /tmp/merc_fifo'

    tmux split-window -t "$session:1.1" -h -p 50 -d 'python3 print.py /tmp/cust_fifo'

    # Split the top-right pane into vertical panes
    tmux split-window -t "$session:1.4" -v -p 25 -d 'python3 status.py /tmp/status_fifo'

    # Select the window to view
    tmux select-window -t "$session:1.1"

    # Attach to the tmux session
    tmux -2 attach-session -t "$session"

    # Detach after attaching
    tmux detach -t "$session"

    echo "UI Created."
}

# Small delay for terminal sync
echo "Opening terminal..."
sleep 0.5

# Check if session exists and create UI if not
if ! tmux has-session -t "$session" 2>/dev/null; then
    create-ui
else
    # Attach to an existing session
    tmux attach-session -t "$session"
fi

echo "Connecting to UI..."

# Detach after connecting
exec tmux detach -t "$session"
