#!/usr/bin/env python3

# Import the necessary libraries
import time
import math
from ev3dev2.motor import *
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *


# Create the sensors and motors objects
motorA = LargeMotor(OUTPUT_B)
motorB = LargeMotor(OUTPUT_C)
left_motor = motorA
right_motor = motorB
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)

spkr = Sound()
btn = Button()

touch_sensor_in5 = TouchSensor(INPUT_1)


# Here is where your code starts

spkr.play_tone(400, 0.1)
left_motor.position = 0
right_motor.position = 0

while not touch_sensor_in5.is_pressed:
    tank_drive.on(50, 50)
tank_drive.off(brake=True)
spkr.play_tone(800, 0.1)

spkr.play_tone(400, 0.1)
