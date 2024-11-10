print("mondongo")


def main():
    print("Sistema de Control de Acceso Iniciado.")
    while True:
        try:
            print("Esperando una tarjeta...")
            card_id, text = reader.read()
            card_id = str(card_id).strip()
            print(f"Tarjeta leída: {card_id}")

            if card_id == MASTER_CARD_UID:
                print("Tarjeta maestra detectada. Actualizando la lista de autorizadas desde la nube...")
                download_file_from_cloud()
            else:
                if is_card_authorized(card_id):
                    print("Acceso permitido.")
                    activate_relay()  # Activar el relé para abrir la puerta
                else:
                    print("Acceso denegado.")
                    # Aquí puedes agregar lógica para alarmas, etc.

            time.sleep(2)  # Retardo para evitar lecturas múltiples rápidas

        except KeyboardInterrupt:
            print("\nSaliendo del sistema.")
            break
        finally:
            GPIO.cleanup()
