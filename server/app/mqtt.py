from flask import Flask
from app.models.mongo import Temperature, IntrusionSystem
import string
import random
import paho.mqtt.client as mqtt


def record_temp(message):
    Temperature.add_measure(
        float(message.payload.decode('utf-8'))
    )

def record_detection(message):
    IntrusionSystem.add_alarm_log(
        message.payload.decode('utf-8') == '1'
    )
    
def on_message(client, userdata, message):
    if userdata["detection"] == message.topic:
        record_detection(message)
    elif userdata["temp"] == message.topic:
        record_temp(message)

class MqttHandler:
    def __init__(self):
        self.handler         = None
        self.topic_detection = None
        self.topic_temp      = None
        self.topic_intrusion = None
        self.topic_alarm     = None

    def init_mqtt(self, app: Flask):
        self.topic_detection = app.config["MQTT_SETTINGS"]["topics"]["detection"]
        self.topic_temp      = app.config["MQTT_SETTINGS"]["topics"]["temp"]
        self.topic_intrusion = app.config["MQTT_SETTINGS"]["topics"]["intrusion"]
        self.topic_alarm     = app.config["MQTT_SETTINGS"]["topics"]["alarm"]

        client = mqtt.Client(
            client_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16)), 
            protocol  = mqtt.MQTTv5
        )
        client.tls_set(tls_version = mqtt.ssl.PROTOCOL_TLS)
        client.username_pw_set(
            app.config["MQTT_SETTINGS"]["user"], 
            app.config["MQTT_SETTINGS"]["pass"]
        )
        client.connect(
            app.config["MQTT_SETTINGS"]["addr"], 
            app.config["MQTT_SETTINGS"]["port"]
        )

        client.on_message = on_message

        client.subscribe(self.topic_detection)
        client.subscribe(self.topic_temp)

        client.user_data_set({
            "detection": self.topic_detection,
            "temp"     : self.topic_temp
        })

        client.loop_start()

        self.handler = client

    def disable_alarm(self):
        self.handler.publish(
            self.topic_alarm,
            '0'
        )

    def enable_intrusion_system(self):
        self.handler.publish(
            self.topic_intrusion,
            '1'
        )

    def disable_intrusion_system(self):
        self.handler.publish(
            self.topic_intrusion,
            '0'
        )

mqtt_handler = MqttHandler()