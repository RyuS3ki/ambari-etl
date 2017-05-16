#!/usr/bin/env python

'''
Script en python para la configuracion inicial de los agentes de Ambari. Debe
lanzarse antes de la creacion del cluster y puede pasarse como argumento un
fichero de configuracion con booleanos que indiquen los servicios
que se van a instalar en el cliente concreto donde se lanza.
El codigo esta organizado en funciones segun los servicios para los que se van a
efectuar los cambios.
Debe ejecutarse siempre, ya que hay servicios genericos que deben prepararse
siempre.
'''

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

def Errors(err):
    subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
    if err == 300:
        print "Error 300: Please run this script in reset mode before continuing"

    elif err == 301:
        print "Error 301: Copy failed, try again"

    elif err == 302:
        print "Error 302: There's no original directory to copy from"

    elif err == 303:
        print "Error 303: Copy failed, try again"

    print "An error occurred, please contact the SysAdmin with this error"
    print "in: guru.it.uc3m.es"
    print "You can also see the error documentation in etl.it.uc3m.es"
    exit()

# Services

# Basic services needed to run a basic Hadoop instance
def HDFS():
    print "HDFS service fix starting"
    print "Running some checks..."

    orig_exists = os.path.exists('/usr/hdp')
    mvd_exists = os.path.exists('/usr/hdp-orig')
    dest_exists = os.path.exists('/var/bigdata/servicios/hdp')
    wrong_exists = os.path.exists('/var/bigdata/hdp')

    if dest_exists:
        print "Previous copy of 'hdp' exists..."

        if wrong_exists:
            print "Previous copy of 'hdp' in wrong directory exists..."
            subprocess.call(['rm', '-rf', '/var/bigdata/hdp'])
            print "Erased not needed copy of directory"

        if orig_exists:
            print "Original directory exists. Freeing space..."
            subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
            subprocess.call(['rm', '-rf', '/usr/hdp'])
            print "Creating symlink..."
            os.symlink('/var/bigdata/servicios/hdp', '/usr/hdp')
            subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
            print "Done!"

        if mvd_exists:
            print "Backup copy of 'hdp' exists... Not needed. Freeing space..."
            subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
            subprocess.call(['rm', '-rf', '/usr/hdp-orig'])
            subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
            print "Done!"

    else:
        print "Clean agent, starting changes..."
        if orig_exists:
            tam_orig = get_size('/usr/hdp')
            if tam_orig != 0:
                # copy('/usr/hdp', '/var/bigdata/servicios/hdp')
                subprocess.call(['cp', '-R', '/usr/hdp','/var/bigdata/servicios/hdp'])
                tam_dest = get_size('/var/bigdata/servicios/hdp')
                if tam_dest == tam_orig:
                    print "Freeing space..."
                    subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
                    subprocess.call(['rm', '-rf', '/usr/hdp'])
                    print "Creating symlink..."
                    os.symlink('/var/bigdata/servicios/hdp', '/usr/hdp')
                    subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
                    print "Done!"
                else:
                    subprocess.call(['rm', '-rf', '/var/bigdata/servicios/hdp']) #Nos aseguramos de que no quede una copia mal hecha
                    err = 301
                    Errors(err)

            else:
                err = 300
                Errors(err)

        else:
            print "Creating directory..."
            os.makedirs('/var/bigdata/servicios/hdp')
            print "Freeing space..."
            subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
            subprocess.call(['rm', '-rf', '/usr/hdp'])
            print "Creating symlink..."
            os.symlink('/var/bigdata/servicios/hdp', '/usr/hdp')
            subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
            print "Done!"


#def Yarn():

#def MapReduce():

#def Tez():

