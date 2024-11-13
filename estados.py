import time
import RPi.GPIO as GPIO
import random  # Simulación de lectura RFID para pruebas

# Configuración de pines GPIO (ejemplo de pines; ajusta según tu configuración)
PIN_BUZZER = 18
PIN_SENSOR_PUERTA = 23
PIN_SENSOR_VIBRACION = 24
PIN_RELAY_PUERTA = 25

# Configuración GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_BUZZER, GPIO.OUT)
GPIO.setup(PIN_SENSOR_PUERTA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PIN_SENSOR_VIBRACION, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PIN_RELAY_PUERTA, GPIO.OUT)
GPIO.output(PIN_BUZZER, GPIO.LOW)
GPIO.output(PIN_RELAY_PUERTA, GPIO.LOW)

# Variables globales
estado_actual = "ESPERA"
usuarios_autorizados = {"123456": "Usuario 1", "654321": "Usuario 2"}  # Diccionario de ejemplo

# Funciones auxiliares
def leer_tarjeta_rfid():
    """Simula la lectura de una tarjeta RFID. En un entorno real, reemplaza con tu código específico."""
    card_id = str(random.choice(list(usuarios_autorizados.keys()) + ["000000"]))  # "000000" representa una tarjeta no autorizada
    print(f"Tarjeta leída: {card_id}")
    return card_id

def activar_buzzer():
    """Activa el buzzer por 2 segundos."""
    GPIO.output(PIN_BUZZER, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(PIN_BUZZER, GPIO.LOW)

def abrir_puerta():
    """Activa el relé para abrir la puerta."""
    GPIO.output(PIN_RELAY_PUERTA, GPIO.HIGH)
    time.sleep(5)  # Simula el tiempo que permanece abierta la puerta
    GPIO.output(PIN_RELAY_PUERTA, GPIO.LOW)

def verificar_sensor_puerta():
    """Verifica si la puerta está abierta."""
    return GPIO.input(PIN_SENSOR_PUERTA)

def verificar_sensor_vibracion():
    """Verifica si hay vibración detectada (puerta forzada)."""
    return GPIO.input(PIN_SENSOR_VIBRACION)

def estado_espera():
    """Estado inicial en espera de un usuario con tarjeta."""
    global estado_actual
    print("Estado: ESPERA. Escaneando tarjeta...")
    card_id = leer_tarjeta_rfid()
    if card_id in usuarios_autorizados:
        print(f"Acceso autorizado para {usuarios_autorizados[card_id]}")
        estado_actual = "PUERTA_ABIERTA"
    elif card_id == "111111":  # Ejemplo de tarjeta maestra para servicio/mudanza
        print("Tarjeta maestra detectada. Modo de servicio activado.")
        estado_actual = "SERVICIO"
    else:
        print("Acceso denegado.")
        activar_buzzer()

def estado_puerta_abierta():
    """Estado cuando se abre la puerta tras un acceso autorizado."""
    global estado_actual
    print("Estado: PUERTA_ABIERTA. Apertura de puerta.")
    abrir_puerta()
    tiempo_inicio = time.time()
    while time.time() - tiempo_inicio < 10:  # Espera hasta 10 segundos
        if verificar_sensor_puerta():
            print("Puerta detectada abierta.")
            estado_actual = "ESPERA"
            return
    print("Puerta no fue abierta. Retornando al estado de espera.")
    estado_actual = "ESPERA"

def estado_intruso():
    """Estado de detección de intruso si se detecta vibración sin autorización."""
    global estado_actual
    print("Estado: INTRUSO DETECTADO. Activando alarma.")
    activar_buzzer()
    # Simulación de manejo de alarma; podría incluir más lógica de seguridad
    estado_actual = "ESPERA"

def estado_servicio():
    """Estado especial para servicio/mudanza. Desactiva cerraduras y alarmas temporalmente."""
    global estado_actual
    print("Estado: SERVICIO. Cerraduras y alarmas desactivadas temporalmente.")
    tiempo_servicio = 30  # Tiempo durante el cual el modo de servicio está activo
    tiempo_inicio = time.time()
    while time.time() - tiempo_inicio < tiempo_servicio:
        print("Modo servicio activo...")  # Simulación de operaciones de servicio
        time.sleep(5)
    print("Saliendo del modo de servicio.")
    estado_actual = "ESPERA"

def maquina_de_estados():
    """Controlador principal de la máquina de estados."""
    global estado_actual
    try:
        while True:
            if estado_actual == "ESPERA":
                estado_espera()
            elif estado_actual == "PUERTA_ABIERTA":
                estado_puerta_abierta()
            elif estado_actual == "INTRUSO":
                estado_intruso()
            elif estado_actual == "SERVICIO":
                estado_servicio()
            # Verificar condiciones para detección de intrusos
            if verificar_sensor_vibracion() and not verificar_sensor_puerta():
                estado_actual = "INTRUSO"
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSistema detenido por el usuario.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    maquina_de_estados()
