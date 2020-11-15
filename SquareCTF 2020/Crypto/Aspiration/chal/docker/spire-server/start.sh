#!/bin/sh

workload-registrar &
bundle-service &
/usr/bin/dumb-init /opt/spire/bin/spire-server run