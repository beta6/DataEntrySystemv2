#!/bin/bash 
service rsyslog start
service mysql start
service redis-server restart
/etc/init.d/supervisor force-reload
service supervisor start
echo "starting... please wait..."
sleep 30s
supervisorctl restart all
supervisorctl status all
echo "DES started and ready!"
echo "port 443 (https) in localhost ready for use"
echo "paste this url in your browser"
echo "https://localhost"
bash
