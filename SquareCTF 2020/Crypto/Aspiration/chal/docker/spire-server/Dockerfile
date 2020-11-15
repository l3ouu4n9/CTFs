FROM gcr.io/spiffe-io/spire-server:unstable

# Override spire configurations
COPY conf/server.conf /opt/spire/conf/server/server.conf
COPY conf/square_ctf_CA.crt /opt/spire/conf/server/square_ctf_CA.crt

COPY workload-registrar /usr/local/bin/workload-registrar
COPY bundle-service /usr/local/bin/bundle-service

WORKDIR /opt/spire

COPY start.sh .
ENTRYPOINT ["./start.sh"]