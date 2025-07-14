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

# CUDA drivers and CUDA toolkit installation
sudo apt-key del 7fa2af80 || true
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-8
rm -f cuda-keyring_1.1-1_all.deb

# CUDA environment variables to PATH
grep -qxF 'export PATH=/usr/local/cuda-12.8/bin${PATH:+:${PATH}}' ~/.bashrc || echo 'export PATH=/usr/local/cuda-12.8/bin${PATH:+:${PATH}}' >> ~/.bashrc
grep -qxF 'export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}' ~/.bashrc || echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}' >> ~/.bashrc

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