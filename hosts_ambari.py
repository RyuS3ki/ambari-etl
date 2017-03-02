#!/usr/bin/python

import os
import subprocess

def read_hostname():
	os.chdir("/etc")
	f_hostname = open('hostname','r')
	hostname = f_hostname.read()
	f_hostname.close()
	return hostname		

def read_ip():
	os.chdir("/etc/network")
	f_addr = open('ADDRESS','r')
	addr = f_addr.read()
	
	prefix = subprocess.call('client.sh', shell=True)
	print("Prefix is: " + prefix)
	type = 'config-'+prefix
	f_ip = open(type,'r')
	dir = f_ip.readline()
	ip_prefix = dir.replace(' ', '')[:-8].upper().strip()
	print("Prefix is: " + prefix)
	ip = ip_prefix + addr
	print("IP is: ")
	f_addr.close()
	return ip
	

def read_hosts():
	os.chdir("/etc")
	f = open('hosts','a+')
	lines = f.readlines()
	hostname = read_hostname()
	for line in lines:
		if line.find(hostname)!=-1:
			found = 0
		else:
			found = 1
	if found == 0:
		hostname = read_hostname()
		ip = read_ip()
		f.write(hostname +"\t"+ip+"\n")
	f.close()
	
print("Executing")
read_hosts()
print("Done")
