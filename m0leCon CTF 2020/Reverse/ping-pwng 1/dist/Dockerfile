FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install freeglut3-dev python3 python3-pip libgmp3-dev
RUN pip3 install coloredlogs fastecdsa
RUN groupadd -r pwn && useradd -r -g pwn pwn

ADD challenge/chall /home/pwn/chall

ADD challenge/entrypoint.sh /home/pwn/entrypoint.sh
RUN chmod +x        /home/pwn/chall

RUN chmod +x /home/pwn/entrypoint.sh
RUN chmod 1733 /tmp

ADD challenge/flag.txt /home/pwn/flag.txt
RUN chmod 440 /home/pwn/flag.txt
ADD challenge/flag_rev.txt /home/pwn/flag_rev.txt
RUN chmod 440 /home/pwn/flag_rev.txt
RUN chown -R root:pwn /home/pwn
ADD challenge/server.py    /home/pwn/server.py
RUN chmod +x        /home/pwn/server.py
ADD challenge/cryptoService.py /home/pwn/cryptoService.py
RUN chmod +x /home/pwn/cryptoService.py
ADD challenge/ecdsa.py /home/pwn/ecdsa.py
RUN chmod +x /home/pwn/ecdsa.py
RUN ls /home/pwn -lh
