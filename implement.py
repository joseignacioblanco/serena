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