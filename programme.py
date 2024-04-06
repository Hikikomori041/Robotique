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
# Fonctions
def changeDirection(cote):
    if (cote == "gauche"):
        if direction == Direction.HAUT:
            return Direction.GAUCHE
        elif direction == Direction.DROITE:
            return Direction.HAUT
        elif direction == Direction.BAS:
            return Direction.DROITE
        elif direction == Direction.GAUCHE:
            return Direction.BAS
    else:
        if direction == Direction.HAUT:
            return Direction.DROITE
        elif direction == Direction.DROITE:
            return Direction.BAS
        elif direction == Direction.BAS:
            return Direction.GAUCHE
        elif direction == Direction.GAUCHE:
            return Direction.HAUT
    return direction


def tourne(cote = "droite"):
    global direction # récupère la variable globale direction
    temps = 1550 / 1000

    if (DEBUG):
        print("Tourne à " + cote)

    if (cote == "gauche"):
        # On tourne à gauche
        steering_drive.on_for_seconds(-90, SpeedRPS(0.5), temps)
    else:
        # On tourne à droite
        steering_drive.on_for_seconds(90, SpeedRPS(0.5), temps)
    tank_drive.off(brake=True)
    time.sleep(150/1000)
    direction = changeDirection(cote)
    return

def recule():
    global robot_x, robot_y # On récupère les coordonnées du robot du programme

    if (DEBUG):
        print("Le robot recule")
    # S'arrête
    tank_drive.off(brake=True)
    spkr.play_tone(800, 0.1, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
    time.sleep(500/1000)
    # Recule
    tank_drive.on_for_seconds(SpeedRPS(1) * -1, SpeedRPS(1) * -1, 1)
    time.sleep(500/1000)

    # Calcul les nouvelles coordonnées du robot
    deplacement = circonferenceRoue
    if(direction == Direction.HAUT):
        robot_y -= deplacement
    elif(direction == Direction.BAS):
        robot_y += deplacement
    elif(direction == Direction.DROITE):
        robot_x -= deplacement
    elif(direction == Direction.GAUCHE):
        robot_x += deplacement

    #todo: verifier dans quelle direction on doit tourner
    tourne("gauche")
    return

def seDeplaceDe(deplacement):
    global robot_x, robot_y # On récupère les coordonnées du robot du programme
    
    if(direction == Direction.HAUT):
        robot_y += deplacement
    elif(direction == Direction.BAS):
        robot_y -= deplacement
    elif(direction == Direction.GAUCHE):
        robot_x -= deplacement
    elif(direction == Direction.DROITE):
        robot_x += deplacement

def avance():
    global robot_x, robot_y # On récupère les coordonnées du robot du programme
    global coords # On utilise la liste en variable globale pour pouvoir l'affecter
    global detecteUnObstacle

    tank_drive.on(SpeedRPS(1), SpeedRPS(1))
    deplacement = circonferenceRoue/30 # On part du principe que le calcul se fait 30 fois par seconde
    seDeplaceDe(deplacement)
    
    distance = ultrasonic_sensor.distance_centimeters
    if distance < 255:
        # Le capteur US a détecté quelque chose sur la droite du robot
        detecteUnObstacle = True
        if(direction == Direction.HAUT):
            x = round(robot_x + distance, 2)
            y = round(robot_y, 2)
        elif(direction == Direction.DROITE):
            x = round(robot_x, 2)
            y = round(robot_y - distance, 2)
        elif(direction == Direction.BAS):
            x = round(robot_x - distance, 2)
            y = round(robot_y, 2)
        elif(direction == Direction.GAUCHE):
            x = round(robot_x, 2)
            y = round(robot_y + distance, 2)
        else:
            if (DEBUG):
                print("DIRECTION NON GÉRÉE: " + str(direction))
            exit()
        if DEBUG:
            print('Obstacle: ' + str(x) + ', ' + str(y))
        coords += str(x) + ',' + str(y) + "\n"
    else:
        if detecteUnObstacle:
            # Ici, on ne détecte plus un obstacle, on devrait donc pouvoir tourner
            detecteUnObstacle = False
            coords += "_\n"
            time.sleep(500/1000)
            deplacement = circonferenceRoue/2
            seDeplaceDe(deplacement)
            tourne("droite")

#-------------------------------------------
#               Programme
#-------------------------------------------

# Instanciation des variables utilisées
diametreRoue = 5.6 #cm
circonferenceRoue = diametreRoue * math.pi
direction = Direction.HAUT
coords = ""
robot_x = 0
robot_y = 0
detecteUnObstacle = False

DEBUG = False
MAX_TIME = 35

# Début du programme, bip sonore
start_time = time.time()
spkr.play_tone(400, 0.1, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
time.sleep(500 / 1000)

# Le robot fait un tour sur lui-même pour repérer les obstacles proches
# todo A DECOMMENTER
# for i in range(4):
#     tourne("droite")

running = True
while running:
    # Calcul du temps écoulé
    current_time = time.time()
    temps_ecoule = (current_time - start_time)

    if (not touch_sensor.is_pressed):
        avance()
    else:
        # Heurte un obstacle
        if (DEBUG):
            print("Vient de heurter un obstacle")
        recule()


    # todo A COMMENTER - arrête le programme après 90 secondes
    if (temps_ecoule >= MAX_TIME):
        if (DEBUG):
            print("Temps écoulé: ", str(round(temps_ecoule, 2)) + "s")
        running = False



# Fin du programme, bip sonore
tank_drive.off(brake=True)
spkr.play_tone(400, 0.1, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)

# Enregistrement des coordonnées
# print("Liste des coordonnées des obstacles:\n" + str(coords))
print(coords)
#todo: enregistrer dans un fichier .txt
# Ouvrir le fichier en mode écriture
with open('environnement.txt', 'w') as file:
    # for coord in coords:
    #     # Écrire chaque coordonnée dans le fichier
    #     file.write(str(coord[0]) + ',' + str(coord[1]) + '\n')
    # Écrit les coordonnées dans le fichier texte
    file.write(coords)
# Donc là, on devrait avoir un fichier environnement.txt, avec des lignes type: "37.15, -204,17"

