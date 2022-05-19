from opcua import Client
import paho.mqtt.client as mqtt
import time
import json

url = "opc.tcp://localhost:4840"
client = Client(url)
client.connect()
print("OPC UA Client connected")

iot_hub = "demo.thingsboard.io"
port = 1883
username = "e7UD6nDAzcFpTSu7lW8C"
password = ""
topic = "v1/devices/me/telemetry"

iot_hub_client = mqtt.Client()
iot_hub_client.username_pw_set(username, password)
iot_hub_client.connect(iot_hub, port)
print("Connected to IOT hub")

data = dict()
while True:
    try:
        temp = client.get_node("ns=2;i=2")
        press = client.get_node("ns=2;i=3")
        hgt = client.get_node("ns=2;i=4")
        temperature = temp.get_value()
        pressure = press.get_value()
        height = hgt.get_value()
        print(temperature, pressure, height)

        data["temperature"] = int(temperature)
        data["pressure"] = int(pressure)
        data["height"] = int(height)
        data_out = json.dumps(data)
        iot_hub_client.publish(topic, data_out, 0)

        time.sleep(2)

    except Exception as e:
        print(e)