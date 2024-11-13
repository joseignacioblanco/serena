#! /usr/bin/python3
# Este es el shebang para que se ejecute como script de python.
# no puede haber nada mas en a primera linea sino no anda.


#------------------------------ PROYECTO SERENA 9/NOV/2024 --------------------------
# AUTOR: JOSE BLANCO.
# CONTACTO: tombonia@gmail.com
# Descripción: Implementa un control de acceso en una Raspberry pi para un consorio.
# Lenguaje preferido: Python.
#------------------------------------------------------------------------------------


# Aqui pone todas las bibliotecas de python que va a usar.

import RPi.GPIO as GPIO # El as ese le da un alias al modulo: para poner GPIO.setmode y no  RPi.GPIO.setmode
from mfrc522 import SimpleMFRC522 # Maneja el modulo rfid.
import time # para manejar cosas que tienen que ver con horarios, dias, tiempo, etc
from implement import *
from app import *

#------------------------------------------------------------------------------------------

lector_1 = SimpleMFRC522() # Crea una instancia de la clase que maneja la placa RC522.
RELAY_1_PIN = 5 #Constante simbolica, despues debo ponerla en un header o algo asi..
SD_FILE_PATH = "/home/pi/Documents/serena/autorized_cards.txt"# Ruta donde se almacena el archivo en la Raspberry Pi (este es el archivo donde estan los id  de las tarjetas con la info de cada usuario: ver como vincular cada id con persona. va tener que parsear el id o usar un archivo binario y no txt)

# Funcion principal de entrada a la aplicación

def main():
    
    setup()
    
    loop()
  
            
#esto es lo del tema que paiton necesita un punto de entrada por mein y no se por que se lo indica asi.
if __name__ == "__main__":
    main()