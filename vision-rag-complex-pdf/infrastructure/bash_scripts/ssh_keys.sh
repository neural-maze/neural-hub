#!/bin/bash
set -e

SSH_DIR="$HOME/.ssh"
KEY_PATH="$SSH_DIR/id_ed25519"

mkdir -p "$SSH_DIR"
chmod 700 "$SSH_DIR"

if [ ! -f "$KEY_PATH" ]; then
    echo "Generating new SSH key in $KEY_PATH"
    ssh-keygen -t ed25519 -f "$KEY_PATH" -N ""
else
    echo "SSH key already exists in $KEY_PATH"
fi

echo "Public SSH key:"
cat "$KEY_PATH.pub"
