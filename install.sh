#!/bin/bash
set -e

echo "Installing Offensive Tools Launcher..."

# Check dependencies
if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Install system dependencies
echo "Installing system dependencies..."
if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y python3-gi gir1.2-gtk-3.0
elif command -v yum >/dev/null 2>&1; then
    sudo yum install -y python3-gobject gtk3-devel
elif command -v pacman >/dev/null 2>&1; then
    sudo pacman -S python-gobject gtk3
else
    echo "Warning: Could not install dependencies automatically."
    echo "Please install: python3-gi gir1.2-gtk-3.0 (or equivalent)"
fi

# Make launcher executable
chmod +x tools-launcher.py

# Install desktop entry
echo "Installing desktop entry..."
mkdir -p ~/.local/share/applications
INSTALL_DIR=$(pwd)
sed "s|%k|$INSTALL_DIR|g" desktop/tools-launcher.desktop > ~/.local/share/applications/tools-launcher.desktop

# Create config directory
mkdir -p ~/.config/tools-launcher

echo "Installation complete!"
echo ""
echo "You can now launch the tool by:"
echo "1. Running: ./tools-launcher.py"
echo "2. From Applications menu: Development -> Offensive Tools"
echo ""
echo "Don't forget to configure your GitHub token for enhanced features!"