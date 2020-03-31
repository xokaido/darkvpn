#!/bin/bash

ovpn=$(which openvpn 2>/dev/null)
[ -z "${ovpn}" ]  && { echo "Please install openvpn first!"; exit 2; }
[ "$UID" != "0" ] && { echo "Please run this script as user root!"; exit 1; }
cwd=$(pwd)
python generate.py
[ "$?" != "0" ] && exit $?

echo "Thank you for been here!"
exit
openvpn --config ${cwd}/configuration.conf \
        --auth-user-pass ${cwd}/auth \
        --writepid /var/run/openvpn.pid \
        --script-security 2 \
        --up ${cwd}/up.sh \
        --daemon 
