#!/bin/sh

ambari-agent stop

mount -o remount,rw /usr
dpkg -i /usr/dist/ambari/ambari-packages/ambari-agent*
mkdir /usr/hdp/current
ln -sfn /usr/local/hadoop-2.7.1.2.3.4.0-3347 /usr/hdp/current/hadoop-client
mount -o remount,ro /usr

ambari-agent stop
sh /var/bigdata/ambari-etl/agent-init-config_v1.0.sh
ambari-agent start
