#Archivo de implemantacion de Funciones y tareas.

#definiciones de funciones


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
    time.sleep(2)  # Mantener el relé activado por 5 segundos (ajústalo según sea necesario)
    GPIO.output(RELAY_PIN, GPIO.LOW)
    print("Relé desactivado - Cerrando puerta")




