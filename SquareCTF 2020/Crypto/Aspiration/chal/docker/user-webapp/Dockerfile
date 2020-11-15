FROM gcr.io/spiffe-io/spire-agent:unstable

COPY conf/agent.conf /opt/spire/conf/agent/agent.conf
COPY conf/user-webapp_agent.key /opt/spire/conf/agent/agent.key
COPY conf/user-webapp_agent.crt /opt/spire/conf/agent/agent.crt
COPY user-webapp /usr/local/bin/user-webapp
COPY index.html /opt/spire/index.html

WORKDIR /opt/spire
ENTRYPOINT []

CMD user-webapp
