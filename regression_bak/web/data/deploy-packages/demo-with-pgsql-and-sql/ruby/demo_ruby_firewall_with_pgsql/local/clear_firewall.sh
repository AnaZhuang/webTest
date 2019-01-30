#!/bin/sh
# [Config]
# LOCALPORTRANGESTART=32768
# LOCALPORTRANGEEND=61000

echo "Clear iptables."

iptables -F
iptables -X

iptables -P FORWARD ACCEPT
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT

echo "Finished."

true
