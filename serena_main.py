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
# se usa: from <espacio de nombres> import <bibliotecas> (verificar si es asi lo correcto)

import RPi.GPIO as GPIO # que onda el as ese: bueno parece que maneja los gpio.
from mfrc522 import SimpleMFRC522 # maneja el modulo rfid.
import requests # supongo que es algo para macaniar con internet y las webs.
import os # ni idea
import time # para manejar cosas que tienen que ver con horarios, dias, tiempo, etc


#------------------------------------------------------------------------------------------


# Configuración de pines GPIO y RFID
GPIO.setmode(GPIO.BOARD) #para que tome la numeracion de la placa y no de la broadcom.
reader = SimpleMFRC522() # no se que carajos configura de la placa modulo rfid

# Configuración del relé (deberian ser dos puertas no una sola vidrio y reja)
RELAY_PIN = 18 # configura el pin 18 para uno de los reles que van a abrir la puerta
GPIO.setup(RELAY_PIN, GPIO.OUT) # configura como salida.
GPIO.output(RELAY_PIN, GPIO.LOW)  # Asegura que el relé comience apagado, deberia ser normal cerrado.

# Configuración de Wi-Fi y URL de Google Drive
WIFI_SSID = "TuSSID"  #esta info no iria porqeu ya rrasberri ya se conectaria sola creo.
WIFI_PASSWORD = "TuPassword"
FILE_URL = "https://drive.google.com/uc?export=download&id=1A2B3C4D5E6F7G8H9"  # Reemplaza con tu enlace de descarga (esto veremos como lo implemento.  capaz que mejor con una web o si, un drive...)

MASTER_CARD_UID = "12ab34cd56"  # UID de la tarjeta maestra   (Esto sacalo. lo hago desde ssh con una terminal y un comandito para actualizar la lista. o directamente la actualizo onfire)
SD_FILE_PATH = "/home/pi/autorizadas.txt"  # Ruta donde se almacena el archivo en la Raspberry Pi (este es el archivo donde estan los id  de las tarjetas con la info de cada usuario: ver como vincular cada id con persona. va tener que parsear el id o usar un archivo binario y no txt)


#---------------------------------------------------------------------------------------------------------------
#definiciones de funciones

def connect_to_wifi():
    # Puedes usar herramientas como wpa_supplicant para configurar el Wi-Fi si no está configurado.
    # Aquí asumimos que la conexión ya está establecida.
    pass   #todo esto no iria




def download_file_from_cloud(): #funcioncita para descargar el archivo desde drive
    try:
        response = requests.get(FILE_URL, stream=True)
        if response.status_code == 200:
            with open(SD_FILE_PATH, 'w') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk.decode())
            print("Archivo descargado y actualizado desde Google Drive.")
        else:
            print(f"Error al descargar el archivo. Código de respuesta: {response.status_code}")
    except Exception as e:
        print(f"Error durante la descarga del archivo: {e}")



def is_card_authorized(card_id):
    try:
        with open(SD_FILE_PATH, 'r') as f:
            authorized_cards = f.read().splitlines()
            return card_id in authorized_cards
    except FileNotFoundError:
        print("El archivo de autorizaciones no se encuentra.")
        return False







def activate_relay():
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    print("Relé activado - Abriendo puerta")
    time.sleep(5)  # Mantener el relé activado por 5 segundos (ajústalo según sea necesario)
    GPIO.output(RELAY_PIN, GPIO.LOW)
    print("Relé desactivado - Cerrando puerta")


#mein


def main():
    print("Sistema de Control de Acceso Iniciado.")
    while True:
        try:
            print("Esperando una tarjeta...")
            card_id, text = reader.read()
            card_id = str(card_id).strip()
            print(f"Tarjeta leída: {card_id}")

            if card_id == MASTER_CARD_UID:
                print("Tarjeta maestra detectada. Actualizando la lista de autorizadas desde la nube...")
                download_file_from_cloud()
            else:
                if is_card_authorized(card_id):
                    print("Acceso permitido.")
                    activate_relay()  # Activar el relé para abrir la puerta
                else:
                    print("Acceso denegado.")
                    # Aquí puedes agregar lógica para alarmas, etc.

            time.sleep(2)  # Retardo para evitar lecturas múltiples rápidas

        except KeyboardInterrupt:
            print("\nSaliendo del sistema.")
            break
        finally:
            GPIO.cleanup()


#esto es lo del tema que paiton necesita un punto de entrada por mein y no se por que se lo indica asi.
if __name__ == "__main__":
    connect_to_wifi()
    main()
