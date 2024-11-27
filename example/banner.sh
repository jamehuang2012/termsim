#!/bin/bash

# Loop for back-and-forth animation
while true; do
    for i in {1..20}; do
        clear  # Clear the screen
        printf "%${i}s" " "  # Add spaces to shift text to the right
        echo "NUVEI" | figlet | lolcat -a
        sleep 0.5  # Delay for animation speed
    done
    
done

