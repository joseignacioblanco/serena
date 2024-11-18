#! /usr/bin/python3

import time
import RPi.GPIO as GPIO


# Configuración de pines GPIO (ejemplo de pines; ajusta según tu configuración)
BUZZER_PIN = 11
SENSOR_PUERTA_PIN = 31
SENSOR_VIBRACION_PIN = 33
MAGNETIC_LOCK_PIN = 7

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
#usuarios_autorizados = {"123456": "Usuario 1", "654321": "Usuario 2"}  # Diccionario de ejemplo

# Funciones auxiliares



def verificar_sensor_puerta():
    """Verifica si la puerta está abierta."""
    return GPIO.input(PIN_SENSOR_PUERTA)

def verificar_sensor_vibracion():
    """Verifica si hay vibración detectada (puerta forzada)."""
    return GPIO.input(PIN_SENSOR_VIBRACION)


#-----------------------------------------------------------------------------------------------

def estado_espera():
    """Estado inicial en espera de un usuario con tarjeta."""
    global estado_actual
    print("Estado: ESPERA. Esperando tarjeta...")
    if :
        print(f"Acceso autorizado para {usuarios_autorizados[card_id]}")
        estado_actual = "PUERTA_ABIERTA"
    elif card_id == "111111":  # Ejemplo de tarjeta maestra para servicio/mudanza
        print("Tarjeta maestra detectada. Modo de servicio activado.")
        estado_actual = "SERVICIO"
    else:
        print("Acceso denegado.")
        activar_buzzer()


















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
            
            # Verificar condiciones para detección de intrusos TODO:
            if verificar_sensor_vibracion() and not verificar_sensor_puerta():
                estado_actual = "INTRUSO"
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nSistema detenido por el usuario.")
    finally:
        GPIO.cleanup()




if __name__ == "__main__":
    maquina_de_estados()