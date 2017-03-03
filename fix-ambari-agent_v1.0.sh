#!/bin/bash

mount -o remount,rw /usr

#cd /var/bigdata

	if [ -d /var/bigdata/ambari-etl ]
	then
		git clone https://github.com/ryus3ki/ambari-etl.git
	fi

	if [ ! -d /var/bigdata/servicios ]
	then
		mkdir /var/bigdata/servicios
	fi


	if [ ! -d /var/bigdata/servicios/hdp ]
	then
		cp -a /usr/hdp /var/bigdata/servicios/hdp
		mv /usr/hdp /usr/hdp-orig
		ln -s /var/bigdata/hdp/ /usr/hdp
	fi
	
			
mount -o remount,ro /usr
