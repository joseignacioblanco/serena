#! /ust/bin/python3
#TODO: todo esto luego iria a serena_main o sino lo reemplaza.

import threading
import app
import state_machine
from bot_estados import *


# esto ejecuta todo lo de serena_main.py de control de acceso -------------------------------------
def tarea1():
    # Código de la primera tarea
    print("Tarea 1 en ejecución: Control de acceso iniciado")
    # ...
    app.loop()
#---------------------------------------------------------------------------------------------------




# este otro ilo controla el bot de telegram -------------------------------------------------------
def tarea2():
    # Código de la segunda tarea
    print("Tarea 2 en ejecución: telegram bot iniciado")
    # ...
    bat() # le cambio el nombre a bat porque bot tiene conflicto con las librerias de telegram.  por eso no hay que usar import * abito?

#----------------------------------------------------------------------------------------------------






# este otro ilo controla el bot de telegram -------------------------------------------------------
def tarea3():
    # Código de la tercera tarea
    print("Tarea 3 en ejecución: maquina de estados iniciada")
    # ...
    state_machine.maquina_de_estados()

#---------------------------------------------------------------------------------------------------







if __name__ == "__main__":
    hilo1 = threading.Thread(target=tarea1)
    hilo2 = threading.Thread(target=tarea2)
    hilo3 = threading.Thread(target=tarea3)

    hilo1.start()
    hilo2.start()
    hilo3.start()

    # Esperar a que ambos hilos terminen (opcional)
    hilo1.join()
    hilo2.join()
    hilo3.join()