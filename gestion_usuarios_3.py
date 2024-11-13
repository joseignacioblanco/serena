#! /usr/bin/python3

import csv
import os
from mfrc522 import SimpleMFRC522

CSV_FILE = "/home/pi/Documents/serena/vinculacion.csv"

lector_1 = SimpleMFRC522()

def leer_archivo_csv():
    """Lee el archivo CSV y devuelve los datos como una lista de diccionarios."""
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def escribir_archivo_csv(data):
    """Escribe la lista de diccionarios en el archivo CSV."""
    with open(CSV_FILE, mode='w', newline='') as file:
        fieldnames = ['CARD_ID', 'NAME', 'DNI']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def mostrar_datos(data):
    """Muestra todos los datos en formato tabular."""
    if not data:
        print("No hay datos disponibles.")
        return
    print(f"{'CARD_ID':<15}{'NAME':<20}{'DNI':<15}")
    print("=" * 50)
    for row in data:
        print(f"{row['CARD_ID']:<15}{row['NAME']:<20}{row['DNI']:<15}")

def consultar_por_card_id(card_id):
    """Consulta un usuario por su CARD_ID."""
    data = leer_archivo_csv()
    for row in data:
        if row['CARD_ID'] == card_id:
            print(f"Usuario encontrado:\nCARD_ID: {row['CARD_ID']}\nNAME: {row['NAME']}\nDNI: {row['DNI']}")
            return
    print("Usuario no encontrado.")

def agregar_usuario(card_id, name, dni):
    """Agrega un nuevo usuario al archivo CSV."""
    data = leer_archivo_csv()
    if any(row['CARD_ID'] == card_id for row in data):
        print("El CARD_ID ya existe. No se puede agregar.")
        return
    data.append({'CARD_ID': card_id, 'NAME': name, 'DNI': dni})
    escribir_archivo_csv(data)
    print("Usuario agregado con éxito.")

def modificar_usuario(card_id):
    """Modifica los datos de un usuario existente."""
    data = leer_archivo_csv()
    for row in data:
        if row['CARD_ID'] == card_id:
            row['NAME'] = input("Nuevo nombre: ")
            row['DNI'] = input("Nuevo DNI: ")
            escribir_archivo_csv(data)
            print("Usuario modificado con éxito.")
            return
    print("Usuario no encontrado.")

def eliminar_usuario(card_id):
    """Elimina un usuario por su CARD_ID."""
    data = leer_archivo_csv()
    new_data = [row for row in data if row['CARD_ID'] != card_id]
    if len(data) == len(new_data):
        print("Usuario no encontrado.")
    else:
        escribir_archivo_csv(new_data)
        print("Usuario eliminado con éxito.")

def obtener_card_id_rfid():
    print("Esperando una tarjeta...")
    card_id, text = lector_1.read()
    card_id = str(card_id).strip()
    print(f"Tarjeta leída: {card_id}")
    return card_id

def menu():
    """Muestra el menú principal y gestiona las opciones seleccionadas."""
    while True:
        print("\n--- Control de Acceso ---")
        print("1. Consultar por CARD_ID")
        print("2. Agregar usuario")
        print("3. Modificar usuario")
        print("4. Eliminar usuario")
        print("5. Consultar todos los usuarios")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            print("1. Ingresar CARD_ID manualmente")
            print("2. Obtener CARD_ID a través del módulo RFID")
            sub_opcion = input("Seleccione una opción: ")
            if sub_opcion == '1':
                card_id = input("Ingrese el CARD_ID: ")
            elif sub_opcion == '2':
                card_id = obtener_card_id_rfid()
                print(f"CARD_ID obtenido: {card_id}")
            else:
                print("Opción inválida.")
                continue
            consultar_por_card_id(card_id)

        elif opcion == '2':
            print("1. Ingresar CARD_ID manualmente")
            print("2. Obtener CARD_ID a través del módulo RFID")
            sub_opcion = input("Seleccione una opción: ")
            if sub_opcion == '1':
                card_id = input("Ingrese el CARD_ID: ")
            elif sub_opcion == '2':
                card_id = obtener_card_id_rfid()
                print(f"CARD_ID obtenido: {card_id}")
            else:
                print("Opción inválida.")
                continue
            name = input("Ingrese el nombre: ")
            dni = input("Ingrese el DNI: ")
            agregar_usuario(card_id, name, dni)

        elif opcion == '3':
            card_id = input("Ingrese el CARD_ID del usuario a modificar: ")
            modificar_usuario(card_id)

        elif opcion == '4':
            print("1. Ingresar CARD_ID manualmente")
            print("2. Obtener CARD_ID a través del módulo RFID")
            sub_opcion = input("Seleccione una opción: ")
            if sub_opcion == '1':
                card_id = input("Ingrese el CARD_ID: ")
            elif sub_opcion == '2':
                card_id = obtener_card_id_rfid()
                print(f"CARD_ID obtenido: {card_id}")
            else:
                print("Opción inválida.")
                continue
            eliminar_usuario(card_id)

        elif opcion == '5':
            data = leer_archivo_csv()
            mostrar_datos(data)

        elif opcion == '6':
            print("Saliendo del programa.")
            break

        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()