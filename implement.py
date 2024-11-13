import RPi.GPIO as GPIO
import time
import datetime


RELAY_1_PIN = 5
SD_FILE_PATH = "/home/pi/Documents/serena/autorized_cards.txt"


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




def registrar_acceso(id_tarjeta, archivo_vinculacion, archivo_log):
  """
  Registra el acceso de una tarjeta RFID.

  Args:
    id_tarjeta: El ID de la tarjeta leída.
    archivo_vinculacion: El nombre del archivo que contiene la vinculación de ID, nombre y DNI.
    archivo_log: El nombre del archivo donde se registrarán los eventos.
  """

  # Leer el archivo de vinculación y crear un diccionario
  usuarios = {}
  with open(archivo_vinculacion, 'r') as f:
    for linea in f:
      id, nombre, dni = linea.strip().split(',')
      usuarios[id] = (nombre, dni)

  # Obtener la fecha y hora actual
  ahora = datetime.datetime.now()

  # Obtener el nombre y DNI del usuario asociado al ID
  nombre, dni = usuarios.get(id_tarjeta, ("Desconocido", "Desconocido"))

  # Formatear el registro
  registro = f"{ahora:%Y-%m-%d %H:%M:%S}, {id_tarjeta}, {nombre}, {dni}\n"

  # Escribir el registro en el archivo de log
  with open(archivo_log, 'a') as f:
    f.write(registro)