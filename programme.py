#!/usr/bin/env python3

# Imports des librairies utilisées
import time
import math
from ev3dev2.motor import *
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor.virtual import * # utilisé par le simulateur, à commenter pour une exécution réelle

#-----------------------------------------------------------------------------------------------------------------------------------------------
# VARIABLES GLOBALES
# direction             -> la direction dans laquelle se dirige le robot (il commence par le haut)
# coords                -> la liste des coordonnées des obstacles à enregistrer
# faitLeTourDUnObstacle -> variable allant de 0 à 4, permettant au robot de se rappeler qu'il fait le tour d'un obstacle puis de continuer tout droit
# aTourne               -> permet au robot de se rappeler qu'il vient de tourner, afin de réinitialiser la dernière distance en mémoire

# CONSTANTES
VITESSE_DU_ROBOT = 1
DEBUG = True            # Pour afficher le debug
MAX_TIME = 90           # Temps maximal d'exécution du programme (en secondes)
#-----------------------------------------------------------------------------------------------------------------------------------------------

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


#-----------------------------------------------------------------------------------------------------------------------------------------------
#               FONCTIONS
#-----------------------------------------------------------------------------------------------------------------------------------------------
# Permet de changer la valeur de la variable globale "direction"
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

# Permet au robot de tourner à 90 degrés sur sa gauche ou sur sa droite 
# (sur sa droite par défaut)
def tourne(cote = "droite"):
    global direction # récupère la variable globale direction
    global lastDistance, aTourne
    lastDistance = None

    temps = 1550 / 1000

    if (DEBUG):
        print("On tourne à " + cote)

    if (cote == "gauche"):
        # On tourne à gauche
        steering_drive.on_for_seconds(-90, SpeedRPS(0.5), temps)
    else:
        # On tourne à droite
        steering_drive.on_for_seconds(90, SpeedRPS(0.5), temps)
    tank_drive.off(brake=True)
    time.sleep(150/1000)
    direction = changeDirection(cote) # change la variable "direction" après avoir tourné
    lastDistance = None
    aTourne = True


