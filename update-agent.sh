#!/bin/sh

ambari-agent stop

mount -o remount,rw /usr
dpkg -i /usr/dist/ambari/ambari-packages/ambari-agent*
mount -o remount,ro /usr
