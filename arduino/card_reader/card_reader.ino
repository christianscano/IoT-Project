#include <LiquidCrystal_PCF8574.h>
#include <SPI.h>
#include <MFRC522.h>

// Connections
#define SS_PIN  D10 
#define RST_PIN D9

// Objects
MFRC522 rfid(SS_PIN, RST_PIN);
LiquidCrystal_PCF8574 lcd(0x27);

String card_id;

void print_on_lcd(String message) 
{
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(message);
}

void setup()
{
  Serial.begin(9600);
  SPI.begin(); 
  rfid.PCD_Init(); 
  lcd.begin(16, 2);
  
  lcd.setBacklight(255);
  print_on_lcd("Place key");
}

void loop()
{
  if (rfid.PICC_IsNewCardPresent()) 
  { 
    if (rfid.PICC_ReadCardSerial()) 
    {
      // Check if the card is supported      
      if (rfid.PICC_GetType(rfid.uid.sak) != MFRC522::PICC_TYPE_MIFARE_1K) 
        print_on_lcd("Not supported");
      else 
      {
        // Read tag uid
        card_id = "";
        for (byte i = 0; i < rfid.uid.size; i++) {;
            card_id += String(rfid.uid.uidByte[i], HEX);
        }

        card_id.toUpperCase();
        print_on_lcd(card_id);

      }
      // Break communication
      rfid.PICC_HaltA();
      rfid.PCD_StopCrypto1();

      delay(10000);
      
      print_on_lcd("Place key");
    }
  }
}