def Lib():
    print "Library fix starting"
    print "Running some checks..."

    # /usr/lib/ambari-agent

    orig_exists = os.path.exists('/usr/lib/ambari-agent')
    dest_exists = os.path.exists('/var/bigdata/servicios/lib/ambari-agent')

    if dest_exists:
        print "Previous copy of 'lib/ambari-agent' exists..."

        if orig_exists:
            print "Original directory exists. Freeing space..."
            subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
            print "Creating backup, please wait..."
            copy('/usr/lib/ambari-agent', '/var/bigdata/backup/lib/ambari-agent')
            subprocess.call(['rm', '-rf', '/usr/lib/ambari-agent'])
            print "Done!"
            print "Creating symlink..."
            os.symlink('/var/bigdata/servicios/lib/ambari-agent', '/usr/lib/ambari-agent')
            subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
            print "Done!"

        if not dest_exists:
            if orig_exists:
                copy('/usr/lib/ambari-agent', '/var/bigdata/servicios/lib/ambari-agent')
                tam_dest = get_size('/var/bigdata/servicios/lib/ambari-agent')
                tam_orig = get_size('/usr/lib/ambari-agent')
                if tam_orig == tam_dest:
                    subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
                    print "Creating backup, please wait..."
                    copy('/usr/lib/ambari-agent', '/var/bigdata/backup/lib/ambari-agent')
                    subprocess.call(['rm', '-rf', '/usr/lib/ambari-agent'])
                    print "Done!"
                    print "Creating symlink..."
                    os.symlink('/var/bigdata/servicios/lib/ambari-agent', '/usr/lib/ambari-agent')
                    subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
                    print "Done!"
                else:
                    subprocess.call(['rm', '-rf', '/var/bigdata/servicios/lib/ambari-agent']) #Nos aseguramos de que no quede una copia mal hecha
                    err = 303
                    Errors(err)

            else:
                err = 302
                Errors(err)


    # /usr/lib/ambari-agent.org

    orig_exists = os.path.exists('/usr/lib/ambari-agent.org')
    dest_exists = os.path.exists('/var/bigdata/servicios/lib/ambari-agent.org')

    if dest_exists:
        print "Previous copy of 'lib/ambari-agent' exists..."

        if orig_exists:
            print "Original directory exists. Freeing space..."
            subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
            print "Creating backup, please wait..."
            copy('/usr/lib/ambari-agent', '/var/bigdata/servicios/lib/ambari-agent.org')
            subprocess.call(['rm', '-rf', '/usr/lib/ambari-agent.org'])
            print "Done!"
            print "Creating symlink..."
            os.symlink('/var/bigdata/servicios/lib/ambari-agent', '/usr/lib/ambari-agent.org')
            subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
            print "Done!"

        if not dest_exists:
            if orig_exists:
                copy('/usr/lib/ambari-agent.org', '/var/bigdata/servicios/lib/ambari-agent')
                tam_dest = get_size('/var/bigdata/servicios/lib/ambari-agent')
                tam_orig = get_size('/usr/lib/ambari-agent.org')
                if tam_orig == tam_dest:
                    subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
                    print "Creating backup, please wait..."
                    copy('/usr/lib/ambari-agent.org', '/var/bigdata/servicios/lib/ambari-agent.org')
                    subprocess.call(['rm', '-rf', '/usr/lib/ambari-agent.org'])
                    print "Done!"
                    print "Creating symlink..."
                    os.symlink('/var/bigdata/servicios/lib/ambari-agent', '/usr/lib/ambari-agent.org')
                    subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
                    print "Done!"
                else:
                    subprocess.call(['rm', '-rf', '/var/bigdata/servicios/lib/ambari-agent']) #Nos aseguramos de que no quede una copia mal hecha
                    err = 303
                    Errors(err)

            else:
                err = 302
                Errors(err)


    # /usr/lib/ambari-metrics-collector

    orig_exists = os.path.exists('/usr/lib/ambari-metrics-collector')
    dest_exists = os.path.exists('/var/bigdata/servicios/lib/ambari-agent')

    if dest_exists:
        print "Previous copy of 'lib/ambari-agent' exists..."

        if orig_exists:
            print "Original directory exists. Freeing space..."
            subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
            print "Creating backup, please wait..."
            copy('/usr/lib/ambari-metrics-collector', '/var/bigdata/servicios/lib/ambari-metrics-collector')
            subprocess.call(['rm', '-rf', '/usr/lib/ambari-metrics-collector'])
            print "Done!"
            print "Creating symlink..."
            os.symlink('/var/bigdata/servicios/lib/ambari-agent', '/usr/lib/ambari-metrics-collector')
            subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
            print "Done!"

        if not dest_exists:
            if orig_exists:
                copy('/usr/lib/ambari-metrics-collector', '/var/bigdata/servicios/lib/ambari-agent')
                tam_dest = get_size('/var/bigdata/servicios/lib/ambari-agent')
                tam_orig = get_size('/usr/lib/ambari-metrics-collector')
                if tam_orig == tam_dest:
                    subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
                    print "Creating backup, please wait..."
                    copy('/usr/lib/ambari-metrics-collector', '/var/bigdata/servicios/lib/ambari-metrics-collector')
                    subprocess.call(['rm', '-rf', '/usr/lib/ambari-metrics-collector'])
                    print "Done!"
                    print "Creating symlink..."
                    os.symlink('/var/bigdata/servicios/lib/ambari-agent', '/usr/lib/ambari-metrics-collector')
                    subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
                    print "Done!"
                else:
                    subprocess.call(['rm', '-rf', '/var/bigdata/servicios/lib/ambari-agent']) #Nos aseguramos de que no quede una copia mal hecha
                    err = 303
                    Errors(err)

            else:
                err = 302
                Errors(err)


    # /usr/lib/ambari-metrics-grafana

    orig_exists = os.path.exists('/usr/lib/ambari-metrics-grafana')
    dest_exists = os.path.exists('/var/bigdata/servicios/lib/ambari-agent')

    if dest_exists:
        print "Previous copy of 'lib/ambari-agent' exists..."

        if orig_exists:
            print "Original directory exists. Freeing space..."
            subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
            print "Creating backup, please wait..."
            copy('/usr/lib/ambari-metrics-grafana', '/var/bigdata/servicios/lib/ambari-metrics-grafana')
            subprocess.call(['rm', '-rf', '/usr/lib/ambari-metrics-grafana'])
            print "Done!"
            print "Creating symlink..."
            os.symlink('/var/bigdata/servicios/lib/ambari-agent', '/usr/lib/ambari-metrics-grafana')
            subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
            print "Done!"

        if not dest_exists:
            if orig_exists:
                copy('/usr/lib/ambari-metrics-grafana', '/var/bigdata/servicios/lib/ambari-agent')
                tam_dest = get_size('/var/bigdata/servicios/lib/ambari-agent')
                tam_orig = get_size('/usr/lib/ambari-metrics-grafana')
                if tam_orig == tam_dest:
                    subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
                    print "Creating backup, please wait..."
                    copy('/usr/lib/ambari-metrics-grafana', '/var/bigdata/servicios/lib/ambari-metrics-grafana')
                    subprocess.call(['rm', '-rf', '/usr/lib/ambari-metrics-grafana'])
                    print "Done!"
                    print "Creating symlink..."
                    os.symlink('/var/bigdata/servicios/lib/ambari-agent', '/usr/lib/ambari-metrics-grafana')
                    subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
                    print "Done!"
                else:
                    subprocess.call(['rm', '-rf', '/var/bigdata/servicios/lib/ambari-agent']) #Nos aseguramos de que no quede una copia mal hecha
                    err = 303
                    Errors(err)

            else:
                err = 302
                Errors(err)


    # /usr/lib/ambari-metrics-hadoop-sink

    orig_exists = os.path.exists('/usr/lib/ambari-metrics-hadoop-sink')
    dest_exists = os.path.exists('/var/bigdata/servicios/lib/ambari-agent')

    if dest_exists:
        print "Previous copy of 'lib/ambari-agent' exists..."

        if orig_exists:
            print "Original directory exists. Freeing space..."
            subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
            print "Creating backup, please wait..."
            copy('/usr/lib/ambari-metrics-hadoop-sink', '/var/bigdata/servicios/lib/ambari-metrics-hadoop-sink')
            subprocess.call(['rm', '-rf', '/usr/lib/ambari-metrics-hadoop-sink'])
            print "Done!"
            print "Creating symlink..."
            os.symlink('/var/bigdata/servicios/lib/ambari-agent', '/usr/lib/ambari-metrics-hadoop-sink')
            subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
            print "Done!"

        if not dest_exists:
            if orig_exists:
                copy('/usr/lib/ambari-metrics-hadoop-sink', '/var/bigdata/servicios/lib/ambari-agent')
                tam_dest = get_size('/var/bigdata/servicios/lib/ambari-agent')
                tam_orig = get_size('/usr/lib/ambari-metrics-hadoop-sink')
                if tam_orig == tam_dest:
                    subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
                    print "Creating backup, please wait..."
                    copy('/usr/lib/ambari-metrics-hadoop-sink', '/var/bigdata/servicios/lib/ambari-metrics-hadoop-sink')
                    subprocess.call(['rm', '-rf', '/usr/lib/ambari-metrics-hadoop-sink'])
                    print "Done!"
                    print "Creating symlink..."
                    os.symlink('/var/bigdata/servicios/lib/ambari-agent', '/usr/lib/ambari-metrics-hadoop-sink')
                    subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
                    print "Done!"
                else:
                    subprocess.call(['rm', '-rf', '/var/bigdata/servicios/lib/ambari-agent']) #Nos aseguramos de que no quede una copia mal hecha
                    err = 303
                    Errors(err)

            else:
                err = 302
                Errors(err)


    # /usr/lib/ambari-metrics-kafka-sink

    orig_exists = os.path.exists('/usr/lib/ambari-metrics-kafka-sink')
    dest_exists = os.path.exists('/var/bigdata/servicios/lib/ambari-agent')

    if dest_exists:
        print "Previous copy of 'lib/ambari-agent' exists..."

        if orig_exists:
            print "Original directory exists. Freeing space..."
            subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
            print "Creating backup, please wait..."
            copy('/usr/lib/ambari-metrics-kafka-sink', '/var/bigdata/servicios/lib/ambari-metrics-kafka-sink')
            subprocess.call(['rm', '-rf', '/usr/lib/ambari-metrics-kafka-sink'])
            print "Done!"
            print "Creating symlink..."
            os.symlink('/var/bigdata/servicios/lib/ambari-agent', '/usr/lib/ambari-metrics-kafka-sink')
            subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
            print "Done!"

        if not dest_exists:
            if orig_exists:
                copy('/usr/lib/ambari-metrics-kafka-sink', '/var/bigdata/servicios/lib/ambari-agent')
                tam_dest = get_size('/var/bigdata/servicios/lib/ambari-agent')
                tam_orig = get_size('/usr/lib/ambari-metrics-kafka-sink')
                if tam_orig == tam_dest:
                    subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
                    print "Creating backup, please wait..."
                    copy('/usr/lib/ambari-metrics-kafka-sink', '/var/bigdata/servicios/lib/ambari-metrics-kafka-sink')
                    subprocess.call(['rm', '-rf', '/usr/lib/ambari-metrics-kafka-sink'])
                    print "Done!"
                    print "Creating symlink..."
                    os.symlink('/var/bigdata/servicios/lib/ambari-agent', '/usr/lib/ambari-metrics-kafka-sink')
                    subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
                    print "Done!"
                else:
                    subprocess.call(['rm', '-rf', '/var/bigdata/servicios/lib/ambari-agent']) #Nos aseguramos de que no quede una copia mal hecha
                    err = 303
                    Errors(err)

            else:
                err = 302
                Errors(err)


    # /usr/lib/ambari-server

    orig_exists = os.path.exists('/usr/lib/ambari-server')
    dest_exists = os.path.exists('/var/bigdata/servicios/lib/ambari-agent')

    if dest_exists:
        print "Previous copy of 'lib/ambari-agent' exists..."

        if orig_exists:
            print "Original directory exists. Freeing space..."
            subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
            print "Creating backup, please wait..."
            copy('/usr/lib/ambari-server', '/var/bigdata/servicios/lib/ambari-server')
            subprocess.call(['rm', '-rf', '/usr/lib/ambari-server'])
            print "Done!"
            print "Creating symlink..."
            os.symlink('/var/bigdata/servicios/lib/ambari-agent', '/usr/lib/ambari-server')
            subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
            print "Done!"

        if not dest_exists:
            if orig_exists:
                copy('/usr/lib/ambari-server', '/var/bigdata/servicios/lib/ambari-agent')
                tam_dest = get_size('/var/bigdata/servicios/lib/ambari-agent')
                tam_orig = get_size('/usr/lib/ambari-server')
                if tam_orig == tam_dest:
                    subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
                    print "Creating backup, please wait..."
                    copy('/usr/lib/ambari-server', '/var/bigdata/servicios/lib/ambari-server')
                    subprocess.call(['rm', '-rf', '/usr/lib/ambari-server'])
                    print "Done!"
                    print "Creating symlink..."
                    os.symlink('/var/bigdata/servicios/lib/ambari-agent', '/usr/lib/ambari-server')
                    subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
                    print "Done!"
                else:
                    subprocess.call(['rm', '-rf', '/var/bigdata/servicios/lib/ambari-agent']) #Nos aseguramos de que no quede una copia mal hecha
                    err = 303
                    Errors(err)

            else:
                err = 302
                Errors(err)


    # /usr/lib/ambari-server-backups

    orig_exists = os.path.exists('/usr/lib/ambari-server-backups')
    dest_exists = os.path.exists('/var/bigdata/servicios/lib/ambari-agent')

    if dest_exists:
        print "Previous copy of 'lib/ambari-agent' exists..."

        if orig_exists:
            print "Original directory exists. Freeing space..."
            subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
            print "Creating backup, please wait..."
            copy('/usr/lib/ambari-server-backups', '/var/bigdata/servicios/lib/ambari-server-backups')
            subprocess.call(['rm', '-rf', '/usr/lib/ambari-server-backups'])
            print "Done!"
            print "Creating symlink..."
            os.symlink('/var/bigdata/servicios/lib/ambari-agent', '/usr/lib/ambari-server-backups')
            subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
            print "Done!"

        if not dest_exists:
            if orig_exists:
                copy('/usr/lib/ambari-server-backups', '/var/bigdata/servicios/lib/ambari-agent')
                tam_dest = get_size('/var/bigdata/servicios/lib/ambari-agent')
                tam_orig = get_size('/usr/lib/ambari-server-backups')
                if tam_orig == tam_dest:
                    subprocess.call(['mount', '-o', 'remount,rw', '/usr'])
                    print "Creating backup, please wait..."
                    copy('/usr/lib/ambari-server-backups', '/var/bigdata/servicios/lib/ambari-server-backups')
                    subprocess.call(['rm', '-rf', '/usr/lib/ambari-server-backups'])
                    print "Done!"
                    print "Creating symlink..."
                    os.symlink('/var/bigdata/servicios/lib/ambari-agent', '/usr/lib/ambari-agent')
                    subprocess.call(['mount', '-o', 'remount,ro', '/usr'])
                    print "Done!"
                else:
                    subprocess.call(['rm', '-rf', '/var/bigdata/servicios/lib/ambari-agent']) #Nos aseguramos de que no quede una copia mal hecha
                    err = 303
                    Errors(err)

            else:
                err = 302
                Errors(err)


