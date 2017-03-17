#!/bin/python

""""
Script en python para la configuración inicial de los agentes de Ambari. Debe
lanzarse antes de la creación del cluster y cogerá como argumentos los servicios
que se van a instalar en el cliente concreto donde se lanza.
El código está organizado en funciones según los servicios para los que se van a
efectuar los cambios.
""""

import os
import subprocess
import sys
import getopt

#Código para leer argumentos

try:
    opts, args = getopt.getopt(sys.argv[1:], 's:h', ['', 'services=', 'help'])
except getopt.GetoptError:
    usage()
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(2)
    elif opt in ('-s', '--services'):
        servicesList = ast.literal_eval(sys.argv[2])
        all_arg = 0
    else:
        print 'Se harán cambios para todos los servicios'
        cont = input("¿Está seguro? (y/n):")
        if cont == y:
            all_arg = 1
        elif cont == n:
            all_arg = 0
            print 'Lance otra vez el fix e introduzca los parámetros deseados'
            usage()
            sys.exit(2)
        else:
            print 'Valor erróneo, debe introducir y/n'
            usage()
            sys.exit(2)

def HCat():
