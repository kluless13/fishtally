#!/bin/bash

# Exit if any command fails
set -e

# Echo commands
echo "Cloning ByteTrack repository..."
git clone https://github.com/ifzhang/ByteTrack.git
cd ByteTrack

echo "Modifying requirements for ByteTrack..."
sed -i 's/onnx==1.8.1/onnx==1.9.0/g' requirements.txt

echo "Installing requirements for ByteTrack..."
pip install -r requirements.txt

echo "Setting up ByteTrack..."
python setup.py develop

echo "ByteTrack installation completed."
cd ..
