#!/bin/sh

mount -o remount,rw /usr

ambari-agent stop
ambari-agent reset
rm -rf /var/lib/ambari-agent
rm -rf /var/run/ambari-agent
rm -rf /usr/lib/ambari-agent
rm -rf /usr/lib/python2.6/site-packages/ambari-agent

dpkg --purge ambari-agent

mount -o remount,ro /usr
