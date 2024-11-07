#include <WiFi.h>
#include <HTTPClient.h>
#include <SD.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 5       // Pin de selección para el módulo RC522
#define RST_PIN 22     // Pin de reinicio para el módulo RC522
#define RELAY1_PIN 25  // Pin para el relé 1 (puerta 1)
#define RELAY2_PIN 26  // Pin para el relé 2 (puerta 2)
#define SD_CS_PIN 13   // Pin de selección para la tarjeta SD

const char* ssid = "TuSSID"; // Reemplaza con tu red Wi-Fi
const char* password = "TuPassword"; // Reemplaza con tu contraseña Wi-Fi
const char* fileURL = "http://example.com/autorizadas.txt"; // URL del archivo

MFRC522 rfid(SS_PIN, RST_PIN);
File sdFile;
String authorizedCards[50]; // Arreglo para almacenar tarjetas autorizadas
int cardCount = 0;

void setup() {
  Serial.begin(115200);
  SPI.begin();
  rfid.PCD_Init();
  pinMode(RELAY1_PIN, OUTPUT);
  pinMode(RELAY2_PIN, OUTPUT);
  digitalWrite(RELAY1_PIN, LOW);
  digitalWrite(RELAY2_PIN, LOW);

  // Conectar a Wi-Fi
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

  // Descargar y actualizar la lista de tarjetas autorizadas desde la nube
  updateAuthorizedListFromCloud();

  // Cargar tarjetas autorizadas desde el archivo
  loadAuthorizedCards();

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

  // Mostrar UID de la tarjeta leída
  Serial.print("UID de la tarjeta: ");
  String cardID = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    Serial.print(rfid.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(rfid.uid.uidByte[i], HEX);
    cardID += String(rfid.uid.uidByte[i], HEX);
  }
  Serial.println();

  // Validar el acceso
  if (isAuthorized(cardID)) {
    Serial.println("Acceso autorizado");
    openDoor(RELAY1_PIN);
  } else {
    Serial.println("Acceso denegado");
  }

  delay(1000);
  rfid.PICC_HaltA();
}

void updateAuthorizedListFromCloud() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(fileURL);
    int httpResponseCode = http.GET();

    if (httpResponseCode == 200) {
      String payload = http.getString();
      Serial.println("Archivo descargado desde la nube");

      // Guardar el archivo en la tarjeta SD
      sdFile = SD.open("/autorizadas.txt", FILE_WRITE);
      if (sdFile) {
        sdFile.println(payload); // Escribe el contenido descargado en el archivo
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

void loadAuthorizedCards() {
  sdFile = SD.open("/autorizadas.txt");
  if (!sdFile) {
    Serial.println("No se pudo abrir el archivo de tarjetas autorizadas");
    return;
  }

  Serial.println("Cargando tarjetas autorizadas...");
  while (sdFile.available() && cardCount < 50) {
    String card = sdFile.readStringUntil('\n');
    card.trim();
    if (card.length() > 0) {
      authorizedCards[cardCount] = card;
      cardCount++;
      Serial.println("Tarjeta cargada: " + card);
    }
  }
  sdFile.close();
}

bool isAuthorized(String cardID) {
  for (int i = 0; i < cardCount; i++) {
    if (cardID.equalsIgnoreCase(authorizedCards[i])) {
      return true;
    }
  }
  return false;
}

void openDoor(int relayPin) {
  digitalWrite(relayPin, HIGH);
  delay(5000);
  digitalWrite(relayPin, LOW);
}
