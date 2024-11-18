#! /ust/bin/python3

import threading
import app
from bot_estados import *


# esto ejecuta todo lo de serena_main.py de control de acceso -------------------------------------
def tarea1():
    # Código de la primera tarea
    print("Tarea 1 en ejecución")
    # ...
    app.loop()
#---------------------------------------------------------------------------------------------------




# este otro ilo controla el bot de telegram -------------------------------------------------------
def tarea2():
    # Código de la segunda tarea
    print("Tarea 2 en ejecución")
    # ...
    bat()


#---------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    hilo1 = threading.Thread(target=tarea1)
    hilo2 = threading.Thread(target=tarea2)

    hilo1.start()
    hilo2.start()

    # Esperar a que ambos hilos terminen (opcional)
    hilo1.join()
    hilo2.join()