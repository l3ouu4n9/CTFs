#!/bin/bash

echo " █     █░▓█████  ██▓     ▄████▄   ▒█████   ███▄ ▄███▓▓█████ ";
echo "▓█░ █ ░█░▓█   ▀ ▓██▒    ▒██▀ ▀█  ▒██▒  ██▒▓██▒▀█▀ ██▒▓█   ▀ ";
echo "▒█░ █ ░█ ▒███   ▒██░    ▒▓█    ▄ ▒██░  ██▒▓██    ▓██░▒███   ";
echo "░█░ █ ░█ ▒▓█  ▄ ▒██░    ▒▓▓▄ ▄██▒▒██   ██░▒██    ▒██ ▒▓█  ▄ ";
echo "░░██▒██▓ ░▒████▒░██████▒▒ ▓███▀ ░░ ████▓▒░▒██▒   ░██▒░▒████▒";
echo "░ ▓░▒ ▒  ░░ ▒░ ░░ ▒░▓  ░░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░   ░  ░░░ ▒░ ░";
echo "  ▒ ░ ░   ░ ░  ░░ ░ ▒  ░  ░  ▒     ░ ▒ ▒░ ░  ░      ░ ░ ░  ░";
echo "  ░   ░     ░     ░ ░   ░        ░ ░ ░ ▒  ░      ░      ░   ";
echo "    ░       ░  ░    ░  ░░ ░          ░ ░         ░      ░  ░";
echo "                        ░                                   ";
echo "                  ▄▄▄█████▓ ▒█████                          ";
echo "                  ▓  ██▒ ▓▒▒██▒  ██▒                        ";
echo "                  ▒ ▓██░ ▒░▒██░  ██▒                        ";
echo "                  ░ ▓██▓ ░ ▒██   ██░                        ";
echo "                    ▒██▒ ░ ░ ████▓▒░                        ";
echo "                    ▒ ░░   ░ ▒░▒░▒░                         ";
echo "                      ░      ░ ▒ ▒░                         ";
echo "                    ░      ░ ░ ░ ▒                          ";
echo "                               ░ ░                          ";
echo "                                                            ";
echo " ▄▄▄▄    ▄▄▄        ██████  ██░ ██ ▓█████  ██▓     ██▓      ";
echo "▓█████▄ ▒████▄    ▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒      ";
echo "▒██▒ ▄██▒██  ▀█▄  ░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░      ";
echo "▒██░█▀  ░██▄▄▄▄██   ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░      ";
echo "░▓█  ▀█▓ ▓█   ▓██▒▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒  ";
echo "░▒▓███▀▒ ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░  ";
echo "▒░▒   ░   ▒   ▒▒ ░░ ░▒  ░ ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░  ";
echo " ░    ░   ░   ▒   ░  ░  ░   ░  ░░ ░   ░     ░ ░     ░ ░     ";
echo " ░            ░  ░      ░   ░  ░  ░   ░  ░    ░  ░    ░  ░  ";
echo "      ░                                                     ";
echo "The flag is in /flag"
echo -n "$ "
read -re inp
exec 0<&-

rex="^[]\[\$<\\_']+$"
if [[ $inp =~ $rex ]]
then
  bash -c $inp
else
  echo "Only 1337 h4ck3r5 are allowed to pass"
fi
