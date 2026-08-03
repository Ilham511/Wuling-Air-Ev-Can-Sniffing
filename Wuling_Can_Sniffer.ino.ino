#include <SPI.h>
#include <mcp_can.h>

const int SPI_CS_PIN = 5;
const int LED_PIN = 2; // Lampu biru bawaan ESP32
MCP_CAN CAN(SPI_CS_PIN);

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
  
  // Jeda 3 detik agar Serial Monitor siap
  delay(3000); 
  
  // Tes kedip lampu 3x saat mulai
  for(int i=0; i<3; i++) {
    digitalWrite(LED_PIN, HIGH); delay(200);
    digitalWrite(LED_PIN, LOW); delay(200);
  }

  Serial.println("\n======================================");
  Serial.println("   CAPSTONE PROJECT: WULING MONITOR   ");
  Serial.println("======================================");
  Serial.println("Status: Program Berhasil Dimulai!");

  /* * CATATAN KRISTAL:
   * Kalau modul birumu tulisannya 16.000 -> ganti MCP_8MHZ jadi MCP_16MHZ
   */
  Serial.println("Sedang mencari Modul MCP2515...");
  
  while (CAN.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) != CAN_OK) {
    Serial.println("HASIL: Modul TIDAK TERDETEKSI (Cek Kabel/Power)");
    digitalWrite(LED_PIN, !digitalRead(LED_PIN)); // Lampu kedip lambat tanda error
    delay(2000);
  }
  
  Serial.println("HASIL: Modul BERHASIL Konek!");
  digitalWrite(LED_PIN, HIGH); // Lampu nyala terus tanda siap
  
  CAN.setMode(MCP_LISTENONLY);
  Serial.println("Mode: Monitoring (Listen Only) Aktif...");
}

void loop() {
  long unsigned int rxId;
  unsigned char len = 0;
  unsigned char rxBuf[8];

  if (CAN_MSGAVAIL == CAN.checkReceive()) {
    CAN.readMsgBuf(&rxId, &len, rxBuf);

    Serial.print("ID:0x");
    Serial.print(rxId, HEX);
    Serial.print(",");

    for (int i = 0; i < len; i++) {
      if (rxBuf[i] < 0x10) Serial.print("0");
      Serial.print(rxBuf[i], HEX);
      if (i < len - 1) Serial.print(" ");
    }
    Serial.println();
  }
}
