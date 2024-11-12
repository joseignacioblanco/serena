#Archivo de implemantacion de Funciones y tareas.

SD_FILE_PATH = "/home/pi/Documents/serena/autorized_cards.txt"

#definiciones de funciones


def is_card_authorized(card_id):
    try:
        with open(SD_FILE_PATH, 'r') as f:
            authorized_cards = f.read().splitlines()
            return card_id in authorized_cards
    except FileNotFoundError:
        print("El archivo de autorizaciones no se encuentra.")
        return False