#def HBase():

#def Pig():

#def ZooKeeper():

#def AmbariMetrics():

#def Spark():

def Generic():
    HDFS()
    Lib()
    # HBase()
    return 0

def all_services():
    if Generic() == 1:
        print "Continuing with services..."
    else:
        print "Generic changes done!"
    # Yarn()
    # MapReduce()
    # Tez()
    # Pig()
    # ZooKeeper()
    # AmbariMetrics()
    # Spark()

# Function that reads config file and sets services to be changed
def selector(confile):
    Config = ConfigParser.ConfigParser()
    Config.read(confile)

    yarn = Config.getboolean('Services', 'Yarn')
    print "Yarn service has been set to: %r" % (yarn)
    mreduce = Config.getboolean('Services', 'MapReduce')
    print "MapReduce service has been set to: %r" % (mreduce)
    tez = Config.getboolean('Services', 'Tez')
    print "Tez service has been set to: %r" % (tez)
    hive = Config.getboolean('Services', 'Hive')
    print "Hive service has been set to: %r" % (hive)
    hbase = Config.getboolean('Services', 'HBase')
    print "HBase service has been set to: %r" % (hbase)
    pig = Config.getboolean('Services', 'Pig')
    print "Pig service has been set to: %r" % (pig)
    zkeeper = Config.getboolean('Services', 'ZooKeeper')
    print "ZooKeeper service has been set to: %r" % (zkeeper)
    ams = Config.getboolean('Services', 'AmbariMetrics')
    print "Ambari Metrics service has been set to: %r" % (ams)
    spark = Config.getboolean('Services', 'Spark')
    print "Spark service has been set to: %r" % (spark)

    if Generic() == 1:
        print "Continuing with services..."
    else:
        print "Generic changes done!"


