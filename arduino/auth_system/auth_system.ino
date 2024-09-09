#include <LiquidCrystal_PCF8574.h>
#include <Wire.h>
#include <SPI.h>
#include <MFRC522.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <Servo.h>

// Connections
#define SV_PIN  D4
#define SS_PIN  D3 
#define RST_PIN D0
#define SDA_PIN D2
#define SCL_PIN D1 

// Objects
Servo servo;
MFRC522 rfid(SS_PIN, RST_PIN);
LiquidCrystal_PCF8574 lcd(0x27);

WiFiClient client;
HTTPClient http;
String card_id;

// Constants
const char* SSID         = "iliadbox-615C99";
const char* PASSWORD     = "";
const String SERVER_ADDR = "192.168.1.31:5000";
const String MASTER_KEY  = "CB4B8922";


void setup_wifi() 
{
  delay(10);

  Serial.println("[+] Connecting to " + String(SSID));

  WiFi.begin(SSID, PASSWORD);
  
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print("[-] Reconnecting...");
    delay(500);
  }
  
  Serial.println("[+] WiFi Connected");
  Serial.print("[+] IP Address: ");
  Serial.println(WiFi.localIP());
}

void check_wifi() 
{
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[!] WiFi connection lost. Reconnecting...");
    setup_wifi();
  }
}

bool send_auth_request(String card_id) 
{
  bool is_auth = false;

  String url = "http://" + SERVER_ADDR + "/api/v1/users/access_rfid?uid=" + card_id;

  http.begin(client, url);

  if (http.GET() == 200) {
    is_auth = true;
  }

  delay(100);
  http.end();

  return is_auth;
}

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
  Wire.begin(SDA_PIN, SCL_PIN);
  lcd.begin(16, 2);
  servo.attach(SV_PIN);
  setup_wifi();
  
  lcd.setBacklight(255);
  servo.write(0);
  print_on_lcd("Place key");
}

void loop()
{
  check_wifi();
  
  if (rfid.PICC_IsNewCardPresent()) 
  { 
    if (rfid.PICC_ReadCardSerial()) 
    {
      // Check if the card is supported      
      if (rfid.PICC_GetType(rfid.uid.sak) != MFRC522::PICC_TYPE_MIFARE_1K)
        print_on_lcd("Access denied");
      else 
      {
        // Read tag uid
        card_id = "";
        for (byte i = 0; i < rfid.uid.size; i++) {;
          card_id += String(rfid.uid.uidByte[i], HEX);
        }

        card_id.toUpperCase();

        if (card_id == MASTER_KEY) {
          print_on_lcd("Access granted");
          servo.write(130);
        } else if (send_auth_request(card_id)) {
          print_on_lcd("Access granted");
          servo.write(130);
        } else {
          print_on_lcd("Access denied");
        }
      }

      // Break communication
      rfid.PICC_HaltA();
      rfid.PCD_StopCrypto1();

      delay(10000);
      
      servo.write(0);
      print_on_lcd("Place key");
    }
  }
}
