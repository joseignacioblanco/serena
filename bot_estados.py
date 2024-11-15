import telebot
import RPi.GPIO as GPIO

# Configura los GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)  # Ejemplo: Pin 7 como salida

# Token de tu bot
#BOT_TOKEN = "6934161704:AAEG8TayLzH0VRerDJCOyf5V95Q4-USxcvg" este es el bot de iyire
#BOT_TOKEN = '5568512239:AAGlvS7ObKzH0jHHaamfuVPbU5K2Tixbny8' este es el bot de prueba1
BOT_TOKEN = '6739139472:AAG4gSZYEWjtjiUdyACO-eL-0u0nhB9dZHM' #este es el bot de plumistachi


# Crea un objeto bot
bot = telebot.TeleBot(BOT_TOKEN)

# Define los comandos
@bot.message_handler(commands=['encender'])
def encender(message):
    GPIO.output(7, GPIO.HIGH)
    bot.reply_to(message, "Dispositivo encendido.")

@bot.message_handler(commands=['apagar'])
def apagar(message):
    GPIO.output(7, GPIO.LOW)
    bot.reply_to(message, "Dispositivo apagado.")

# Ejecuta el bot
bot.polling()














# ... (código anterior)

# Diccionario para almacenar el estado de los GPIO
estado_gpio = {17: False}

# ... (funciones encender y apagar modificadas para actualizar el estado)

@bot.message_handler(commands=['estado'])
def estado(message):
    if estado_gpio[17]:
        bot.reply_to(message, "El dispositivo está encendido.")
    else:
        bot.reply_to(message, "El dispositivo está apagado.")