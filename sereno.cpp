#include <SPI.h>
#include <MFRC522.h>
#include <SD.h>

#define SS_PIN 5      // Pin de selección para el módulo RC522
#define RST_PIN 22    // Pin de reinicio para el módulo RC522
#define RELAY1_PIN 25 // Pin para el relé 1 (puerta 1)
#define RELAY2_PIN 26 // Pin para el relé 2 (puerta 2)
#define SD_CS_PIN 13  // Pin de selección para la tarjeta SD

MFRC522 rfid(SS_PIN, RST_PIN);
File sdFile;
String authorizedCards[50]; // Arreglo para almacenar las tarjetas autorizadas (máximo 50 por ejemplo)
int cardCount = 0;          // Contador de tarjetas leídas desde la SD

void setup() {
  Serial.begin(115200);
  SPI.begin();            // Iniciar comunicación SPI para RFID y SD
  rfid.PCD_Init();        // Iniciar el módulo RFID
  pinMode(RELAY1_PIN, OUTPUT);
  pinMode(RELAY2_PIN, OUTPUT);

  digitalWrite(RELAY1_PIN, LOW); // Inicializar relés en estado apagado
  digitalWrite(RELAY2_PIN, LOW);

  // Iniciar la tarjeta SD
  if (!SD.begin(SD_CS_PIN)) {
    Serial.println("Error al inicializar la tarjeta SD");
    while (true);
  }
  Serial.println("Tarjeta SD inicializada correctamente");

  // Leer la lista de tarjetas autorizadas desde el archivo
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
    openDoor(RELAY1_PIN); // Control de relé 1 (puerta 1)
  } else {
    Serial.println("Acceso denegado");
  }

  delay(1000); // Breve pausa para evitar lecturas repetidas
  rfid.PICC_HaltA(); // Detener comunicación con la tarjeta
}

void loadAuthorizedCards() {
  sdFile = SD.open("/autorizadas.txt");
  if (!sdFile) {
    Serial.println("No se pudo abrir el archivo de tarjetas autorizadas");
    return;
  }

  Serial.println("Cargando tarjetas autorizadas...");
  while (sdFile.available() && cardCount < 50) {
    String card = sdFile.readStringUntil('\n'); // Leer cada línea
    card.trim(); // Eliminar espacios y saltos de línea
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
  delay(5000); // Mantener la puerta abierta durante 5 segundos
  digitalWrite(relayPin, LOW);
}
