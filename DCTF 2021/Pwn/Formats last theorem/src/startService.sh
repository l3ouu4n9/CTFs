#!/bin/bash
chown pilot:pilot /app/formats_last_theorem
chmod +x /app/formats_last_theorem
while true; do
    su pilot -c 'timeout -k 30 1d socat TCP-LISTEN:7482,nodelay,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 ./formats_last_theorem"'
done