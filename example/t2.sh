#!/bin/sh

# Define session and window names
session="$USER"
window="$session:1"

# Get terminal dimensions
lines="$(tput lines)"
columns="$(tput cols)"

# Start a new tmux session in detached mode
tmux -2 new-session -d -x "$columns" -y "$lines" -s "$session" 'echo "step -1"; bash'

# Enable mouse support
tmux set-option -g mouse on

# Create a new window for logs
tmux new-window -t "$window" -n 'Logs' 'echo "step 0"; bash' || exit

# Split the window into multiple panes
tmux split-window -t "$window" -h -p 30 -d 'echo "step 1"; bash'

tmux split-window -t "$window" -h -p 60 -d 'echo "step 2"; bash'


#tmux split-window -t "$window" -v -p 10 -b -d 'echo "step 2a"; bash'
# Uncomment to add a third vertical split
# tmux split-window -t "$window" -v -p 22 -d 'echo "step 2b"; bash'


# Split the top-right window into vertical panes
tmux split-window -t "$window.{top-left}" -v -p 80 -d
#tmux split-window -t "$window.{top-left}" -v -p 64

tmux split-window -t "$window.{top-right}" -v -p 35 -d


# Select the bottom-right pane
#tmux select-pane -t "$window.{bottom-right}"

# Additional vertical splits in the main window
#tmux split-window -t "$window.{buttom-left}" -h -p 67
#tmux split-window -t "$window" -h -p 50

# Select the window to view
tmux select-window -t "$window"

# Attach to the tmux session
tmux -2 attach-session -t "$session"
