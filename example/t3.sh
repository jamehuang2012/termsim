#!/bin/bash

SESSION_NAME="termsim"

# Check if the session already exists
tmux has-session -t $SESSION_NAME 2>/dev/null
if [ $? != 0 ]; then



    # Create a new session
    tmux new-session -d -s $SESSION_NAME
    
    tmux set-option -g mouse on

    # Window 1: Split panes
    tmux new-window -t $SESSION_NAME:1 -n 'Split1'
    
    # Split the window horizontally into two panes (left 40%, right 60%)
    tmux split-window -h -t $SESSION_NAME:1
    
    # Resize the left pane to 40% width
    tmux resize-pane -R -t $SESSION_NAME:1.0 10   # 40% width adjustment
    
    # Split the right pane into two (top-right 25%, bottom-right 35%)
    tmux split-window -h -t $SESSION_NAME:1.1   # Split the right pane horizontally

    tmux split-window -t $SESSION_NAME:1.1 -v -p 5 -b -d 'echo "step 2a"; bash'


    
    # Resize the middle pane to 25%
    tmux resize-pane -R -t $SESSION_NAME:1.1 5   # 25% width adjustment


    #s Split the right pane into two (bottom-left 50%, bottom-right 50%)

    tmux split-window -h -t  $SESSION_NAME:1.2 


    # Resize the bottom-right pane to 35% width
    tmux resize-pane -R -t $SESSION_NAME:1.3 10   # 35% width adjustment
    

    # Split the bottom-right pane vertically into two panes (top 60%, bottom 40%)
    tmux split-window -v -t $SESSION_NAME:1.3   # Split the bottom-right pane vertically

    

   # Set up commands in each pane
    tmux select-pane -t $SESSION_NAME:1.0
    tmux send-keys -t $SESSION_NAME:1.0 'echo "$SESSION_NAME:1.0"' C-m

    
    tmux select-pane -t $SESSION_NAME:1.1
    tmux send-keys -t $SESSION_NAME:1.1 'echo "$SESSION_NAME:1.1"' C-m

    tmux select-pane -t $SESSION_NAME:1.2
    tmux send-keys -t $SESSION_NAME:1.2 'echo "$SESSION_NAME:1.2"' C-m

    tmux select-pane -t $SESSION_NAME:1.3
    tmux send-keys -t $SESSION_NAME:1.3 'echo "$SESSION_NAME:1.3"' C-m

    tmux select-pane -t $SESSION_NAME:1.4
    tmux send-keys -t $SESSION_NAME:1.4 'echo "$SESSION_NAME:1.4"' C-m

    # tmux select-pane -t $SESSION_NAME:1.2
    # tmux send-keys -t $SESSION_NAME:1.2 'echo "Bottom-Right Pane (Top)"' C-m

    # tmux select-pane -t $SESSION_NAME:1.3
    # tmux send-keys -t $SESSION_NAME:1.3 'echo "Bottom-Right Pane (Bottom)"' C-m

fi

# Attach to the session
tmux attach -t $SESSION_NAME
