import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Hide the hello message from pygame
import pygame
import sys

import random

# Fonctions et classes
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def draw_line(color, point1, point2):
    print("Drawing line from (" + str(point1.x) + ", " + str(point1.y) + ") to (" + str(point2.x) + ", " + str(point2.y) + ")")
    pygame.draw.line(window_surface, color, (point1.x, point1.y), (point2.x, point2.y))
    return

def draw_line_from_center(color, point1, point2):
   draw_line(color, Point( round(point1.x+CENTER,2) , round(point1.y+CENTER,2) ), Point( round(point2.x+CENTER,2) , round(point2.y+CENTER,2) ))


# Fonction pour générer des coordonnées aléatoires
def generer_prochaines_coordonnees(i, dernieresCoordonnees = None):
    if dernieresCoordonnees is None:
        x = 0
        y = 0
    else:
        if i % 2 == 0:
            x = round(random.uniform(-MAX_COORDS, MAX_COORDS), 2)
            y = round(random.uniform(-MAX_COORDS, MAX_COORDS), 2)
        else:
            x = round(random.uniform(-MAX_COORDS, MAX_COORDS), 2)
            y = dernieresCoordonnees.y 
    return Point(x, y)


# Définition des constantes
SIZE = 800
CENTER = SIZE/2
MAX_COORDS = CENTER - 10

# Création de la fenêtre
pygame.init()
window_resolution=(SIZE,SIZE)
window_surface=pygame.display.set_mode(window_resolution)
pygame.display.set_caption('Drawing walls')


# Getting une liste de points
NB_COORDS = 14
# liste_de_coordonnees = generer_liste_points(NB_COORDS)


# Configuration de l'intervalle de temps (500 ms)
intervalle = 350  # en millisecondes

# Durée totale d'exécution (10 secondes)
duree_totale = intervalle * NB_COORDS  # en millisecondes

# Création d'un événement personnalisé pour appeler la fonction
MON_EVENEMENT = pygame.USEREVENT + 1
pygame.time.set_timer(MON_EVENEMENT, intervalle)

# Compteur pour suivre le temps écoulé
temps_ecoule = 0
i = 0
dernieresCoordonnees = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == MON_EVENEMENT and temps_ecoule < duree_totale:
            # Appel de votre fonction
            # coordonnees = liste_de_coordonnees[i]
            coordonnees = generer_prochaines_coordonnees(i, dernieresCoordonnees)
            if (dernieresCoordonnees != None):
                color = random.choices(range(256), k=3)
                draw_line_from_center(color, dernieresCoordonnees, coordonnees)
            dernieresCoordonnees = coordonnees
            i += 1
            temps_ecoule += intervalle
            pygame.display.flip()

# Nettoyage et fermeture de Pygame
pygame.quit()
