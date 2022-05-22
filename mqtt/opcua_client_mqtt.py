from opcua import Client
import paho.mqtt.client as mqtt
import time
import json
import psycopg2
import datetime

# Параметры базы данных
DB_HOST = 'ec2-63-32-248-14.eu-west-1.compute.amazonaws.com'
DB_NAME = 'd974frae2u76bq'
DB_USER = 'kemiwygyzjgseg'
DB_PASS = '282e49b00caaf11338cfc6b8c1451c827637eea11348c139860f5c370538c2ec'

# Соединение с OPC UA сервером
url = "opc.tcp://localhost:4840"
client = Client(url)
client.connect()
print("OPC UA Client connected")

# Соединение с Thingsboard через MQTT
iot_hub = "demo.thingsboard.io"
port = 1883
username = "e7UD6nDAzcFpTSu7lW8C"
password = ""
topic = "v1/devices/me/telemetry"

# Соединение с базой данных по нашим данным
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
# Создание курсора
cur = conn.cursor()

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

        cur.execute("INSERT INTO data (id_sensor, date, time, value) VALUES (%s, %s, %s, %s)",
                    (1, datetime.date.today(), time.strftime("%H:%M:%S"), int(temperature)))
        cur.execute("INSERT INTO data (id_sensor, date, time, value) VALUES (%s, %s, %s, %s)",
                    (2, datetime.date.today(), time.strftime("%H:%M:%S"), int(pressure)))
        cur.execute("INSERT INTO data (id_sensor, date, time, value) VALUES (%s, %s, %s, %s)",
                    (3, datetime.date.today(), time.strftime("%H:%M:%S"), int(height)))

        conn.commit()

        time.sleep(2)

    except Exception as e:
        print(e)
