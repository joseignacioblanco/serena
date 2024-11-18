#! /usr/bin/python3

import telebot
import RPi.GPIO as GPIO


#Asociacion de pines en modo BOARD
MAGNETIC_LOCK_PIN = 7
BUZZER_PIN = 11
LUZ_VEREDA_PIN = 13
REFLECTOR_PIN = 15
ALARMA_PIN = 29 # disponibles 37



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

GPIO.setup(REFLECTOR_PIN, GPIO.OUT)  # Pin 15 como salida.
GPIO.output(REFLECTOR_PIN, OFF)

GPIO.setup(ALARMA_PIN, GPIO.OUT)  # Pin 29 como salida.
GPIO.output(ALARMA_PIN, OFF)



# Configuracion inicial del diccionario de estados:
estado_gpio = {MAGNETIC_LOCK_PIN: BLOQUEADA, BUZZER_PIN: PRENDIDO, LUZ_VEREDA_PIN: MODO_AUTOMATICO, REFLECTOR_PIN: APAGADO, ALARMA_PIN: APAGADO} # Diccionario para almacenar el estado de los GPIO TODO: iniciar todos en False. por ahora uso un diccionario para saber el estado de los pines, cuando sea grande  ya voy a aprender  a leer el estado de los pines con una funcion gpio.rrid o algo asi.

#----------------------------------------------------------------------------------------------------

# Crea un objeto bot
bot = telebot.TeleBot(BOT_TOKEN)

#----------------------------------------------------------------------------------------------------

# Define los comandos
# COMANDO BLOQUEAR PUERTA
@bot.message_handler(commands=['bloquear_puerta', '/bloquear_puerta@plumistachi_bot'])
def bloquear_puerta(message):
    GPIO.setup(MAGNETIC_LOCK_PIN, GPIO.OUT)
    GPIO.output(MAGNETIC_LOCK_PIN, LOCK)
    estado_gpio[MAGNETIC_LOCK_PIN] = BLOQUEADA
    bot.reply_to(message, "Puertas Bloqueadas!")


# COMANDO DESBLOQUEAR PUERTA
@bot.message_handler(commands=['desbloquear_puerta', '/desbloquear_puerta@plumistachi_bot'])
def desbloquear_puerta(message):
    GPIO.setup(MAGNETIC_LOCK_PIN, GPIO.OUT)
    GPIO.output(MAGNETIC_LOCK_PIN, UNLOCK)
    estado_gpio[MAGNETIC_LOCK_PIN] = DESBLOQUEADA
    bot.reply_to(message, "Puertas Desbloqueadas.")


# COMANDO CON CHICHARRA
@bot.message_handler(commands=['con_chicharra', '/con_chicharra@plumistachi_bot'])
def con_chicharra(message):
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.output(BUZZER_PIN, ON)
    estado_gpio[BUZZER_PIN] = PRENDIDO
    bot.reply_to(message, "Chicharra Prendida!")


# COMANDO SIN CHICHARRA
@bot.message_handler(commands=['sin_chicharra', '/sin_chicharra@plumistachi_bot'])
def sin_chicharra(message):
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.output(BUZZER_PIN, OFF)
    estado_gpio[BUZZER_PIN] = APAGADO
    bot.reply_to(message, "Chicharra Apagada.")


# COMANDO LUZ VEEDA AUTOMATIICO
@bot.message_handler(commands=['luz_vereda_autom', '/luz_vereda_autom@plumistachi_bot'])
def luz_vereda_autom(message):
    GPIO.setup(LUZ_VEREDA_PIN, GPIO.OUT)
    GPIO.output(LUZ_VEREDA_PIN, AUTOMATIC)
    estado_gpio[LUZ_VEREDA_PIN] = MODO_AUTOMATICO
    bot.reply_to(message, "LUZ vereda MODO AUTOMATICO!")


# COMANDO LUZ VEREDA MANUAL
@bot.message_handler(commands=['luz_vereda_manual', '/luz_vereda_manual@plumistachi_bot'])
def luz_vereda_manual(message):
    GPIO.setup(LUZ_VEREDA_PIN, GPIO.OUT)
    GPIO.output(LUZ_VEREDA_PIN, MANUAL)
    estado_gpio[LUZ_VEREDA_PIN] = MODO_MANUAL
    bot.reply_to(message, "LUZ vereda MODO MANUAL.")


# COMANDO REFLECTOR PRENDER
@bot.message_handler(commands=['reflector_prender', '/reflector_prender@plumistachi_bot'])
def reflector_prender(message):
    GPIO.setup(REFLECTOR_PIN, GPIO.OUT)
    GPIO.output(REFLECTOR_PIN, ON)
    estado_gpio[REFLECTOR_PIN] = PRENDIDO
    bot.reply_to(message, "REFLECTOR PRENDIDO!")


# COMANDO REFLECTOR APAGAR
@bot.message_handler(commands=['reflector_apagar', '/reflector_apagar@plumistachi_bot'])
def reflector_apagar(message):
    GPIO.setup(REFLECTOR_PIN, GPIO.OUT)
    GPIO.output(REFLECTOR_PIN, OFF)
    estado_gpio[REFLECTOR_PIN] = APAGADO
    bot.reply_to(message, "REFLECTOR APAGADO!")


# COMANDO ALARMA PRENDER
@bot.message_handler(commands=['alarma_prender', '/alarma_prender@plumistachi_bot'])
def alarma_prender(message):
    GPIO.setup(ALARMA_PIN, GPIO.OUT)
    GPIO.output(ALARMA_PIN, ON)
    estado_gpio[ALARMA_PIN] = PRENDIDO
    bot.reply_to(message, "ALARMA ENCENDIDA!!!")


# COMANDO ALARMA APAGAR
@bot.message_handler(commands=['alarma_apagar', '/alarma_apagar@plumistachi_bot'])
def alarma_apagar(message):
    GPIO.setup(ALARMA_PIN, GPIO.OUT)
    GPIO.output(ALARMA_PIN, OFF)
    estado_gpio[ALARMA_PIN] = APAGADO
    bot.reply_to(message, "ALARMA APAGADA.")



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


    if estado_gpio[REFLECTOR_PIN]:
        bot.reply_to(message, "El reflector esta prendido.")
    else:
        bot.reply_to(message, "El reflector esta apagado.")
        
        
    if estado_gpio[ALARMA_PIN]:
        bot.reply_to(message, "ALARMA PRENDIDA! SONANDO!!.")
    else:
        bot.reply_to(message, "ALARMA APAGADA...")









# COMANDO AYUDA
@bot.message_handler(commands=['ayuda','ayuda@plumistachi_bot'])
def ayuda(message):
    bot.reply_to(message, 'MENU DE OPCIONES: \n\n' + '🔐 /bloquear_puerta \n' + '🔓 /desbloquear_puerta \n\n' + '🦗 /con_chicharra \n' + '🔇 /sin_chicharra \n\n' + '🅰️ /luz_vereda_autom \n' + 'Ⓜ️ /luz_vereda_manual \n\n' + '☀️ /reflector_prender \n' + '🌚 /reflector_apagar \n\n' + '📢 /alarma_prender \n' + '🔕 /alarma_apagar \n\n' + '📊 /estado_del_sistema : Estado general del sistema \n' + '🆘 /ayuda : Muestra este menu')


#-----------------------------------------------------------------------------------------------------


# Ejecuta el bot
def bat():
    try:
        
        bot.polling()
        
    except KeyboardInterrupt:
        print("\nSaliendo del sistema.")
    finally:
        GPIO.cleanup()



       
        
if __name__ == "__main__":
    bat()
    
