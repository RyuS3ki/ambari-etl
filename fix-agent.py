#!/usr/bin/env python

"""
Script en python para la configuracion inicial de los agentes de Ambari. Debe
lanzarse antes de la creacion del cluster y puede pasarse como argumento un
fichero de configuracion con booleanos que indiquen los servicios
que se van a instalar en el cliente concreto donde se lanza.
El codigo esta organizado en funciones segun los servicios para los que se van a
efectuar los cambios.
Debe ejecutarse siempre, ya que hay servicios genericos que deben prepararse
siempre.
"""

import os
import subprocess
import sys
import getopt
import errno
import shutils

#Funciones genericas para atomizar tareas
def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            try:
                shutil.copy(src, dest)
            except OSError as e:
                print('File not copied. Error: %s' % e)

        else:
            print('Directory not copied. Error: %s' % e)

def HDFS():
    copy('/usr/hdp', 'var/bigdata')
    os.rename('/usr/hdp', '/usr/hdp-orig')
    os.symlink('/var/bigdata/hdp', '/usr/hdp')

#def Yarn():

#def MapReduce():

#def Tez():

#def Hive():

#def HBase():

#def Pig():

#def ZooKeeper():

#def AmbariMetrics():

#def Spark():

#DataNode, NameNode, NodeManager
def Generic():
    HDFS()

def all_services():
    Generic()
    # HDFS()
    # Yarn()
    # MapReduce()
    # Tez()
    # Hive()
    # HBase()
    # Pig()
    # ZooKeeper()
    # AmbariMetrics()
    # Spark()

def selector():
    yarn = Config.getboolean("Services", "Yarn")
    mreduce = Config.getboolean("Services", "MapReduce")
    tez = Config.getboolean("Services", "Tez")
    hive = Config.getboolean("Services", "Hive")
    hbase = Config.getboolean("Services", "HBase")
    pig = Config.getboolean("Services", "Pig")
    zkeeper = Config.getboolean("Services", "ZooKeeper")
    ams = Config.getboolean("Services", "AmbariMetrics")
    spark = Config.getboolean("Services", "Spark")



def usage():
  print "\nThis is the usage function\n"
  print 'Usage: '+sys.argv[0]+' -[option]'
  print '-a:                        All services are configured'
  print '-s path/to/file.ini:       You must specify a config file with a list of services'
  print '-h:                        This help is printed'

#Codigo para leer argumentos
def main(argv):
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ahs:', ['all', 'help', 'services='])
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
            selector(confile)
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
