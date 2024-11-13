import csv
VINCULATION_FILE = "/home/pi/Documents/serena/vinculacion.csv"

def mostrar_menu():
    print("Menú:")
    print("1. Consultar usuario")
    print("2. Modificar usuario")
    print("3. Eliminar usuario")
    print("4. Agregar usuario")
    print("5. Salir")

def consultar_usuario(archivo, card_id):
    with open(archivo, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == card_id:
                print("Nombre:", row[1])
                print("DNI:", row[2])
                return
        print("Usuario no encontrado.")

def modificar_usuario(archivo, card_id, nuevo_nombre, nuevo_dni):
    with open(archivo, 'r') as csvfile, open('temp.csv', 'w', newline='') as temp:
        reader = csv.reader(csvfile)
        writer = csv.writer(temp)
        for row in reader:
            if row[0] == card_id:
                row[1] = nuevo_nombre
                row[2] = nuevo_dni
            writer.writerow(row)
    import os
    os.remove(archivo)
    os.rename('temp.csv', archivo)

def eliminar_usuario(archivo, card_id):
    with open(archivo, 'r') as csvfile, open('temp.csv', 'w', newline='') as temp:
        reader = csv.reader(csvfile)
        writer = csv.writer(temp)
        for row in reader:
            if row[0] != card_id:
                writer.writerow(row)
    import os
    os.remove(archivo)
    os.rename('temp.csv', archivo)

def agregar_usuario(archivo, card_id, nombre, dni):
    with open(archivo, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([card_id, nombre, dni])

if __name__ == "__main__":
    archivo_csv = VINCULATION_FILE  # Ajusta el nombre del archivo
    while True:
        mostrar_menu()
        opcion = int(input("Ingrese una opción: "))
        if opcion == 1:
            card_id = input("Ingrese el ID de la tarjeta: ")
            consultar_usuario(archivo_csv, card_id)
        elif opcion == 2:
            card_id = input("Ingrese el ID de la tarjeta a modificar: ")
            nuevo_nombre = input("Ingrese el nuevo nombre: ")
            nuevo_dni = input("Ingrese el nuevo DNI: ")
            modificar_usuario(archivo_csv, card_id, nuevo_nombre, nuevo_dni)
        elif opcion == 3:
            card_id = input("Ingrese el ID de la tarjeta a eliminar: ")
            eliminar_usuario(archivo_csv, card_id)
        elif opcion == 4:
            card_id = input("Ingrese el nuevo ID de la tarjeta: ")
            nombre = input("Ingrese el nombre: ")
            dni = input("Ingrese el DNI: ")
            agregar_usuario(archivo_csv, card_id, nombre, dni)
        elif opcion == 5:
            break
        else:
            print("Opción inválida.")