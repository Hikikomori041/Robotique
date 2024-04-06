#!/usr/bin/env python3

# Import the necessary libraries
import time
import math
from ev3dev2.motor import *
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor.virtual import * # utilisé par le simulateur, à commenter pour une exécution réelle


# Les 4 directions possibles du robot
class Direction(object):
    HAUT = 1
    DROITE = 2
    BAS = 3
    GAUCHE = 4


# Inputs et outputs du robot
spkr = Sound()
btn = Button()


# Moteurs
roueGauche = OUTPUT_A # A dans le simulateur, B dans le réel
roueDroite = OUTPUT_B # B dans le simulateur, C dans le réel
left_motor = LargeMotor(roueGauche)
right_motor = LargeMotor(roueDroite)
tank_drive = MoveTank(roueGauche, roueDroite)
steering_drive = MoveSteering(roueGauche, roueDroite)


# Capteurs
ultrasonic_sensor = UltrasonicSensor(INPUT_4)
touch_sensor = TouchSensor(INPUT_1)



#-------------------------------------------
#               Programme
#-------------------------------------------
diametreRoue = 5.6 #cm
circonferenceRoue = round(diametreRoue * math.pi, 2)

direction = Direction.HAUT
robot_x = None
robot_y = None
coords = None
obstacle = None


spkr.play_tone(400, 0.1, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
coords = []
robot_x = 0
robot_y = 0
time.sleep(500 / 1000)
while not touch_sensor.is_pressed:
    distance = round(ultrasonic_sensor.distance_centimeters)
    robot_y += round(circonferenceRoue, 2)
    tank_drive.on(SpeedRPS(1), SpeedRPS(1))
    if distance < 255:
        # Le capteur US a détecté quelque chose sur la droite du robot
        if(direction == Direction.HAUT):
            x = round(robot_x + distance, 2)
            y = round(robot_y, 2)
        else:
            print("DIRECTION NON GÉRÉE: " + str(direction))
        obstacle = [x, y]
        print('Obstacle: ' + str(x) + ', ' + str(y))
        coords.append(obstacle)
tank_drive.off(brake=True)
spkr.play_tone(400, 0.1, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
print('Liste des coordonnées des obstacles' + str(coords))