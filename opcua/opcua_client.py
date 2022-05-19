from opcua import Client
import time

url = "opc.tcp://localhost:4840"
client = Client(url)
client.connect()

while True:
    temp = client.get_node("ns=2;i=2")
    press = client.get_node("ns=2;i=3")
    hgt = client.get_node("ns=2;i=4")
    temperature = temp.get_value()
    pressure = press.get_value()
    height = hgt.get_value()
    print(temperature, pressure, height)
    time.sleep(2)