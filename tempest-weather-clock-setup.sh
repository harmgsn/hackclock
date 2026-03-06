#!/bin/bash

# 1. Update System
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install Dependencies for Python 3.13 & RGB Matrix
sudo apt-get install -y build-essential python3-dev python3-pip python3-pil \
libgraphicsmagick++-dev libwebp-dev fonts-dejavu

# 3. Setup Virtual Environment for Python 3.13
python3 -m venv env --system-site-packages
source env/bin/activate

# 4. Install Python Modules
pip install --upgrade pip
pip install requests pillow

# 5. Install RGB Matrix Library
# Note: This is the standard library for the Adafruit Hat
curl -sS https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/rgb-matrix.sh | bash

# Final Instructions
echo "-------------------------------------------------------"
echo "Installation Complete."
echo "1. Edit tempest_weather_clock.py with your API Key and Station ID."
echo "2. Run with sudo (required for GPIO access):"
echo "   sudo ./env/bin/python tempest_weather_clock.py"
echo "-------------------------------------------------------"
