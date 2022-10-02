#!/usr/bin/bash
if [ $(whoami) != 'root' ]; then
	echo "This script requires root permission."
    exit 126
fi
if [ $# -lt 1 ]; then
    echo "Usage: install.sh <servicename> where servicename is of [tempcontrol, blind]."
    exit 2
fi
systemctl stop $1.service
cp ./$1.service /etc/systemd/system/$1.service
systemctl start $1.service