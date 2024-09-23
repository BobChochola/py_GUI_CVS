#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Creating executable..."
pyinstaller --name="MemberListGenerator" --windowed --onefile gui.py

echo "Build complete!"
