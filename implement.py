import RPi.GPIO as GPIO
import time
import datetime
import csv

RELAY_1_PIN = 5
BUZZER_PIN = 3
#SD_FILE_PATH = "/home/pi/Documents/serena/autorized_cards.txt"
VINCULATION_FILE = "/home/pi/Documents/serena/vinculacion.csv"

autorizado = True
denegado = False


#-------------------------------------------------------------------------------------------

def activate_relay():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RELAY_1_PIN, GPIO.OUT)
    GPIO.output(RELAY_1_PIN, GPIO.HIGH)
    print("Relé activado - Abriendo puerta")
    buzzer(autorizado)
    time.sleep(2)  # Mantener el relé activado por 5 segundos (ajústalo según sea necesario)
    GPIO.output(RELAY_1_PIN, GPIO.LOW)
    print("Relé desactivado - Cerrando puerta")

#-------------------------------------------------------------------------------------------

def is_card_authorized(card_id):
    try:
        with open(VINCULATION_FILE, 'r') as f:  #el with lo usa para manejar los archivos y el as f  le da otro nombre para referenciarlo en adelante
            #authorized_cards = f.read().splitlines()  #el splitlines separa linea por linea y parece que mete todo en una tupla
            authorized_cards = cargar_ids_desde_csv(VINCULATION_FILE)
            return card_id in authorized_cards   #se fija si en esa tupla esta la tarjeta que presento que es car aidí
    except FileNotFoundError:
        print("El archivo de autorizaciones no se encuentra.")
        return False


#-------------------------------------------------------------------------------------------


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
  print(registro)
  with open(archivo_log, 'a') as f:
    f.write(registro)

#-------------------------------------------------------------------------------------------

def cargar_ids_desde_csv(archivo_csv):
  
    """ funcion para no tener que usar el autorizado.txt sino un vinculacion.csv
    Carga los IDs de un archivo CSV, asumiendo que el ID está en la primera columna.
    Args:
    archivo_csv (str): Ruta al archivo CSV.

    Returns:
    tuple: Tupla con todos los IDs cargados.
    """
  
    ids = []
    with open(archivo_csv, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Extraemos el primer elemento de cada fila (el ID)
            id_tarjeta = row[0]
            ids.append(id_tarjeta)
    return tuple(ids)

#-------------------------------------------------------------------------------------------

def buzzer(autorizacion):
  if autorizacion:
    print("piiiiiiiiiiiiiiiiiiiiip")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    time.sleep(0.1)
    
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    #prender buser autorizado piiiiiiiiiiiiiiiip
  else:
    print("pip pip pip")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    time.sleep(0.2)
    
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    #prender buser denegado pip pip pip