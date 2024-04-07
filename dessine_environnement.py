import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Hide the hello message from pygame
import pygame
import sys

import random

# Fonctions et classes
class Point:
    def __init__(self, x, y, continueLigne=True):
        self.x = x
        self.y = y
        self.continueLigne = continueLigne

def draw_line(color, point1, point2):
    pygame.draw.line(window_surface, color, (point1.x, point1.y), (point2.x, point2.y), 4) # épaisseur du trait de 3 pixels

def draw_line_from_center(color, point1, point2):
   global continueLigne

   if not point2.continueLigne:
       point1 = point2
       continueLigne = True

   draw_line(
       color,
       Point(round(point1.x+CENTER,2), round(point1.y+CENTER,2), point1.continueLigne),
       Point(round(point2.x+CENTER,2), round(point2.y+CENTER,2), point2.continueLigne)
    )

def drawCrossAt0_0():
    # Define the cross
    cross_color = (255, 255, 255)  # White color
    cross_thickness = 1
    cross_length = 10  # Length of the cross lines

    # Draw the cross
    pygame.draw.line(window_surface, cross_color, (CENTER - cross_length, CENTER), (CENTER + cross_length, CENTER), cross_thickness)
    pygame.draw.line(window_surface, cross_color, (CENTER, CENTER - cross_length), (CENTER, CENTER + cross_length), cross_thickness)

def recupererListeCoordonnees():
    global nb_coords, continueLigne
    nb_coords = 0
    liste = []

    # Ouvrir le fichier en mode lecture
    with open('environnement.txt', 'r') as file:
        for line in file:
            # Supprimer les sauts de ligne
            line = line.strip()
            if line != "":
                if line == "_":
                    continueLigne = False
                    # print("On arrête la ligne après le point " + str(nb_coords))
                else:
                    # La ligne représente les coordonnées d'un obstacle
                    # Séparer les coordonnées
                    x, y = line.split(',')
                    
                    # Convertir les coordonnées en entiers et les ajouter à la liste
                    point = Point(int(float(x)), -int(float(y)), continueLigne)
                    liste.append(point)
                    nb_coords += 1
    return liste

# Définition des constantes
SIZE = 800 # 800cm donc 8 mètres
CENTER = SIZE/2
MAX_COORDS = CENTER - 10

# Création de la fenêtre
pygame.init()
window_resolution=(SIZE,SIZE)
window_surface=pygame.display.set_mode(window_resolution)
pygame.display.set_caption('Dessin de l\'environnement')

# Configuration de l'intervalle de temps (2 ms)
intervalle = 2  # en millisecondes

# Création d'un événement personnalisé pour appeler la fonction
MON_EVENEMENT = pygame.USEREVENT + 1
pygame.time.set_timer(MON_EVENEMENT, intervalle)

# Compteur pour suivre le temps écoulé
temps_ecoule = 0
i = 0
dernieresCoordonnees = None
continueLigne = True
listeCoordonnees = recupererListeCoordonnees()

# Durée totale d'exécution
duree_totale = intervalle * nb_coords  # en millisecondes

drawCrossAt0_0()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == MON_EVENEMENT and temps_ecoule < duree_totale:
            coordonnees = listeCoordonnees[i]
            if (dernieresCoordonnees != None):
                if i%2==0:
                    color = (192,0,0) # rouge
                else:
                    color = (192,192,0) # yellow
                # color = random.choices(range(256), k=3)
                draw_line_from_center(color, dernieresCoordonnees, coordonnees)
            dernieresCoordonnees = coordonnees
            i += 1
            temps_ecoule += intervalle
            pygame.display.flip()

# Nettoyage et fermeture de Pygame
pygame.quit()
