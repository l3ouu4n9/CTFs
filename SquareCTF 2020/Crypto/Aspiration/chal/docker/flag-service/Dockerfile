FROM gcr.io/spiffe-io/spire-agent:unstable as spire

COPY conf/agent.conf /opt/spire/conf/agent/agent.conf
COPY conf/flag-service_agent.key /opt/spire/conf/agent/agent.key
COPY conf/flag-service_agent.crt /opt/spire/conf/agent/agent.crt
COPY flag-service /usr/local/bin/flag-service

WORKDIR /opt/spire
ENTRYPOINT []
CMD flag-service
