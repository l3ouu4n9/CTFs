FROM alpine:3

RUN apk --no-cache update
RUN apk --no-cache upgrade
RUN apk --no-cache add bash socat

# ENVIRONMENT
WORKDIR /home

# FLAG
COPY flag.txt flag
RUN chown root:root flag
RUN chmod 444 flag

# USER
RUN adduser -D anon
RUN echo "anon:password" | chpasswd anon

# SERVER
ENTRYPOINT [ \
    "socat", \
    "-T60", \
    "TCP-LISTEN:8000,reuseaddr,fork,su=anon", \
    "EXEC:'/bin/sh -c \\'/usr/bin/env -i /bin/bash --norc --noprofile --restricted 2>/dev/null 1>/dev/null\\'',pty,stderr" \
]
