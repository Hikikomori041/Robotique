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

touch_sensor_in1 = TouchSensor(INPUT_1)
ultrasonic_sensor_in4 = UltrasonicSensor(INPUT_4)


# Here is where your code starts

coords = None
num = None

spkr.play_tone(400, 0.1, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
coords = []
num = 0
time.sleep(500 / 1000)
while not touch_sensor_in1.is_pressed:
    num += 1
    tank_drive.on(60, 60)
    print(str(str(num) + ': ') + str(ultrasonic_sensor_in4.distance_centimeters))
    coords.append(ultrasonic_sensor_in4.distance_centimeters)
tank_drive.off(brake=True)
spkr.play_tone(400, 0.1, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
print(coords)