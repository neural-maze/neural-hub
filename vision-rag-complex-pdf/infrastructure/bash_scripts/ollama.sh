#!/bin/bash

curl -fsSL https://ollama.com/install.sh | sh

ollama serve &

sleep 10

ollama pull gemma3:27b