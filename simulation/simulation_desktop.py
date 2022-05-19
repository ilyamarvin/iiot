from tkinter import *
from tkinter.ttk import Checkbutton
from random import randint
from opcua import Server
import time

checkbox = None


def isCheckedTemp():
    if temp_state.get():
        temp = randint(95, 100)
        temp_slider.set(temp)
        root.after(3000, isCheckedTemp)


def postTemp(model):
    temperature = temp_slider.get()
    print(temperature)
    temp.set_value(temperature)


def postPressure(model):
    pressure = press_slider.get()
    print(pressure)
    press.set_value(pressure)


def postLevel(model):
    level = level_slider.get()
    print(level)
    hgt.set_value(level)


def isCheckedPress():
    if press_state.get():
        press = randint(1500, 1600)
        press_slider.set(press)
        root.after(3000, isCheckedPress)


def isCheckedLevel():
    if level_state.get():
        level = randint(100, 110)
        level_slider.set(level)
        root.after(3000, isCheckedLevel)


server = Server()
url = "opc.tcp://localhost:4840"
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


root = Tk()
root.title("Эмулятор данных")

# Температура
temp_frame = LabelFrame(root, text='Температура', padx=20, pady=20)
temp_frame.pack(side=LEFT)

temp_state = BooleanVar()
temp_state.set(False)
temp_check = Checkbutton(temp_frame, text='Автоматический режим работы', var=temp_state, command=isCheckedTemp)
temp_check.grid(row=0)

temp_slider = Scale(temp_frame, from_=0, to=150, tickinterval=25, orient=HORIZONTAL, length=300, command=postTemp)
temp_slider.grid(row=1)

# Давление
press_frame = LabelFrame(root, text='Давление', padx=20, pady=20)
press_frame.pack(side=LEFT)

press_state = BooleanVar()
press_state.set(False)
press_check = Checkbutton(press_frame, text='Автоматический режим работы', var=press_state, command=isCheckedPress)
press_check.grid(row=0)

press_slider = Scale(press_frame, from_=0, to=2000, tickinterval=400, orient=HORIZONTAL, length=300, command=postPressure)
press_slider.grid(row=1)

# Уровень
level_frame = LabelFrame(root, text='Уровень', padx=20, pady=20)
level_frame.pack(side=LEFT)

level_state = BooleanVar()
level_state.set(False)
level_check = Checkbutton(level_frame, text='Автоматический режим работы', var=level_state, command=isCheckedLevel)
level_check.grid(row=0)

level_slider = Scale(level_frame, from_=0, to=120, tickinterval=20, orient=HORIZONTAL, length=300, command=postLevel)
level_slider.grid(row=1)

root.mainloop()
