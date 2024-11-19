import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522
from implement import *

#VINCULATION_FILE = "/home/pi/Documents/serena/vinculacion.csv"
REGISTER_FILE = "/home/pi/Documents/serena/log_accesos.csv"

lector_1 = SimpleMFRC522()


def loop():
    while True:
        try:
            GPIO.setmode(GPIO.BOARD) # Configura el modo numeracion de placa.
            GPIO.setup(RELAY_1_PIN, GPIO.OUT) # configura el relé_pin como salida. esto debe ir al setup
            GPIO.output(RELAY_1_PIN, TURN_OFF)  # Asegura que el relé comience apagado, deberia ser normal cerrado.
            
            GPIO.setup(BUZZER_PIN, GPIO.OUT)
            GPIO.output(BUZZER_PIN, TURN_OFF)

            #lee la tarjeta:

            print("Esperando una tarjeta...")
            card_id, text = lector_1.read() #asignacion multiple, a text lo usa para parsear porque sino mete basura en id.
            card_id = str(card_id).strip() #strip le saca los espacios y str lo castea a estring
            registrar_acceso(card_id, VINCULATION_FILE, REGISTER_FILE)
            print(f"Tarjeta leída: {card_id}") #print con formato.

            #se fija si esta autorizada

            if is_card_authorized(card_id):
                print("Acceso permitido.")
                activate_relay()  # Activar el relé para abrir la puerta
            else:
                print("Acceso denegado.")
                buzzer(denegado)

            time.sleep(1)  # Retardo para evitar lecturas múltiples rápidas

        except KeyboardInterrupt:
            print("\nSaliendo del sistema.")
            break
#        finally: #si le pongo esto, se tranga cuando anda el simultaneo con el bot y ademas reinicia la setiada de estados del bot. por eso lo sacamos
#            GPIO.cleanup()