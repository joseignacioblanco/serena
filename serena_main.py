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

#------------------------------------------------------------------------------------------

lector_1 = SimpleMFRC522() # Crea una instancia de la clase que maneja la placa RC522.
RELAY_1_PIN = 5 #Constante simbolica, despues debo ponerla en un header o algo asi..
SD_FILE_PATH = "/home/pi/Documents/serena/autorized_cards.txt"# Ruta donde se almacena el archivo en la Raspberry Pi (este es el archivo donde estan los id  de las tarjetas con la info de cada usuario: ver como vincular cada id con persona. va tener que parsear el id o usar un archivo binario y no txt)

# Funcion principal de entrada a la aplicación

def main():
    
    setup()
    
    loop()

    #print("Sistema de Control de Acceso Iniciado.")
    '''while True:
        try:
            GPIO.setmode(GPIO.BOARD) # Configura el modo numeracion de placa.
            GPIO.setup(RELAY_1_PIN, GPIO.OUT) # configura el relé_pin como salida. esto debe ir al setup
            GPIO.output(RELAY_1_PIN, GPIO.LOW)  # Asegura que el relé comience apagado, deberia ser normal cerrado.
            
            #lee la tarjeta:

            print("Esperando una tarjeta...")
            card_id, text = lector_1.read() #asignacion multiple, a text nunca lo usa.
            card_id = str(card_id).strip() #strip le saca los espacios y str lo castea a estring
            print(f"Tarjeta leída: {card_id}") #print con formato.
            
            #se fija si esta autorizada

            if is_card_authorized(card_id):
                print("Acceso permitido.")
                activate_relay()  # Activar el relé para abrir la puerta
            else:
                print("Acceso denegado.")
                # Aquí puedes agregar lógica para alarmas, etc.

            time.sleep(1)  # Retardo para evitar lecturas múltiples rápidas

        except KeyboardInterrupt:
            print("\nSaliendo del sistema.")
            break
        finally:
            print("mondongo")
            GPIO.cleanup() '''


#todo este funcionaje deberia ponerlo en distintos archivos modulos.



def setup():
    print("Sistema de Control de Acceso Iniciado.")




def loop():
    while True:
        try:
            GPIO.setmode(GPIO.BOARD) # Configura el modo numeracion de placa.
            GPIO.setup(RELAY_1_PIN, GPIO.OUT) # configura el relé_pin como salida. esto debe ir al setup
            GPIO.output(RELAY_1_PIN, GPIO.LOW)  # Asegura que el relé comience apagado, deberia ser normal cerrado.
            
            #lee la tarjeta:

            print("Esperando una tarjeta...")
            card_id, text = lector_1.read() #asignacion multiple, a text nunca lo usa.
            card_id = str(card_id).strip() #strip le saca los espacios y str lo castea a estring
            print(f"Tarjeta leída: {card_id}") #print con formato.
            
            #se fija si esta autorizada

            if is_card_authorized(card_id):
                print("Acceso permitido.")
                activate_relay()  # Activar el relé para abrir la puerta
            else:
                print("Acceso denegado.")
                # Aquí puedes agregar lógica para alarmas, etc.

            time.sleep(1)  # Retardo para evitar lecturas múltiples rápidas

        except KeyboardInterrupt:
            print("\nSaliendo del sistema.")
            break
        finally:
            print("mondongo")
            GPIO.cleanup()
            
            

def activate_relay():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RELAY_1_PIN, GPIO.OUT)
    GPIO.output(RELAY_1_PIN, GPIO.HIGH)
    print("Relé activado - Abriendo puerta")
    time.sleep(2)  # Mantener el relé activado por 5 segundos (ajústalo según sea necesario)
    GPIO.output(RELAY_1_PIN, GPIO.LOW)
    print("Relé desactivado - Cerrando puerta")



def is_card_authorized(card_id):
    try:
        with open(SD_FILE_PATH, 'r') as f:  #el with lo usa para manejar los archivos y el as f  le da otro nombre para referenciarlo en adelante
            authorized_cards = f.read().splitlines()  #el splitlines separa linea por linea y parece que mete todo en una tupla
            return card_id in authorized_cards   #se fija si en esa tupla esta la tarjeta que presento que es car aidí
    except FileNotFoundError:
        print("El archivo de autorizaciones no se encuentra.")
        return False


#esto es lo del tema que paiton necesita un punto de entrada por mein y no se por que se lo indica asi.
if __name__ == "__main__":
    main()