#!/bin/sh
set -e

opkg update
opkg install python3-light python3-codecs python3-email

chmod +x co2monitor-sender.py
chmod +x co2monitor-sender.init

cp co2monitor-sender.py /usr/bin
cp co2monitor-sender.init /etc/init.d/
cp co2monitor_sender /etc/config/
/etc/init.d/co2monitor-sender.init enable
/etc/init.d/co2monitor-sender.init enabled && echo "The service is now enabled."
