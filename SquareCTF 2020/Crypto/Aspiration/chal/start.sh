#!/bin/bash

set -e

bb=$(tput bold)
nn=$(tput sgr0)

fingerprint() {
	# calculate the SHA1 digest of the DER bytes of the certificate using the
	# "coreutils" output format (`-r`) to provide uniform output from
	# `openssl sha1` on macOS and linux.
	cat $1 | openssl x509 -outform DER | openssl sha1 -r | awk '{print $1}'
}

USER_WEBAPP_AGENT_FINGERPRINT=$(fingerprint docker/user-webapp/conf/user-webapp_agent.crt)
USER_SERVICE_AGENT_FINGERPRINT=$(fingerprint docker/user-service/conf/user-service_agent.crt)
FLAG_SERVICE_AGENT_FINGERPRINT=$(fingerprint docker/flag-service/conf/flag-service_agent.crt)

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

(cd src/user-webapp && GOOS=linux go build -v -o $DIR/docker/user-webapp/user-webapp && cp index.html $DIR/docker/user-webapp/index.html)
(cd src/user-service && GOOS=linux go build -v -o $DIR/docker/user-service/user-service)
(cd src/flag-service && GOOS=linux go build -v -o $DIR/docker/flag-service/flag-service)
(cd src/workload-registrar && GOOS=linux go build -v -o $DIR/docker/spire-server/workload-registrar)
(cd src/bundle-service && GOOS=linux go build -v -o $DIR/docker/spire-server/bundle-service)

docker-compose -f docker-compose.yml build

docker-compose up -d

# Bootstrap trust to the SPIRE server for each agent by copying over the
# trust bundle into each agent container.
echo "${bb}Bootstrapping trust between SPIRE agents and SPIRE server...${nn}"
docker-compose exec -T spire-server bin/spire-server bundle show |
	docker-compose exec -T user-webapp tee conf/agent/bootstrap.crt > /dev/null
docker-compose exec -T spire-server bin/spire-server bundle show |
	docker-compose exec -T user-service tee conf/agent/bootstrap.crt > /dev/null
docker-compose exec -T spire-server bin/spire-server bundle show |
	docker-compose exec -T flag-service tee conf/agent/bootstrap.crt > /dev/null

# Start up the user-webapp SPIRE agent.
echo "${bb}Starting user-webapp SPIRE agent...${nn}"
docker-compose exec -d user-webapp bin/spire-agent run

# Start up the user-service SPIRE agent.
echo "${bb}Starting user-service SPIRE agent...${nn}"
docker-compose exec -d user-service bin/spire-agent run

# Start up the flag-service SPIRE agent.
echo "${bb}Starting flag-service SPIRE agent...${nn}"
docker-compose exec -d flag-service bin/spire-agent run

# create registration entries
echo "${bb}Creating registration entry for the user-webapp...${nn}"
docker-compose exec spire-server bin/spire-server entry create \
	-parentID spiffe://square.ctf.chal/spire/agent/x509pop/${USER_WEBAPP_AGENT_FINGERPRINT} \
	-spiffeID spiffe://square.ctf.chal/userWeb \
	-selector unix:user:root \

echo "${bb}Creating registration entry for the user-service...${nn}"
docker-compose exec spire-server bin/spire-server entry create \
	-parentID spiffe://square.ctf.chal/spire/agent/x509pop/${USER_SERVICE_AGENT_FINGERPRINT} \
	-spiffeID spiffe://square.ctf.chal/userService \
	-selector unix:user:root \

echo "${bb}Creating registration entry for the flag-service...${nn}"
docker-compose exec spire-server bin/spire-server entry create \
	-parentID spiffe://square.ctf.chal/spire/agent/x509pop/${FLAG_SERVICE_AGENT_FINGERPRINT} \
	-spiffeID spiffe://square.ctf.chal/flagService \
	-selector unix:user:root \