'''Ejecutamos ahora los servicios seleccionados en el archivo de
    configuracion

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

# Function that resets all client configuration about Ambari (this is the
# desperate method for "fixing" things)
def Reset():
    script = '/var/bigdata/ambari-etl/agent-reset.sh'
    print "Resetting agent..."
    subprocess.check_output(script, shell=True)
    print "Done! Remember to run this script again before connecting to the server"

def usage():
  print "\nThis is the usage function\n"
  print 'Usage: '+sys.argv[0]+' -[option]'
  print '-a                 :       All services are configured'
  print '-s path/to/file.ini:       You must specify a config file with a list of services'
  print '-r                 :       Reset the agent to default values (configuration loss)'
  print '-h                 :       This help is printed'


def main(argv):
    os.system('clear')
    print "AMBARI ETL SCRIPT\n"
    #Codigo para leer argumentos
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ahrs:', ['all', 'help', 'reset', 'services='])
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
            if cont == 'y':
                all_services()
            elif cont == 'n':
                print "Execute this script again using the desired parameters"
                usage()
                sys.exit(2)
            else:
                print "Wrong usage"
                print "Exiting..."
                usage()
                sys.exit(2)
        elif opt in ('-r', '--reset'):
            print "You're about to reset all previous configuration in this client"
            print "If you have any problem try first contacting the SysAdmins, "
            print "you can do so in: guru.it.uc3m.es"
            print "If you choose to continue, remember Ambari won't work until you"
            print "run this script again."
            print "Remember: Great power comes with great responsibility"
            c = raw_input("Are you sure? (y/n):")
            if c == 'y':
                Reset()
            elif c == 'n':
                print "Exiting..."
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
