#!/bin/bash
echo "Here we go, starting the server..."
python3 -u /home/pwn/server.py & python3 -u /home/pwn/cryptoService.py
