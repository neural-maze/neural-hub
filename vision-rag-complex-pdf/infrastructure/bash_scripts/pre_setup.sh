#!/bin/bash

set -e

# Rust install for uv usage
curl https://sh.rustup.rs -sSf | sh -s -- -y

# Rust path for uv shortcuts
export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"
source "$HOME/.cargo/env"

# System packages
sudo apt update && sudo apt install -y unzip zip \
    make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
    libffi-dev liblzma-dev

# uv installation
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
    command -v uv >/dev/null || { echo "uv is not in PATH."; exit 1; }
else
    echo "uv already installed"
fi

# pyproject.toml
if [ ! -f pyproject.toml ]; then
    echo "pyproject.toml not found."
    exit 1
fi

# uv dependencies in pyproject.toml
uv sync

# Virtual environment activation
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
    echo "Virtual environment activated."
else
    echo "Virtual environment not found."
    exit 1
fi

# dev tools installation
uv add --dev ruff pre-commit

export PYTHONPATH=/root
echo 'export PYTHONPATH=/root' >> ~/.bashrc

# pre-commit installation
if [ -f .pre-commit-config.yaml ]; then
    pre-commit install
    echo "pre-commit installed."
else
    echo ".pre-commit-config.yaml not found."
fi