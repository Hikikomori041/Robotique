#!/usr/bin/env python3

# Import the necessary libraries
import time
import math
from ev3dev2.motor import *
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor.virtual import *

# Create the sensors and motors objects
motorA = LargeMotor(OUTPUT_A)
motorB = LargeMotor(OUTPUT_B)
left_motor = motorA
right_motor = motorB
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)

spkr = Sound()
btn = Button()
radio = Radio()

ultrasonic_sensor_in1 = UltrasonicSensor(INPUT_1)
gyro_sensor_in2 = GyroSensor(INPUT_2)
gps_sensor_in3 = GPSSensor(INPUT_3)
pen_in4 = Pen(INPUT_4)
touch_sensor_in5 = TouchSensor(INPUT_5)

motorC = LargeMotor(OUTPUT_C) # Magnet

# Here is where your code starts

import math

robot_y = None
robot_x = None
coords = None
obstacle = None


spkr.play_tone(400, 0.1, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
gyro_sensor_in2.reset()
coords = []
robot_x = 0
robot_y = 0
time.sleep(500 / 1000)
while not touch_sensor_in5.is_pressed:
    robot_y += 5.5
    tank_drive.on(SpeedRPS(1), SpeedRPS(1))
    if ultrasonic_sensor_in1.distance_centimeters < 255:
        obstacle = [robot_x + round(ultrasonic_sensor_in1.distance_centimeters), robot_y, None]
        print(str('Obstacle: ' + str(str(robot_x + round(ultrasonic_sensor_in1.distance_centimeters)) + ', ')) + str(robot_y))
        coords.append(obstacle)
tank_drive.off(brake=True)
spkr.play_tone(400, 0.1, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
print('Liste des coordonnées des obstacles' + str(coords))
