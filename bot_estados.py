#! /usr/bin/python3

import telebot
import RPi.GPIO as GPIO


# Configura los GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)  # Pin 7 como salida, TODO:darle nombres y poner constanstes simbolicas


# Token de tu bot
#BOT_TOKEN = "6934161704:AAEG8TayLzH0VRerDJCOyf5V95Q4-USxcvg" este es el bot de iyire
#BOT_TOKEN = '5568512239:AAGlvS7ObKzH0jHHaamfuVPbU5K2Tixbny8' este es el bot de prueba1
BOT_TOKEN = '6739139472:AAG4gSZYEWjtjiUdyACO-eL-0u0nhB9dZHM' #este es el bot de plumistachi


# Crea un objeto bot
bot = telebot.TeleBot(BOT_TOKEN)

estado_gpio = {7: False} # Diccionario para almacenar el estado de los GPIO TODO: iniciar todos en False





# Define los comandos

@bot.message_handler(commands=['bloquear_puerta', '/bloquear_puerta@plumistachi_bot'])
def encender(message):
    GPIO.output(7, GPIO.HIGH)
    estado_gpio[7] = True
    bot.reply_to(message, "Puertas Bloqueadas!")



@bot.message_handler(commands=['desbloquear_puerta'])
def apagar(message):
    GPIO.output(7, GPIO.LOW)
    estado_gpio[7] = False
    bot.reply_to(message, "Puertas Desbloqueadas.")



#agregar aqio funcionalidades






@bot.message_handler(commands=['estado_del_sistema'])
def estado(message):
    if estado_gpio[7]:
        bot.reply_to(message, "La puerta esta Bloqueada.")
    else:
        bot.reply_to(message, "La Puerta esta Desbloqueada.")




@bot.message_handler(commands=['ayuda'])
def ayuda(message):
    bot.reply_to(message, 'MENU DE OPCIONES: \n\n' + '🔐 /bloquear_puerta \n' + '🔓 /desbloquear_puerta \n\n' + '🦗 /con_chicharra \n' + '🔇 /sin_chicharra \n\n' + '📊 /estado_del_sistema : Estado general del sistema \n' + '🆘 /ayuda : Muestra este menu')





# Ejecuta el bot
bot.polling()



       
        
if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
    
    '''
    try:
    
    
    
    except KeyboardInterrupt:
            print("\nSaliendo del sistema.")
            break
        finally:
            GPIO.cleanup()
    
    
    
    '''