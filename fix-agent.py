#!/usr/bin/env python

"""
Script en python para la configuracion inicial de los agentes de Ambari. Debe
lanzarse antes de la creacion del cluster y cogera como argumentos los servicios
que se van a instalar en el cliente concreto donde se lanza.
El codigo esta organizado en funciones segun los servicios para los que se van a
efectuar los cambios.
"""

import os
import subprocess
import sys
import getopt

#DataNode, NameNode, NodeManager
#def Generic():    

#def HDFS():

#def Yarn():

#def MapReduce():

#def Tez():

#def Hive():

#def HBase():

#def Pig():

#def ZooKeeper():

#def AmbariMetrics():

#def Spark():

#def all_services():

def usage():
  print "\nThis is the usage function\n"
  print 'Usage: '+sys.argv[0]+' -[option]'
  print '-a:                        All services are configured'
  print '-s path/to/file.conf:      You must specify a config file with a list of services'
  print '-h:                        This help is printed'

#Codigo para leer argumentos
def main(argv):
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ahs:', ['all', 'services=', 'help'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-s', '--services'):
            print 'Abriendo archivo de configuracion'
            confile = sys.argv[2]
        elif opt in ('-a', '--all'):
            print 'Se haran cambios para todos los servicios'
            cont = raw_input("Esta seguro? (y/n):")
            if cont == "y":
                all_services()
            elif cont == "n":
                print 'Lance otra vez el fix e introduzca los parametros deseados'
                usage()
                sys.exit(2)
            else:
                print 'Valor erroneo, debe introducir y/n'
                usage()
                sys.exit(2)
        else:
            usage()
            sys.exit(2)

#Ejecucion del main
if __name__ =='__main__':
    main(sys.argv[1:])
