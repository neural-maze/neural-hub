#!/bin/bash

set -e

echo "Searching RUNPOD API KEY in .env"

if [ ! -f .env ]; then
  echo ".env not found."
  exit 1
fi

API_KEY=$(grep -E '^RUNPOD_API_KEY=' .env | cut -d '=' -f2- | tr -d '"')

if [ -z "$API_KEY" ]; then
  echo "RUNPOD API KEY not defined in .env"
  exit 1
fi

echo "RUNPOD API KEY found."

echo "Downloading runpodctl."
wget -q https://github.com/Run-Pod/runpodctl/releases/download/v1.14.3/runpodctl-linux-amd64 -O runpodctl
chmod +x runpodctl
sudo mv runpodctl /usr/local/bin/runpodctl

echo "runpodctl installed: $(runpodctl --version)"

echo "Enabling runpodctl with RUNPOD API KEY."
runpodctl config --apiKey "$API_KEY"

echo "runpodctl installed and configured."
