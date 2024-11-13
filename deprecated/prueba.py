#! /usr/bin/python3

# Este es el shebang para que se ejecute como script de python.

'''from modulo1 import *

print("mondongo")


def main():
    print("mondongo del mein")
    saluda("mondongo")'''


from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
try:
    while True:
        id, text = reader.read()
        print(id)
        print(text)
finally:
    GPIO.cleanup()
if __name__ == "__main__":
    main()
