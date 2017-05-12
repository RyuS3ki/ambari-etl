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
        script = '/etc/network/client.sh'
        prefix = subprocess.check_output(script, shell=True)
        type = ('config-'+str(prefix)).strip()
        f_ip = open(type,'r')
        dir = f_ip.readline()
        ip_prefix = dir[7:19]
        ip = ip_prefix + addr
        f_addr.close()
        return ip


def read_hosts():
        os.chdir("/etc")
        ip = read_ip()
        hostname = read_hostname()
        f = open('hosts','a+')
        lines = f.readlines()
        for line in lines:
                if line.find(hostname)==-1:
                        found = 0
                else:
                        found = 1
        if found == 0:
                f.write("#IP publica del host para ambari\n")
                f.write(ip.strip() + " " + hostname)
        f.close()


read_hosts()
