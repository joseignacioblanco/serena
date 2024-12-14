#! /usr/bin/python3


''' Aqui esta la maquina de estados que le dice al programa en cada momento como es la situacion y va integrando
las demas funciones segun el estado en que se encuentre.'''



import time
import RPi.GPIO as GPIO
import implement
import bot_estados

# Configuración de pines GPIO (ejemplo de pines; ajusta según tu configuración)
BUZZER_PIN = 11
SENSOR_PUERTA_PIN = 31
SENSOR_VIBRACION_PIN = 33
MAGNETIC_LOCK_PIN = 7
ALARMA_PIN = 29
ALARMA2_PIN = 37

# Configuración GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(SENSOR_PUERTA_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SENSOR_VIBRACION_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(MAGNETIC_LOCK_PIN, GPIO.OUT)

#GPIO.output(PIN_BUZZER, GPIO.LOW)
#GPIO.output(PIN_RELAY_PUERTA, GPIO.LOW)

# Variables globales
estado_actual = "ESPERA"
flag = False
#usuarios_autorizados = {"123456": "Usuario 1", "654321": "Usuario 2"}  # Diccionario de ejemplo

# Funciones auxiliares



def verificar_sensor_puerta():
    """Verifica si la puerta está abierta."""
    return GPIO.input(SENSOR_PUERTA_PIN)

def verificar_sensor_vibracion():
    """Verifica si hay vibración detectada (puerta forzada)."""
    return GPIO.input(SENSOR_VIBRACION_PIN)


#-----------------------------------------------------------------------------------------------

def estado_espera():
    #Estado inicial en espera de un usuario con tarjeta.
    global estado_actual, flag
    print("MACHINE: ESPERA. Esperando tarjeta...")
    
    
    if (implement.estado_gpio[MAGNETIC_LOCK_PIN] == implement.BLOQUEADA) and (verificar_sensor_puerta()) and flag == False:
        print("MACHINE: ESTADO INTRUSO")
        estado_actual = "INTRUSO"
    
    elif ((bot_estados.estado_gpio[BUZZER_PIN] == bot_estados.APAGADO) or (bot_estados.estado_gpio[MAGNETIC_LOCK_PIN] == bot_estados.DESBLOQUEADA)):
        print("MACHINE: ESTADO MODO DE SERVICIO.")
        estado_actual = "SERVICIO"
        flag = True
    
    elif (implement.estado_gpio[MAGNETIC_LOCK_PIN] == implement.DESBLOQUEADA or bot_estados.estado_gpio[MAGNETIC_LOCK_PIN] == bot_estados.DESBLOQUEADA):
        print("MACHINE: ESTADO ABRIENDO PUERTA")
        estado_actual = "ABRIENDO"
    
    
    elif verificar_sensor_puerta():
        print("MACHINE: ESTADO PUERTA ABIERTA CHICHARRIANDO")
        estado_actual = "PUERTA_ABIERTA"
    
    
        
    elif verificar_sensor_vibracion():
        print("MACHINE: ESTADO ADVERTENCIA")
        estado_actual = "ADVERTENCIA"
        
    
        
    else:
        print("MACHINE: ESTADO ESPERA")
        estado_actual = "ESPERA"
        if not verificar_sensor_puerta():
            flag = False #para que pueda volver a entrar al estado intruso porque sino de servicio se pasaba a intruso y era mejor que se quede en espera hasta que se cierre la puerta
            












def estado_abriendo():
    #Estado abriendo esperando que abran la puerta porque ya le dieron acceso.
    global estado_actual
    print("MACHINE: ABRIENDO")
    
    if verificar_sensor_puerta():
        time.sleep(4)
        print("MACHINE: ESTADO CHICHARRA DE PUERTA ABIERTA")
        estado_actual = "PUERTA_ABIERTA"
    
    elif (implement.estado_gpio[MAGNETIC_LOCK_PIN] == implement.BLOQUEADA) and (not verificar_sensor_puerta()):
        print("MACHINE: MODO ESPERA.")
        estado_actual = "ESPERA"
    else:
        print("...")
        estado_actual = "ABRIENDO"
        






def estado_puerta_abierta():
    #Estado puerta abierta y sonando la chicharra.
    global estado_actual
    print("MACHINE: PUERTA ABIERTA Y CHICHARRIANDO")
    
    if not verificar_sensor_puerta():
        print("MACHINE: ESTADO ESPERA")
        estado_actual = "ESPERA"
    
    else:
        print("CHICHARRIANDO...")
        implement.chicharra()
        estado_actual = "PUERTA_ABIERTA"






def estado_servicio():
    #Estado servicio para mudanzas y basura.
    global estado_actual
    print("MACHINE: ESTADO DE SERVICIO")
    
    if bot_estados.estado_gpio[BUZZER_PIN] == bot_estados.PRENDIDO and bot_estados.estado_gpio[MAGNETIC_LOCK_PIN] == bot_estados.BLOQUEADA:
        print("MACHINE: ESTADO ESPERA")
        estado_actual = "ESPERA"
    
    else:
        print("MACHINE: ESTADO DE SERVICIO")
        estado_actual = "SERVICIO"






def estado_advertencia():
    #Estado de advertencia por maltrato.
    global estado_actual
    print("MACHINE: ESTADO ADVERTENCIA")
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ALARMA_PIN, GPIO.OUT)
    GPIO.output(ALARMA_PIN, implement.TURN_ON)
    time.sleep(1)
    GPIO.output(ALARMA_PIN, implement.TURN_OFF)
    estado_actual = "ESPERA"
    
    
    
    
def estado_intruso():
    #Estado intruso abrio la puerta sin autorizacion.
    global estado_actual
    print("MACHINE: ESTADO INTRUSO IN")
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ALARMA2_PIN, GPIO.OUT)
    GPIO.output(ALARMA2_PIN, implement.TURN_ON)
    print("prende alarma intruso")
    time.sleep(5)
    GPIO.output(ALARMA2_PIN, implement.TURN_OFF)
    print("apaga alarma intruso")
    estado_actual = "ESPERA"
    
    
    
    

#-------------------------------------------------------------------------------------------------------


def maquina_de_estados():
    """Controlador principal de la máquina de estados."""
    global estado_actual #parece que esto llama una variable global dentro de la funcion. pero si es global no tendria que estar presente sola sin llamarla? inestigar que onda esto.
    try:
        while True: #un bucle por siempre hasta que salga con ctrl + C
            if estado_actual == "ESPERA":
                estado_espera()
            
            elif estado_actual == "ABRIENDO":
                estado_abriendo()
            
            elif estado_actual == "PUERTA_ABIERTA":
                estado_puerta_abierta()
            
            elif estado_actual == "SERVICIO":
                estado_servicio()
            
            elif estado_actual == "ADVERTENCIA":
                estado_advertencia()
            
            elif estado_actual == "INTRUSO":
                estado_intruso()
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nSistema detenido por el usuario.")
    finally:
        GPIO.cleanup()




#if __name__ == "__main__":
#    maquina_de_estados()