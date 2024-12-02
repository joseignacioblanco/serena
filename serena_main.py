#! /usr/bin/python3
# Este es el shebang para que se ejecute como script de python.
# no puede haber nada mas en a primera linea sino no anda.
'''Este archivo serena_main era para tener un punto de entrada a la aplicacion de control de acceso
supuestamente ya estaria obsoleto siendo que el archivo de multihilos prueba de hilos lo reeplaza para
poder hacer andar todos los programas en simultaneo'''

#------------------------------ PROYECTO SERENA 9/NOV/2024 --------------------------
# AUTOR: JOSE BLANCO.
# CONTACTO: tombonia@gmail.com
# Descripción: Implementa un control de acceso en una Raspberry pi para un consorio.
# Lenguaje preferido: Python.
#------------------------------------------------------------------------------------

import app

def main():
    print("Sistema de Control de Acceso Iniciado.")
    app.loop()


# Python necesita un punto de entrada por el mein y no se por que se lo indica asi.
if __name__ == "__main__":
    main()