FROM ubuntu:20.04

RUN apt-get update && \
  apt-get -y install bind9-dnsutils libncursesw6

COPY client /

# Make sure locales is set to UTF8
RUN apt-get install -y locales && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8

# Make sure your terminal supports color, and displays emojis such as 🏆
ENV TERM xterm-256color

ENV LANG   C.UTF-8
ENV LC_ALL C.UTF-8
ENV LC_ALL en_US.UTF-8 

ENTRYPOINT [ "bash", "-c", "/client $(dig maze.chal.perfect.blue +short) 1" ]
