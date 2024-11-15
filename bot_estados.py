#! /usr/bin/python3

import telebot
import RPi.GPIO as GPIO


#Asociacion de pines en modo BOARD
MAGNETIC_LOCK_PIN = 7
BUZZER_PIN = 11 # 15, 29, 31, 33, 37
LUZ_VEREDA_PIN = 13



#----------------------------------------------------------------------------------------------------
# CONFIGURA el Token del bot:
#BOT_TOKEN = "6934161704:AAEG8TayLzH0VRerDJCOyf5V95Q4-USxcvg" este es el bot de iyire
#BOT_TOKEN = '5568512239:AAGlvS7ObKzH0jHHaamfuVPbU5K2Tixbny8' este es el bot de prueba1
BOT_TOKEN = '6739139472:AAG4gSZYEWjtjiUdyACO-eL-0u0nhB9dZHM' #este es el bot de plumistachi

#----------------------------------------------------------------------------------------------------


#para el comandito de la biblioteca GPIO
LOCK = ON = AUTOMATIC = GPIO.HIGH
UNLOCK = OFF = MANUAL = GPIO.LOW

#para el diccionario
BLOQUEADA = PRENDIDO = MODO_AUTOMATICO = True
DESBLOQUEADA = APAGADO = MODO_MANUAL = False



# Configura los GPIO al estado inicial.
GPIO.setmode(GPIO.BOARD)

GPIO.setup(MAGNETIC_LOCK_PIN, GPIO.OUT)  # Pin 7 como salida.
GPIO.output(MAGNETIC_LOCK_PIN, LOCK)

GPIO.setup(BUZZER_PIN, GPIO.OUT)  # Pin 11 como salida.
GPIO.output(BUZZER_PIN, ON)

GPIO.setup(LUZ_VEREDA_PIN, GPIO.OUT)  # Pin 13 como salida.
GPIO.output(LUZ_VEREDA_PIN, AUTOMATIC)





# Configuracion inicial del diccionario de estados:
estado_gpio = {MAGNETIC_LOCK_PIN: BLOQUEADA, BUZZER_PIN: PRENDIDO, LUZ_VEREDA_PIN: MODO_AUTOMATICO} # Diccionario para almacenar el estado de los GPIO TODO: iniciar todos en False. por ahora uso un diccionario para saber el estado de los pines, cuando sea grande  ya voy a aprender  a leer el estado de los pines con una funcion gpio.rrid o algo asi.

#----------------------------------------------------------------------------------------------------

# Crea un objeto bot
bot = telebot.TeleBot(BOT_TOKEN)

#----------------------------------------------------------------------------------------------------

# Define los comandos
# COMANDO BLOQUEAR PUERTA
@bot.message_handler(commands=['bloquear_puerta', '/bloquear_puerta@plumistachi_bot'])
def bloquear_puerta(message):
    GPIO.output(MAGNETIC_LOCK_PIN, LOCK)
    estado_gpio[MAGNETIC_LOCK_PIN] = BLOQUEADA
    bot.reply_to(message, "Puertas Bloqueadas!")


# COMANDO DESBLOQUEAR PUERTA
@bot.message_handler(commands=['desbloquear_puerta', '/desbloquear_puerta@plumistachi_bot'])
def desbloquear_puerta(message):
    GPIO.output(MAGNETIC_LOCK_PIN, UNLOCK)
    estado_gpio[MAGNETIC_LOCK_PIN] = DESBLOQUEADA
    bot.reply_to(message, "Puertas Desbloqueadas.")


# COMANDO CON CHICHARRA
@bot.message_handler(commands=['con_chicharra', '/con_chicharra@plumistachi_bot'])
def con_chicharra(message):
    GPIO.output(BUZZER_PIN, ON)
    estado_gpio[BUZZER_PIN] = PRENDIDO
    bot.reply_to(message, "Chicharra Prendida!")


# COMANDO SIN CHICHARRA
@bot.message_handler(commands=['sin_chicharra', '/sin_chicharra@plumistachi_bot'])
def sin_chicharra(message):
    GPIO.output(BUZZER_PIN, OFF)
    estado_gpio[BUZZER_PIN] = APAGADO
    bot.reply_to(message, "Chicharra Apagada.")


# COMANDO LUZ VEEDA AUTOMATIICO
@bot.message_handler(commands=['luz_vereda_autom', '/luz_vereda_autom@plumistachi_bot'])
def luz_vereda_autom(message):
    GPIO.output(LUZ_VEREDA_PIN, AUTOMATIC)
    estado_gpio[LUZ_VEREDA_PIN] = MODO_AUTOMATICO
    bot.reply_to(message, "LUZ vereda MODO AUTOMATICO!")


# COMANDO LUZ VEREDA MANUAL
@bot.message_handler(commands=['luz_vereda_manual', '/luz_vereda_manual@plumistachi_bot'])
def luz_vereda_manual(message):
    GPIO.output(LUZ_VEREDA_PIN, MANUAL)
    estado_gpio[LUZ_VEREDA_PIN] = MODO_MANUAL
    bot.reply_to(message, "LUZ vereda MODO MANUAL.")








# COMANDO mondongo






# COMANDO ESTADO DEL SISTEMA
@bot.message_handler(commands=['estado_del_sistema', 'estado_del_sistema@plumistachi_bot'])
def estado_del_sistema(message):
    if estado_gpio[MAGNETIC_LOCK_PIN]:
        bot.reply_to(message, "La puerta esta Bloqueada.")
    else:
        bot.reply_to(message, "La Puerta esta Desbloqueada.")


    if estado_gpio[BUZZER_PIN]:
        bot.reply_to(message, "El buzzer esta prendido.")
    else:
        bot.reply_to(message, "El buzzer esta apagado.")


    if estado_gpio[LUZ_VEREDA_PIN]:
        bot.reply_to(message, "La luz de la vereda esta en modo AUTOMATICO.")
    else:
        bot.reply_to(message, "La luz de la vereda esta en modo MANUAL.")



# COMANDO AYUDA
@bot.message_handler(commands=['ayuda','ayuda@plumistachi_bot'])
def ayuda(message):
    bot.reply_to(message, 'MENU DE OPCIONES: \n\n' + '🔐 /bloquear_puerta \n' + '🔓 /desbloquear_puerta \n\n' + '🦗 /con_chicharra \n' + '🔇 /sin_chicharra \n\n' + '🅰️ /luz_vereda_autom \n' + 'Ⓜ️ /luz_vereda_manual \n\n' + '📊 /estado_del_sistema : Estado general del sistema \n' + '🆘 /ayuda : Muestra este menu')


#-----------------------------------------------------------------------------------------------------


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