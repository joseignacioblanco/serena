#include <SoftwareSerial.h>

SoftwareSerial mySerial(10, 11); // RX, TX

void setup() {
    Serial.begin(9600); // Inicia la comunicación serie con el PC
    mySerial.begin(9600); // Inicia la comunicación serie con el lector RFID
}

void loop() {
    if (mySerial.available()) {
        String rfidData = "";
        while (mySerial.available()) {
            char c = mySerial.read();
            rfidData += c;
        }
        Serial.println("Datos recibidos del lector RFID: " + rfidData);
    }
}