# Permet au robot de reculer pendant 1/2 seconde
# utilisée après avoir heurté un obstacle
def recule():
    global robot_x, robot_y # On récupère les coordonnées du robot du programme
    vitesse_recule = 1

    if (DEBUG):
        print("Le robot recule")

    # S'arrête
    tank_drive.off(brake=True)
    spkr.play_tone(800, 0.1, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
    time.sleep(500/1000)
    # Recule
    tank_drive.on_for_seconds(SpeedRPS(vitesse_recule) * -1, SpeedRPS(vitesse_recule) * -1, 1)
    time.sleep(500/1000)

    # Calcul les nouvelles coordonnées du robot
    deplacement = vitesse_recule*circonferenceRoue
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
    


# Modifie les coordonnées du robot
# en fonction de son déplacement
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


# Enregistre les coordonnées d'un obstacle
# en fonction des coordonnées du robot et de sa distance à l'obstacle
def enregistreUnObstacle(distance):
    global coords, direction

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
    coords += str(x) + ',' + str(y) + "\n"


# Détermine si le robot vient de capter un nouvel obstacle
#   Pour cela, on récupère la distance envoyée par le capteur US
#   Si elle est trop différente de la dernière perçue, alors c'est un nouvel obstacle
def grandEcartDistance(distance):
    global lastDistance
    return abs(distance - lastDistance) > 5


# Appelé quand le robot a dépassé un obstacle, et qu'il a la place de tourner
def neDetectePlusObstacle():
    # Ici, on ne détecte plus un obstacle, on devrait donc pouvoir tourner
    global coords, faitLeTourDUnObstacle, lastDistance, lastTimeTour
    lastDistance = None

    if (DEBUG):
        print("On est arrivé au bout d'un obstacle (" + str(faitLeTourDUnObstacle) + ")")
    # coords += "_\n"
    distance = ultrasonic_sensor.distance_centimeters
    
    faitLeTourDUnObstacle += 1
    time.sleep(500/1000)
    deplacement = VITESSE_DU_ROBOT*circonferenceRoue/2
    seDeplaceDe(deplacement)
    lastDistance = distance
    
    if faitLeTourDUnObstacle > 0 and faitLeTourDUnObstacle <= 4 and distance >= 20:
        # Si le robot est en train de faire le tour d'un obstacle, et qu'il a la place de tourner
        tourne("droite")
    else:
        # Le robot a fini de tourner autour d'un obstacle
        faitLeTourDUnObstacle = 0
        lastTimeTour = time.time()


# Fonction principale, permet au robot d'avancer
def avance():
    global robot_x, robot_y # On récupère les coordonnées du robot du programme
    global coords # On utilise la liste en variable globale pour pouvoir l'affecter
    global faitLeTourDUnObstacle

    tank_drive.on(SpeedRPS(VITESSE_DU_ROBOT), SpeedRPS(VITESSE_DU_ROBOT))
    deplacement = VITESSE_DU_ROBOT*circonferenceRoue/30 # On part du principe que le calcul se fait 30 fois par seconde
    seDeplaceDe(deplacement)
    
    distance = ultrasonic_sensor.distance_centimeters
    grandEcart = grandEcartDistance(distance)
    if grandEcart: # On sort du champ d'un obstacle
        if DEBUG:
            print("Nouvel obstacle détecté !")
        coords += "_\n"
        if distance >= 20 and lastDistance < 100:
            if DEBUG:
                print("Cet obstacle est suffisamment loin (" + str(round(distance,2)) + " cm)")
            if time.time() - lastTimeTour > 1.5:
                neDetectePlusObstacle()



#-----------------------------------------------------------------------------------------------------------------------------------------------
#               PROGRAMME
#-----------------------------------------------------------------------------------------------------------------------------------------------
# Instanciation des variables utilisées
running = True                              # Temps que vrai, le programme tourne
diametreRoue = 5.6 #cm                      # Le diamètre des roues du robot
circonferenceRoue = diametreRoue * math.pi  # La circonférence de ces-mêmes roues, permet de calculer la distance parcourue en ligne droite
direction = Direction.HAUT                  # La direction dans laquelle les coordonnées du robot varient
coords = ""                                 # Le contenu du fichier texte à enregistrer (les coordonnées des obstacles)
robot_x = 0                                 # La position de gauche à droite du robot (par rapport à sa position de départ)
robot_y = 0                                 # La position de haut en bas du robot (par rapport à sa position de départ)
faitLeTourDUnObstacle = 0                   # Compteur du nombre de rotations autour d'un obstacle
lastDistance = None                         # Dernière distance captée par le capteur US
aTourne = False
lastTimeTour = time.time()


# Début du programme, bip sonore
start_time = time.time()
spkr.play_tone(400, 0.1, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
time.sleep(500 / 1000)

# Le robot fait un tour sur lui-même pour repérer les obstacles proches
# (On annule cette partie finalement)
# for i in range(4):
#     tourne("droite")
#     distance = ultrasonic_sensor.distance_centimeters
#     if distance < 255:
#         enregistreUnObstacle(distance)
#     lastDistance = distance


# Tant que le programme tourne
while running:
    # Calcul du temps écoulé
    temps_ecoule = (time.time() - start_time)

    distance = ultrasonic_sensor.distance_centimeters
    if distance < 255:
        enregistreUnObstacle(distance)
    if lastDistance == None:
        lastDistance = distance

    # print("Distance/last: " + str(round(distance,2)) + " / " + str(round(lastDistance,2)))

    if (not touch_sensor.is_pressed):
        avance()
    else:
        # Heurte un obstacle
        if (DEBUG):
            print("Vient de heurter un obstacle")
        recule()
        
    if not aTourne:
        lastDistance = distance

    aTourne = False

    # Arrête le programme après avoir atteind son temps d'exécution maximal, ou lorsque l'on appuie sur le bouton ENTER
    if (temps_ecoule >= MAX_TIME or btn.enter):
        if (DEBUG):
            print("Temps écoulé: ", str(round(temps_ecoule, 2)) + "s")
        running = False

#-----------------------------------------------------------------------------------------------------------------------------------------------
# Fin du programme, bip sonore
tank_drive.off(brake=True)
spkr.play_tone(400, 0.1, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)


# Enregistrement des coordonnées
print(coords) #todo - à commenter, ne sert que pour le simulateur qui n'écrit pas de fichier .txt

# Ouvrir le fichier en mode écriture
with open('environnement.txt', 'w') as file:
    # for coord in coords:
    #     # Écrire chaque coordonnée dans le fichier
    #     file.write(str(coord[0]) + ',' + str(coord[1]) + '\n')

    # Écrit les coordonnées dans le fichier texte
    file.write(coords)
