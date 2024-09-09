#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <DHT.h>
#include <PubSubClient.h>
#include <LittleFS.h>
#include <TZ.h>
#include <FS.h>
#include <CertStoreBearSSL.h>

// Connections
#define DHT_PIN D3
#define DHT_TYPE DHT11
#define PIR_PIN D2
#define ALARM_PIN D6
#define LED_PIN D7

// Objects
DHT dht(DHT_PIN, DHT_TYPE);
PubSubClient *mqtt_client;
CertStore certStore;

// Constants
const char* SSID      = "iliadbox-615C99";
const char* PASSWORD  = "";

const char* MQTT_ADDR = "49ded85c25e645a7ba547aee781d2231.s1.eu.hivemq.cloud";
const int   MQTT_PORT = 8883;
const char* MQTT_USER = "darkknight";
const char* MQTT_PWD  = "ie6fLMLc2D!LVT^r##";

const char* TOPIC_INTR  = "/server/intrusion";   // Subscribe
const char* TOPIC_ALARM = "/server/alarm";       // Subscribe
const char* TOPIC_DET   = "/server/detection";   // Publish
const char* TOPIC_TEMP  = "/server/temperature"; // Publish

bool intrusion_system_state = false;
bool alarm_state            = false;

/* ------------
 * Wi-Fi Utils
 * ------------ */
void setup_wifi() 
{
  delay(10);

  Serial.println("[+] Connecting to " + String(SSID));

  WiFi.begin(SSID, PASSWORD);
  
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("[-] Reconnecting...");
    delay(500);
  }

  randomSeed(micros());
  
  Serial.println("[+] WiFi Connected");
  Serial.print("[+] IP Address: ");
  Serial.println(WiFi.localIP());
}

void check_wifi() 
{
  if (WiFi.status() != WL_CONNECTED)
    setup_wifi();
}

/* -----------
 * MQTT Utils
 * ----------- */
void setDateTime() 
{
  configTime(TZ_Europe_Berlin, "pool.ntp.org", "time.nist.gov");

  Serial.print("[+] Waiting for NTP time sync: ");
  time_t now = time(nullptr);
  while (now < 8 * 3600 * 2) {
    delay(100);
    Serial.print(".");
    now = time(nullptr);
  }
  Serial.println();

  struct tm timeinfo;
  gmtime_r(&now, &timeinfo);
  Serial.printf("[+] %s %s", tzname[0], asctime(&timeinfo));
}

void setup_mqtt()
{  
  while (!mqtt_client->connected()) {
    String client_id = "ESP8266-";
    client_id += String(random(0xffff), HEX);

    if (mqtt_client->connect(client_id.c_str(), MQTT_USER, MQTT_PWD)) {
      Serial.println("[+] MQTT Connected");

      mqtt_client->subscribe(TOPIC_ALARM);
      mqtt_client->subscribe(TOPIC_INTR);
    } else {
      Serial.print("[-] Failed, rc=");
      Serial.println(mqtt_client->state());
      Serial.println("[-] Try again now");
    }
  }
}

void check_mqtt()
{
  if(!mqtt_client->connected())
    setup_mqtt();
}

void mqtt_callback(char* topic, byte* payload, unsigned int length) 
{
  String message;
  
  for (int i = 0; i < length; i++)
    message += (char)payload[i];

  if (String(topic) == TOPIC_ALARM && message == "0") {
    alarm_state = false;
    digitalWrite(ALARM_PIN, LOW);
  }

  if (String(topic) == TOPIC_INTR)
    if (message == "1") {
      intrusion_system_state = true;
      digitalWrite(LED_PIN, HIGH);
    } else {
      intrusion_system_state = false;
      alarm_state  = false;
      digitalWrite(LED_PIN, LOW);
    }
}

/* -----------------
 * Components utils
 * ----------------- */
void get_temperature()
{
  float value = dht.readTemperature();
  if (!isnan(value))
    mqtt_client->publish(TOPIC_TEMP, String(value).c_str());
}

void check_intrusion() 
{
  // If the an intrusion is detected the it can be 
  // deactivated only through the web interface 
  if (!alarm_state && intrusion_system_state) {
    int pir_value = digitalRead(PIR_PIN);

    if (pir_value == HIGH) {
      alarm_state = true;
      mqtt_client->publish(TOPIC_DET, String("1").c_str());      
      tone(ALARM_PIN, 440);
    }
  }

  // Disable the alarm if the system is disabled
  if (!intrusion_system_state)
    digitalWrite(ALARM_PIN, LOW);
}


void setup() 
{
  // Components setup
  Serial.begin(9600);
  pinMode(PIR_PIN, INPUT);
  pinMode(ALARM_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  dht.begin();
  
  setup_wifi();

  // Wi-Fi Client with TLS
  LittleFS.begin();
  setDateTime();
  certStore.initCertStore(LittleFS, PSTR("/certs.idx"), PSTR("/certs.ar"));
  WiFiClientSecure *bear = new WiFiClientSecure();
  bear->setCertStore(&certStore);
  mqtt_client = new PubSubClient(*bear);

  // Connect to MQTT broker
  mqtt_client->setServer(MQTT_ADDR, MQTT_PORT);
  mqtt_client->setCallback(mqtt_callback);

  // Initial components config
  digitalWrite(ALARM_PIN, LOW);
}

void loop() 
{
  check_wifi();
  check_mqtt();

  mqtt_client->loop();

  get_temperature();
  check_intrusion();

  delay(2000);
}
