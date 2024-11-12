#Archivo de implemantacion de Funciones y tareas.

SD_FILE_PATH = "/home/pi/Documents/serena/autorized_cards.txt"

#definiciones de funciones


def is_card_authorized(card_id):
    try:
        with open(SD_FILE_PATH, 'r') as f:  #el with lo usa para manejar los archivos y el as f  le da otro nombre para referenciarlo en adelante
            authorized_cards = f.read().splitlines()  #el splitlines separa linea por linea y parece que mete todo en una tupla
            return card_id in authorized_cards   #se fija si en esa tupla esta la tarjeta que presento que es car aidí
    except FileNotFoundError:
        print("El archivo de autorizaciones no se encuentra.")
        return False



