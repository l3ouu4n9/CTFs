FROM gcr.io/spiffe-io/spire-agent:unstable as spire

COPY conf/agent.conf /opt/spire/conf/agent/agent.conf
COPY conf/user-service_agent.key /opt/spire/conf/agent/agent.key
COPY conf/user-service_agent.crt /opt/spire/conf/agent/agent.crt
COPY user-service /usr/local/bin/user-service

WORKDIR /opt/spire
ENTRYPOINT []
CMD user-service
