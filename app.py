import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from implement import *
import time

lector_1 = SimpleMFRC522()


RELAY_1_PIN = 5

def setup():
    print("Sistema de Control de Acceso Iniciado.")
    RELAY_1_PIN = 5
    lector_1 = SimpleMFRC522()




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