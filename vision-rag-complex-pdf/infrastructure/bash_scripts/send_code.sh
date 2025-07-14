#!/bin/bash

set -e

ZIP_NAME="project_code.zip"
HOST="runpod-pytorch"

echo "Code zipped in: ${ZIP_NAME}..."
zip -r "$ZIP_NAME" . -x ".venv/*" "uv.lock" "*.git*" "node_modules/*" "__pycache__/*"

echo "Sending ${ZIP_NAME} to the remote host."

OUTPUT=$(runpodctl send "$ZIP_NAME")
echo "$OUTPUT"

