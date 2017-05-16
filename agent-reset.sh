#!/bin/sh

mount -o remount,rw /usr

ambari-agent stop
ambari-agent reset

echo "Cleaning directories..."

rm -rf /usr/hdp
rm -rf /var/bigdata/servicios
rm -rf /var/bigdata/backup

echo "Restoring symlinks..."

mkdir /usr/hdp
mkdir /usr/hdp/current
ln -sfn /usr/local/hadoop-2.7.0 /usr/hdp/current/hadoop-client
sh /var/bigdata/ambari-etl/agent-init-config_v1.0.sh

mount -o remount,ro /usr
