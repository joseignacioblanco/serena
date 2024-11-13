import csv
from tkinter import *
from tkinter import messagebox

def consultar_usuario(archivo, card_id):
    with open(archivo, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == card_id:
                return f"Nombre: {row[1]}, DNI: {row[2]}"
        return "Usuario no encontrado."

def consultar_todos_usuarios(archivo):
    with open(archivo, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Saltar la cabecera si existe
        usuarios = list(reader)
        if not usuarios:
            return "No hay usuarios registrados."
        resultado = "\n".join(f"ID: {row[0]}, Nombre: {row[1]}, DNI: {row[2]}" for row in usuarios)
        return resultado

def modificar_usuario(archivo, card_id, nuevo_nombre, nuevo_dni):
    with open(archivo, 'r') as csvfile, open('temp.csv', 'w', newline='') as temp:
        reader = csv.reader(csvfile)
        writer = csv.writer(temp)
        encontrado = False
        for row in reader:
            if row[0] == card_id:
                row[1] = nuevo_nombre
                row[2] = nuevo_dni
                encontrado = True
            writer.writerow(row)
    import os
    os.remove(archivo)
    os.rename('temp.csv', archivo)
    return "Usuario modificado correctamente" if encontrado else "Usuario no encontrado"

def eliminar_usuario(archivo, card_id):
    with open(archivo, 'r') as csvfile, open('temp.csv', 'w', newline='') as temp:
        reader = csv.reader(csvfile)
        writer = csv.writer(temp)
        encontrado = False
        for row in reader:
            if row[0] != card_id:
                writer.writerow(row)
            else:
                encontrado = True
        import os
        os.remove(archivo)
        os.rename('temp.csv', archivo)
        return "Usuario eliminado correctamente" if encontrado else "Usuario no encontrado"

def agregar_usuario(archivo, card_id, nombre, dni):
    with open(archivo, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([card_id, nombre, dni])
    return "Usuario agregado correctamente"

def mostrar_resultado(resultado):
    resultado_label.config(text=resultado)

def procesar_consulta():
    card_id = entry_card_id.get()
    resultado = consultar_usuario(archivo_csv, card_id)
    mostrar_resultado(resultado)

def procesar_consulta_todos():
    resultado = consultar_todos_usuarios(archivo_csv)
    mostrar_resultado(resultado)

def procesar_modificacion():
    card_id = entry_card_id.get()
    nuevo_nombre = entry_nombre.get()
    nuevo_dni = entry_dni.get()
    resultado = modificar_usuario(archivo_csv, card_id, nuevo_nombre, nuevo_dni)
    mostrar_resultado(resultado)

def procesar_eliminacion():
    card_id = entry_card_id.get()
    resultado = eliminar_usuario(archivo_csv, card_id)
    mostrar_resultado(resultado)

def procesar_agregacion():
    card_id = entry_card_id.get()
    nombre = entry_nombre.get()
    dni = entry_dni.get()
    resultado = agregar_usuario(archivo_csv, card_id, nombre, dni)
    mostrar_resultado(resultado)

# Crear la ventana principal
ventana = Tk()
ventana.title("Gestor de Usuarios")

# Crear los elementos de la interfaz
# ... (como en la versión anterior)

# Botones
boton_consultar = Button(ventana, text="Consultar", command=procesar_consulta)
boton_consultar_todos = Button(ventana, text="Consultar Todos", command=procesar_consulta_todos)
boton_modificar = Button(ventana, text="Modificar", command=procesar_modificacion)
boton_eliminar = Button(ventana, text="Eliminar", command=procesar_eliminacion)
boton_agregar = Button(ventana, text="Agregar", command=procesar_agregacion)

# Label para mostrar mensajes
resultado_label = Label(ventana, text="", wraplength=300)

# Colocar los elementos en la ventana
# ... (utilizar grid, pack o place)

# Bucle principal de la ventana
ventana.mainloop()