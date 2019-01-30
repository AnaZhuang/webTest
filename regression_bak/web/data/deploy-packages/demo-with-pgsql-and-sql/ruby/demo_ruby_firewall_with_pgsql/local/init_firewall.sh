#!/bin/sh
# [Config]
# LOCALPORTRANGESTART=32768
# LOCALPORTRANGEEND=61000

echo "Using iptables."
echo "Resetting firewall rules."

#################################################
# 1.clear firewall & initialize kernel parameters 
#################################################

# Shut down all traffic
iptables -P FORWARD DROP
iptables -P INPUT DROP
iptables -P OUTPUT DROP

# Delete any existing chains
iptables -F
iptables -X

echo "Setting kernel parameters."
# Turn on kernel IP spoof protection
echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_broadcasts 2> /dev/null
# Set the TCP timestamps config
echo 0 > /proc/sys/net/ipv4/tcp_timestamps 2> /dev/null
# Enable TCP SYN Cookie Protection if available
test -e /proc/sys/net/ipv4/tcp_syncookies && echo 1 > /proc/sys/net/ipv4/tcp_syncookies 2> /dev/null
echo 0 > /proc/sys/net/ipv4/conf/all/accept_source_route 2> /dev/null
echo 0 > /proc/sys/net/ipv4/conf/default/accept_source_route 2> /dev/null
# Log truly weird packets.
echo 1 > /proc/sys/net/ipv4/conf/all/log_martians 2> /dev/null
echo 1 > /proc/sys/net/ipv4/conf/default/log_martians 2> /dev/null
echo "32768 61000" > /proc/sys/net/ipv4/ip_local_port_range 2> /dev/null

echo "Configuring firewall rules."

#################################################
# 2.Set up our logging and drop,reject chains 
#################################################

# Set up our logging and packet 'executing' chains
#iptables -N logdrop2
#iptables -A logdrop2 -j LOG --log-prefix "DROPPED " --log-level 4 --log-ip-options --log-tcp-options --log-tcp-sequence 
#iptables -A logdrop2 -j DROP
#iptables -N logdrop
#iptables -A logdrop -m limit --limit 1/second --limit-burst 10 -j logdrop2
#iptables -A logdrop -m limit --limit 2/minute --limit-burst 1 -j LOG --log-prefix "LIMITED " --log-level 4
#iptables -A logdrop -j DROP
#iptables -N logreject2
#iptables -A logreject2 -j LOG --log-prefix "REJECTED " --log-level 4 --log-ip-options --log-tcp-options --log-tcp-sequence 
#iptables -A logreject2 -p tcp -j REJECT --reject-with tcp-reset
#iptables -A logreject2 -p udp -j REJECT --reject-with icmp-port-unreachable
#iptables -A logreject2 -j DROP
#iptables -N logreject
#iptables -A logreject -m limit --limit 1/second --limit-burst 10 -j logreject2
#iptables -A logreject -m limit --limit 2/minute --limit-burst 1 -j LOG --log-prefix "LIMITED " --log-level 4
#iptables -A logreject -p tcp -j REJECT --reject-with tcp-reset
#iptables -A logreject -p udp -j REJECT --reject-with icmp-port-unreachable
#iptables -A logreject -j DROP
#iptables -N logaborted2
#iptables -A logaborted2 -j LOG --log-prefix "ABORTED " --log-level 4 --log-ip-options --log-tcp-options --log-tcp-sequence 
#iptables -A logaborted2 -m state --state ESTABLISHED,RELATED -j ACCEPT
#iptables -N logaborted
#iptables -A logaborted -m limit --limit 1/second --limit-burst 10 -j logaborted2
#iptables -A logaborted -m limit --limit 2/minute --limit-burst 1 -j LOG --log-prefix "LIMITED " --log-level 4

#################################################
# 3.allow loopback traffic & broadcasts 
#################################################

# Allow loopback traffic.
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Switch the current language for a moment
GUARDDOG_BACKUP_LANG=$LANG
GUARDDOG_BACKUP_LC_ALL=$LC_ALL
LANG=US
LC_ALL=US
export LANG
export LC_ALL
# Accept broadcasts from ourself.
IP_BCAST_PAIRS="`ifconfig | gawk '/^\w/ { nic = gensub(/^(.*):.*/,\"\\\\1\",\"g\",$1)}
/inet addr:.*Bcast/ {match($0,/inet addr:[[:digit:]\\.]+/)
ip=substr($0,RSTART+10,RLENGTH-10)
match($0,/Bcast:[[:digit:]\\.]+/)
bcast = substr($0,RSTART+6,RLENGTH-6)
printf \"%s_%s_%s\\n\",nic,ip,bcast }'`"
# Restore the language setting
LANG=$GUARDDOG_BACKUP_LANG
LC_ALL=$GUARDDOG_BACKUP_LC_ALL
export LANG
export LC_ALL
for X in $IP_BCAST_PAIRS ; do
  NIC="`echo \"$X\" | cut -f 1 -d _`"
  IP="`echo \"$X\" | cut -f 2 -d _`"
  BCAST="`echo \"$X\" | cut -f 3 -d _`"
  iptables -A INPUT -i $NIC -s $IP -d $BCAST -j ACCEPT
done

#can accept udp broadcast port 33333
#it's for clear all firewall ruleset
iptables -A INPUT -p udp --dport 33333 -m state --state NEW -j ACCEPT

#################################################
# 4.common setting of tcp & icmp 
#################################################

# Detect aborted TCP connections.
iptables -A INPUT -m state --state ESTABLISHED,RELATED -p tcp --tcp-flags RST RST -j logaborted
# Quickly allow anything that belongs to an already established connection.
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow certain critical ICMP types
iptables -A INPUT -p icmp --icmp-type destination-unreachable -j ACCEPT  # Dest unreachable
iptables -A OUTPUT -p icmp --icmp-type destination-unreachable -j ACCEPT # Dest unreachable
iptables -A FORWARD -p icmp --icmp-type destination-unreachable -j ACCEPT &> /dev/null  # Dest unreachable
iptables -A INPUT -p icmp --icmp-type time-exceeded -j ACCEPT            # Time exceeded
iptables -A OUTPUT -p icmp --icmp-type time-exceeded -j ACCEPT           # Time exceeded
iptables -A FORWARD -p icmp --icmp-type time-exceeded -j ACCEPT &> /dev/null # Time exceeded
iptables -A INPUT -p icmp --icmp-type parameter-problem -j ACCEPT        # Parameter Problem
iptables -A OUTPUT -p icmp --icmp-type parameter-problem -j ACCEPT       # Parameter Problem
iptables -A FORWARD -p icmp --icmp-type parameter-problem -j ACCEPT &> /dev/null # Parameter Problem

