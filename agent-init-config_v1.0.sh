#!/bin/sh

#Sustituimos la configuracion generica por la propia
cp /usr/dist/ambari/ambari-etl/ambari-agent.ini /etc/ambari-agent/conf/ambari-agent.ini

#Añadimos el equipo a /etc/hosts
python hosts_ambari.py
