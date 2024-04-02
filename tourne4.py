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
motorA = LargeMotor(OUTPUT_A)
motorB = LargeMotor(OUTPUT_B)
left_motor = motorA
right_motor = motorB
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)

spkr = Sound()
btn = Button()

ultrasonic_sensor_in1 = UltrasonicSensor(INPUT_1)

# Here is where your code starts

spkr.play_tone(400, 0.1)
# spkr.speak("J ai les cramptes")
left_motor.position = 0
right_motor.position = 0
for count in range(10):
    time.sleep(500 / 1000)
    tank_drive.on_for_seconds(50, 50, 1)
    tank_drive.off(brake=True)
    time.sleep(1)
    tank_drive.on_for_seconds(0, 49, 1)
spkr.play_tone(400, 0.1)
