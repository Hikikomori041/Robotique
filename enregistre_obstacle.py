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

motorC = LargeMotor(OUTPUT_C) # Magnet

# Here is where your code starts

import math

robot_y = None
robot_x = None
coords = None
obstacle = None


spkr.play_tone(400, 0.1, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
coords = []
robot_x = 0
robot_y = 0
time.sleep(500 / 1000)
while not touch_sensor_in1.is_pressed:
    robot_y += 5.5
    tank_drive.on(SpeedRPS(1), SpeedRPS(1))
    distance = round(ultrasonic_sensor_in4.distance_centimeters)
    if distance < 255:
        obstacle = [robot_x + distance, robot_y]
        print(str('Obstacle: ' + str(str(robot_x + distance) + ', ')) + str(robot_y))
        coords.append(obstacle)
tank_drive.off(brake=True)
spkr.play_tone(400, 0.1, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
print('Liste des coordonnees des obstacles' + str(coords))
