#!/bin/sh

#Sustituimos la configuracion generica por la propia
cp /usr/dist/ambari/ambari-etl/ambari-agent.ini /etc/ambari-agent/conf/ambari-agent.ini

#Añadimos el equipo a /etc/hosts
<<<<<<< HEAD
python hosts_ambari.py
=======
python hosts-ambari.py
>>>>>>> fe81879b840e48ac997b4c1bf5a8b44025e2854d
