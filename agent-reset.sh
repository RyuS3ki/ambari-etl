#!/bin/sh

mount -o remount,rw /usr

ambari-agent stop
ambari-agent reset

echo "Cleaning directories..."

rm -rf /var/lib/ambari-agent
rm -rf /var/run/ambari-agent
rm -rf /usr/lib/ambari-agent
rm -rf /usr/lib/python2.6/site-packages/ambari-agent
rm -rf /usr/hdp
rm -rf /var/bigdata/servicios
rm -rf /var/bigdata/backup
rm -rf /etc/ambari-agent

echo "Restoring symlinks..."

mkdir /usr/hdp
mkdir /usr/hdp/current
ln -sfn /usr/local/hadoop-2.7.1.2.3.4.0-3347 /usr/hdp/current/hadoop-client
sh /var/bigdata/ambari-etl/agent-init-config_v1.0.sh

mount -o remount,ro /usr
