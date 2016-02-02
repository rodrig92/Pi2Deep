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
import RPi.GPIO as GPIO                                                    #import RPi.GPIO module  

GPIO.setmode(GPIO.BCM)                                                     #seleccionamos BCM o BOARD  
GPIO.setup(17, GPIO.IN)                                                    #establecemos el pin GPIO17 como input   
   
try:
        camera = picamera.PiCamera()
        if len(sys.argv) == 2:
                camera.resolution = (int(sys.argv[1]), int(sys.argv[1]))   #caso de pasarle un tamanio por argumento
        elif len(sys.argv) == 3:
                camera.resolution = (int(sys.argv[1]), int(sys.argv[2]))   #caso de pasarle los tamanios por argumento
        else:
                camera.resolution = (600, 600)                             #tamanio por defecto de la imagen
  
        while True:                                                        #bucle para la espera de pulsar el boton 
                if (GPIO.input(17) == 1):
                        print "captura"
                        name = str(camera.resolution)
                        name = str('img'+name+'.jpg')                      #asignacion del nombre de la imagen

                        camera.capture(name)                               #captura

                        time.sleep(2)                                      #Tiempo para que saque la foto

                        ejecutar = ['./jpcnn','-i',name,'-n','../networks/jetpac.ntwk','-t','-m','s','-d']     #lista de parametros para la ejecucion del reconocimiento

                        call(ejecutar)                                     #ejecucion del reconocimiento

                        time.sleep(2)                                      #retardo final
 
                        call(['rm', name])                                 #borramos la foto resultado   

except KeyboardInterrupt:                                                  #CTRL+C para interrumpir  
        GPIO.cleanup()                                                     #reset de los puertos GPIO usados  
        print "Cerrado correctamente"
