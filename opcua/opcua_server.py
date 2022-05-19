from opcua import Server
from random import randint
import time


server = Server()
url = "opc.tcp://0.0.0.0:4840"
server.set_endpoint(url)
name = "Industrial Internet of Things"
add_space = server.register_namespace(name)

node = server.get_objects_node()
param = node.add_object(add_space, "Parameters")

temp = param.add_variable(add_space, "Temperature", 0)
press = param.add_variable(add_space, "Pressure", 0)
hgt = param.add_variable(add_space, "Level", 0)

temp.set_writable()
press.set_writable()
hgt.set_writable()

server.start()
print("Server started at {}".format(url))

while True:
    temperature = randint(95, 100)
    pressure = randint(1500, 1600)
    height = randint(100, 103)
    print(temperature, pressure, height)

    temp.set_value(temperature)
    press.set_value(pressure)
    hgt.set_value(pressure)

    time.sleep(3)

