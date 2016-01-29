#!/usr/bin/python
###############################################################
###   Autor:       Rodrigo Colombo Vlaeminch                ###
###   Universidad: Universidad de La Laguna                 ###
###   Descripcion: Script de enlace entre el programa de    ### 
###                reconocimiento de imagenes realizado     ###
###                por Pete Warden y la captura de imagen   ###
###                de la Raspberry Pi 2.                    ###
###   Version:     V0.1                                     ###
###############################################################

import picamera
import time
import sys
from subprocess import call

camera = picamera.PiCamera()
time.sleep(7)                                                  #Retardo para poder sacar la foto

if len(sys.argv) == 2:
    camera.resolution = (int(sys.argv[1]), int(sys.argv[1]))   #caso de pasarle un tamaño por argumento
elif len(sys.argv) == 3:
   camera.resolution = (int(sys.argv[1]), int(sys.argv[2]))    #caso de pasarle los tamaños por argumento
else:
   camera.resolution = (600, 600)                              #tamaño por defecto de la imagen

name = str(camera.resolution)
name = str('img'+name+'.jpg')                                  #asignacion del nombre de la imagen

camera.capture(name)                                           #captura

time.sleep(2)                                                  #Tiempo para que saque la foto

ejecutar = ['./jpcnn','-i',name,'-n','../networks/jetpac.ntwk','-t','-m','s','-d']     #lista de parametros para la ejecución del reconocimiento

call(ejecutar)                                                 #ejecución del reconocimiento

time.sleep(2)                                                  #retardo final
 
call(['rm', name])                                             #borramos la foto resultado   
