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
import shutil
import ConfigParser

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

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

#Servicios
def HDFS():
    subprocess.call(["mount", "-o", "remount,rw", "/usr"])
    print "Installing HDFS in the system..."
    copy('/usr/hdp', '/var/bigdata')
    os.rename('/usr/hdp', '/usr/hdp-orig')
    tam_orig = get_size('/usr/hdp-orig')
    os.symlink('/var/bigdata/hdp', '/usr/hdp')
    tam_bd = get_size('/var/bigdata/hdp')
    if tam_bd == tam_orig:
        subprocess.call(["mount", "-o", "remount,ro", "/usr"])
        print "Done!"
    else:
        print "An error occurred, please contact the SysAdmin"



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
    print "Preparing changes..."
    if os.path.exists("/var/bigdata/hdp"):
        print "Changes have been applied before, if you continue previous changes can be overwritten and some may fail"
        #print "It is recommended that you use the option -d to start over"
        cont1 = raw_input("Do you still want to apply config file changes? [y/n]:")
        if cont1 == "y":
            print "(Changes based on HDFS will be skipped)"
            return 1
        elif cont1 == "n":
            print "Exiting..."
            exit()
        else:
            print "Not a valid answer"
            print "Exiting..."
            exit()

    else:
        HDFS()
        return 0

def all_services():
    if Generic() == 1:
        print "Continuing with services..."
    else:
        print "Generic changes done!"
    # Yarn()
    # MapReduce()
    # Tez()
    # Hive()
    # HBase()
    # Pig()
    # ZooKeeper()
    # AmbariMetrics()
    # Spark()

def selector(confile):
    #global conf_changes = False
    #Inicializamos el Parser y abrimos el archivo de configuracion
    var = 0
    Config = ConfigParser.ConfigParser()
    Config.read(confile)

    yarn = Config.getboolean("Services", "Yarn")
    print "El servicio Yarn esta: %r" % (yarn)
    mreduce = Config.getboolean("Services", "MapReduce")
    print "El servicio Yarn esta: %r" % (yarn)
    tez = Config.getboolean("Services", "Tez")
    print "El servicio Yarn esta: %r" % (yarn)
    hive = Config.getboolean("Services", "Hive")
    print "El servicio Yarn esta: %r" % (yarn)
    hbase = Config.getboolean("Services", "HBase")
    print "El servicio Yarn esta: %r" % (yarn)
    pig = Config.getboolean("Services", "Pig")
    print "El servicio Yarn esta: %r" % (yarn)
    zkeeper = Config.getboolean("Services", "ZooKeeper")
    print "El servicio Yarn esta: %r" % (yarn)
    ams = Config.getboolean("Services", "AmbariMetrics")
    print "El servicio Yarn esta: %r" % (yarn)
    spark = Config.getboolean("Services", "Spark")
    print "El servicio Yarn esta: %r" % (yarn)

    '''Esta funcion contiene lo minimo que podemos lanzar para tener una
    instancia de Hadoop, debe ejecutarse siempre que se utilice el fix'''

    if Generic() == 1:
        print "Continuing with services..."
    else:
        print "Generic changes done!"


    '''Ejecutamos ahora los servicios seleccionados en el archivo de
    configuracion'''
    '''
    if yarn == True:
        #Yarn()

    if mreduce == True:
        #MapReduce()

    if tez == True:
        #Tez()

    if hive == True:
        #Hive()

    if hbase == True:
        #HBase()

    if pig == True:
        #Pig()

    if zkeeper == True:
        #ZooKeeper()

    if ams == True:
        #AmbariMetrics()

    if spark == True:
        #Spark()
'''

def usage():
  print "\nThis is the usage function\n"
  print 'Usage: '+sys.argv[0]+' -[option]'
  print '-a                 :       All services are configured'
  print '-s path/to/file.ini:       You must specify a config file with a list of services'
  print '-h                 :       This help is printed'


def main(argv):
    os.system('clear')
    print "AMBARI ETL SCRIPT\n"
    #Codigo para leer argumentos
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
            print "Opening config file"
            confile = sys.argv[2]
            selector(confile)
        elif opt in ('-a', '--all'):
            print "This will make changes for all the services"
            cont = raw_input("Are you sure? (y/n):")
            if cont == "y":
                all_services()
            elif cont == "n":
                print "Execute this script again using the desired parameters"
                usage()
                sys.exit(2)
            else:
                print "Wrong usage"
                print "Exiting..."
                usage()
                sys.exit(2)
        else:
            usage()
            sys.exit(2)

#Ejecucion del main
if __name__ =='__main__':
    main(sys.argv[1:])
