#!/bin/bash

# Exit if any command fails
set -e

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setup completed."
