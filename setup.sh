#!/bin/bash
pkg update && pkg upgrade -y
pkg install python git -y
pip install flask requests
echo "[+] Setup finished! Run 'python app.py' to start."
