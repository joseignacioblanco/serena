#include <WiFi.h>
#include <HTTPClient.h>
#include <SD.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 5       // Pin de selección para el módulo RC522
#define RST_PIN 22     // Pin de reinicio para el módulo RC522
#define SD_CS_PIN 13   // Pin de selección para la tarjeta SD

const char* ssid = "TuSSID"; // Reemplaza con tu red Wi-Fi
const char* password = "TuPassword"; // Reemplaza con tu contraseña Wi-Fi
const char* fileURL = "https://drive.google.com/uc?export=download&id=1A2B3C4D5E6F7G8H9"; // Reemplaza con tu enlace de descarga directa

MFRC522 rfid(SS_PIN, RST_PIN);
String masterCardUID = "12ab34cd56"; // UID de la llave RFID maestra

void setup() {
  Serial.begin(115200);
  SPI.begin();
  rfid.PCD_Init();
  
  // Conexión Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Conectando a Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado a Wi-Fi");

  // Inicializar la tarjeta SD
  if (!SD.begin(SD_CS_PIN)) {
    Serial.println("Error al inicializar la tarjeta SD");
    while (true);
  }
  Serial.println("Tarjeta SD inicializada correctamente");

  Serial.println("Sistema de Control de Acceso Iniciado");
}

void loop() {
  // Comprobar si hay una nueva tarjeta presente
  if (!rfid.PICC_IsNewCardPresent()) {
    return;
  }

  // Intentar leer la tarjeta
  if (!rfid.PICC_ReadCardSerial()) {
    return;
  }

  // Obtener el UID de la tarjeta leída
  String cardID = getCardUID();

  // Verificar si es la tarjeta maestra
  if (cardID.equalsIgnoreCase(masterCardUID)) {
    Serial.println("Tarjeta maestra detectada. Actualizando la lista desde Google Drive...");
    updateAuthorizedListFromCloud();
  } else {
    Serial.println("Tarjeta leída: " + cardID);
    // Aquí puedes agregar la lógica para validar y autorizar acceso si no es la tarjeta maestra
  }

  delay(1000); // Breve retardo para evitar múltiples lecturas seguidas
  rfid.PICC_HaltA();
}

String getCardUID() {
  String cardID = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    cardID += String(rfid.uid.uidByte[i], HEX);
  }
  return cardID;
}

void updateAuthorizedListFromCloud() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(fileURL); // Enlace de descarga directa de Google Drive
    int httpResponseCode = http.GET();

    if (httpResponseCode == 200) {
      String payload = http.getString();
      Serial.println("Archivo descargado desde Google Drive");

      // Guardar el archivo en la tarjeta SD
      File sdFile = SD.open("/autorizadas.txt", FILE_WRITE);
      if (sdFile) {
        sdFile.println(payload);
        sdFile.close();
        Serial.println("Archivo actualizado en la tarjeta SD");
      } else {
        Serial.println("Error al abrir el archivo para escribir");
      }
    } else {
      Serial.print("Error al descargar el archivo. Código de respuesta: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("Wi-Fi no conectado");
  }
}
