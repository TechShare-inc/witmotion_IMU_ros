#!/bin/bash

# Define the new rule
RULE='SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="HWT905"'

# File name for the new rule
RULE_FILE="/etc/udev/rules.d/99-usb-serial.rules"

# Function to create and write the new rule
create_rule() {
    echo "$RULE" | sudo tee "$RULE_FILE" > /dev/null
}

# Function to reload udev rules
reload_rules() {
    sudo udevadm control --reload-rules && sudo udevadm trigger
}

# Main script execution
create_rule
reload_rules

echo "New udev rule applied. Device should now be recognized as /dev/HWT905."

