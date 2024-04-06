#!/usr/bin/env python3

from ev3dev2.motor import *
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *


motorA = LargeMotor(OUTPUT_B)
motorB = LargeMotor(OUTPUT_C)
left_motor = motorA
right_motor = motorB
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)

spkr = Sound()
btn = Button()

touch_sensor_in1 = TouchSensor(INPUT_1)
us_sensor_in4 = UltrasonicSensor(INPUT_4)

spkr.play_tone(400, 0.1)
left_motor.position = 0
right_motor.position = 0

tank_drive.on_for_degrees(0,50,360) #on fait un tour complet pour observer les alentours
while not touch_sensor_in1.is_pressed:
    tank_drive.on(50, 50)
#tank_drive.off(brake=True)
tank_drive.on(-50, -50) #on recule
tank_drive.on_for_degrees(50,0,90) #on tourne a gauche
while not touch_sensor_in1.is_pressed:
    tank_drive.on(10, 10)
    if us_sensor_in4.distance_centimeters == 255: #on a plus rien a droite
        tank_drive.on(50,50) #on avance pour ne pas heurter l'obstacle
        tank_drive.on_for_degrees(0,50,90) #on tourne a droite
spkr.play_tone(400, 0.1)