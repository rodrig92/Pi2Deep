#!/usr/bin/python
###############################################################
###   Autor:       Rodrigo Colombo Vlaeminch                ###
###   Universidad: Universidad de La Laguna                 ###
###   Descripcion: Script de enlace entre el programa de    ### 
###                reconocimiento de imagenes realizado     ###
###                por Pete Warden y la captura de imagen   ###
###                de la Raspberry Pi 2.                    ###
###   Version:     V3.1                                     ###
###############################################################

import picamera
import time
import sys
from subprocess import call
import RPi.GPIO as GPIO                                                                    #import RPi.GPIO module  

GPIO.setmode(GPIO.BCM)                                                                     #choose BCM or BOARD  
GPIO.setup(23, GPIO.IN)                                                                    #set GPIO23 as an input   
GPIO.setup(18, GPIO.IN)                                                                    #set GPIO18 as an input 

def envia_foto (foto):
    if len (foto) > 0:
        ejecutar = ['fbi','-d','/dev/fb1','-T','1','-noverbose','-a',foto]
        call (ejecutar)
    else:
        print "No hay foto"

def capturar ():
    camera = picamera.PiCamera()
    camera.resolution = (320, 240)                                     #tamanio por defecto de la imagen
    name = str (camera.resolution)
    name = str ('img'+name+'.jpg')                                      #asignacion del nombre de la imagen
    camera.capture (name)                                               #captura
    envia_foto (name)
    camera.close () 
    return name
   
def resultado (fichero):
    ejecutar = ['sort','-n','-k2','-r',fichero,'-o','log2.txt']              #ordenamos el resultado para que salga la mayor probabilidad primero
    call (ejecutar)
    res = open ('log2.txt', 'r')                                        #abrimos fichero resultado
    linea = res.readline ()                                             #leemos la primera linea
    linea = linea.split ()                                              #separamos la linea en una lista de palabras
    if float (linea[0]) > 0.05:
       res = "Resultado:" + str (linea[1])
       envia_foto (res)                                           #enviamos el resultado a la pantalla
       time.sleep (1.5)
    else:
       envia_foto ("imposible reconocer")

def reconoce (foto):
    if len (foto) > 0:
        ejecutar = ['./jpcnn','-i',foto,'-n','../networks/jetpac.ntwk','-t','-m','s','-d']
        outfile = open ('log.txt', 'w')
        errfile = open ('/dev/null', 'w')
        call (ejecutar,stdout = outfile,stderr = errfile)                       #ejecucion del reconocimiento
        outfile.close ()
        errfile.close ()
        resultado ('log.txt')
    else:
        print "error en reconocimiento"
       
def salir (foto):
    envia_foto ("Fin del programa")
    ejecutar = ['rm','-r',foto,'log.txt','log2.txt']
    call (ejecutar)
    GPIO.cleanup ()                                                     #reset de los puertos GPIO usados  
    print "Bye bye"

fotos = {1: 'f_menu/Capturar.jpg',
         2: 'f_menu/Previsualizar.jpg',
         3: 'f_menu/Reconocer.jpg',
         0: 'f_menu/Salir.jpg',
         10: 'img(320, 240).jpg'  
       }

def op1 ():
    envia_foto (capturar ())
    time.sleep (3)
def op2 ():
    envia_foto (fotos[10])
    time.sleep (4)
def op3 ():
    reconoce (fotos[10])
    time.sleep (1)
def op0 ():
    salir (fotos[10])
    exit (0)
    
opcion_menu = {1: op1,
               2: op2,
               3: op3,
               0: op0,
              }
    
contador_menu = 1
envia_foto (fotos[1])

try:
    while True:    
        if (GPIO.input (23) == 0):                   #boton de desplazamiento de menu
            contador_menu = int ((contador_menu + 1) % 4)
            envia_foto (fotos[contador_menu])
            time.sleep (0.5)
        if (GPIO.input (18) == 0):                   #boton de accion
            opcion_menu[contador_menu] ()
            contador_menu = 1
            envia_foto (fotos[contador_menu]) 
            time.sleep (0.5)
           
except KeyboardInterrupt:
    salir (fotos[10])
