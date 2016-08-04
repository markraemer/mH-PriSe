#!/bin/bash
# Start
# buggy network manager workaround
sudo nmcli radio wifi off
sudo rfkill unblock wlan
# Configure IP address for WLAN
sudo ifconfig wlan0 10.0.0.1/24 up
# Start DHCP/DNS server
#sudo dnsmasq -C /etc/dnsmasq.conf -H /etc/fakehosts.conf -d
sudo service dnsmasq restart
# Enable routing
sudo sysctl net.ipv4.ip_forward=1
# Enable NAT
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
# route traffic through MITMproxy
sudo iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 443 -j REDIRECT --to-port 8080
sudo iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 80 -j REDIRECT --to-port 8080
# Run access point daemon
sudo hostapd /etc/hostapd.conf
# Stop
# Disable NAT
sudo iptables -D POSTROUTING -t nat -o eth0 -j MASQUERADE
# Delete routing rules for mitmproxy
sudo iptables -t nat -D PREROUTING -i wlan0 -p tcp --dport 443 -j REDIRECT --to-port 8080
sudo iptables -t nat -D PREROUTING -i wlan0 -p tcp --dport 80 -j REDIRECT --to-port 8080
# Disable routing
sudo sysctl net.ipv4.ip_forward=0
# Disable DHCP/DNS server
sudo service dnsmasq stop
sudo service hostapd stop

