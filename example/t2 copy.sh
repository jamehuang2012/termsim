#!/bin/sh

session="$USER"
window="$session:1"

lines="$(tput lines)"
columns="$(tput cols)"

tmux -2 new-session -d -x "$columns" -y "$lines" -s "$session" 'echo "step -1"; bash'
tmux new-window -t "$window" -n 'Logs' 'echo "step 0"; bash' || exit

tmux split-window -t "$window"             -h -p 67    -d 'echo "step 1";  bash'
tmux split-window -t "$window"             -v -p 10 -b -d 'echo "step 2a"; bash'
tmux split-window -t "$window"             -v -p 22    -d 'echo "step 2b"; bash'
tmux split-window -t "$window"             -h -p 50       'echo "step 3";  bash'
tmux split-window -t "$window.{top-right}" -v -p 55    -d
tmux split-window -t "$window.{top-right}" -v -p 64
tmux select-pane  -t "$window.{bottom-right}"
tmux split-window -t "$window"             -v -p 67
tmux split-window -t "$window"             -v -p 50

tmux select-window -t "$window"

# Attach to session
tmux -2 attach-session -t "$session"
