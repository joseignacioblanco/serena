#! /usr/bin/python3
# Este es el shebang para que se ejecute como script de python.

#------------------------------ PROYECTO SERENA 9/NOV/2024 --------------------------
# AUTOR: JOSE BLANCO
# CONTACTO: tombonia@gmail.com
# Descripción: Implementa un control de acceso en una Raspberry pi para un consorio.
#------------------------------------------------------------------------------------

#Evidentemente los comentarios en python se hacen con #

#como e el tema para que quede como archivo ejecutable?
# con el shebang #! /usr/bin/python3 pero esto es solo para linux.  en windors ya salen ejecutables.
# como yo lo hago en la rrasberri, entonces va el shebang y todo

# Aqui pone todas las bibliotecas de python que va a usar.
# se usa: from <espacio de nombres> import <bibliotecas> (verificar si es asi lo correcto) para importar todo uso el operador * o sino impport modulo y despues llamo a las funciones con el operador . moduo1.saluda()




import RPi.GPIO as GPIO # que onda el as ese: bueno parece que es para poner GPIO.setmode y no  RPi.GPIO.setmode en la linea 30 mas abajo.
from mfrc522 import SimpleMFRC522 # maneja el modulo rfid.
#import requests # supongo que es algo para macaniar con internet y las webs.
#import os # manipulla archivos.
import time # para manejar cosas que tienen que ver con horarios, dias, tiempo, etc
from implement import * #importa todas las funciones.

#------------------------------------------------------------------------------------------


# Configuración de pines GPIO y RFID
GPIO.setmode(GPIO.BOARD) #para que tome la numeracion de la placa y no de la broadcom.
lector_1 = SimpleMFRC522() # no se que carajos configura de la placa modulo rfid

# Configuración del relé (deberian ser dos puertas no una sola vidrio y reja)

RELAY_PIN = 5 # configura el pin 18 para uno de los reles que van a abrir la puerta
GPIO.setup(RELAY_PIN, GPIO.OUT) # configura como salida.
GPIO.output(RELAY_PIN, GPIO.LOW)  # Asegura que el relé comience apagado, deberia ser normal cerrado.

# Configuración del URL de Google Drive

#FILE_URL = "https://drive.google.com/uc?export=download&id=1A2B3C4D5E6F7G8H9"  # Reemplaza con tu enlace de descarga (esto veremos como lo implemento.  capaz que mejor con una web o si, un drive. o ver si se puede de gitjab..)


#SD_FILE_PATH = "/home/pi4/Documentos/serena/autorized_cards.txt"  # Ruta donde se almacena el archivo en la Raspberry Pi (este es el archivo donde estan los id  de las tarjetas con la info de cada usuario: ver como vincular cada id con persona. va tener que parsear el id o usar un archivo binario y no txt)

#---------------------------------------------------------------------------------------------------------------


#mein


def main():
    print("Sistema de Control de Acceso Iniciado.")
    while True:
        try:
            print("Esperando una tarjeta...")
            card_id, text = lector_1.read()
            card_id = str(card_id).strip()
            print(f"Tarjeta leída: {card_id}")

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
            GPIO.cleanup()



def activate_relay():
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    print("Relé activado - Abriendo puerta")
    time.sleep(2)  # Mantener el relé activado por 5 segundos (ajústalo según sea necesario)
    GPIO.output(RELAY_PIN, GPIO.LOW)
    print("Relé desactivado - Cerrando puerta")




#esto es lo del tema que paiton necesita un punto de entrada por mein y no se por que se lo indica asi.
if __name__ == "__main__":
#    connect_to_wifi()
    main()