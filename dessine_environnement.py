# Imports des librairies utilisées
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Hide the hello message from pygame
import pygame
import sys

#-----------------------------------------------------------------------------------------------------------------------------------------------
# Définition des constantes
SIZE = 800 # 800cm donc 8 mètres
CENTER = SIZE/2
MAX_COORDS = CENTER - 10

# VARIABLES GLOBALES
# Couleurs des lignes dessinées
color_red = (192,0,0)
color_yellow = (192,192,0)
color = color_yellow

#-----------------------------------------------------------------------------------------------------------------------------------------------
#               FONCTIONS & CLASSES
#-----------------------------------------------------------------------------------------------------------------------------------------------
# Point: les coordonnées d'un point d'un obstacle repéré par le robot
class Point:
    def __init__(self, x, y, continueLigne=True, color=(192,0,0)):
        self.x = x                          # x: position de gauche à droite (-400 -> +400)
        self.y = y                          # y: position de bas en haut     (-400 -> +400)
        self.continueLigne = continueLigne  # False si le point n'appartient pas à l'obstacle du point précédent (le programme ne dessinera alors pas de ligne entre les deux)
        self.color = color                  # La couleur du trait à dessiner

# Fonction de dessin utilisé
def draw_line(color, point1, point2):
    pygame.draw.line(window_surface, color, (point1.x, point1.y), (point2.x, point2.y), 4) # épaisseur du trait de 4 pixels

# Appelle la fonction de dessin, en plaçant les coordonnées par rapport au centre de la fenêtre (0,0)
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

# Dessine une croix en (0,0), pour repérer le point de départ du robot
def drawCrossAt0_0():
    cross_color = (255, 255, 255)  # Blanc
    cross_thickness = 1 # 1 pixel de large
    cross_length = 10   # 10 pixels de long

    pygame.draw.line(window_surface, cross_color, (CENTER - cross_length, CENTER), (CENTER + cross_length, CENTER), cross_thickness)
    pygame.draw.line(window_surface, cross_color, (CENTER, CENTER - cross_length), (CENTER, CENTER + cross_length), cross_thickness)

# Ouvre le fichier 'environnement.txt', et crée la liste des coordonnées
# S'il trouve une coordonnée (x,y), il l'ajoute
# S'il trouve '_', il fait comprendre au programme qu'il y a une coupure après les dernières coordonnées
def recupererListeCoordonnees():
    global nb_coords, continueLigne, color, color_red, color_yellow
    nb_coords = 0
    liste = []

    # Ouvre le fichier en mode lecture
    with open('environnement.txt', 'r') as file:
        for line in file:
            # Supprimer les sauts de ligne
            line = line.strip()
            if line != "":
                if line == "_":
                    continueLigne = False
                    if color == color_red:
                        color = color_yellow
                    else:
                        color = color_red
                    # print("On arrête la ligne après le point " + str(nb_coords))
                else:
                    x, y = line.split(',') # Récupération des coordonnées d'un obstacle
                    
                    # On convertit les coordonnées en entiers avant de les ajouter à la liste
                    point = Point(int(float(x)), -int(float(y)), continueLigne, color)
                    liste.append(point)
                    nb_coords += 1
    return liste


#-----------------------------------------------------------------------------------------------------------------------------------------------
#               PROGRAMME
#-----------------------------------------------------------------------------------------------------------------------------------------------
# Création de la fenêtre
pygame.init()
window_resolution=(SIZE,SIZE)
window_surface=pygame.display.set_mode(window_resolution)
# icone = pygame.image.load('crayon.ico')
# pygame.display.set_icon(icone)
pygame.display.set_caption('Croquis de l\'environnement')

# Instanciation des variables utilisées
running = True
# Configuration de l'intervalle de temps (1 ms)
intervalle = 1  # en millisecondes

# Création d'un événement personnalisé pour définir un intervalle de dessin
MON_EVENEMENT = pygame.USEREVENT + 1
pygame.time.set_timer(MON_EVENEMENT, intervalle)

# Compteur pour suivre le temps écoulé
temps_ecoule = 0
i = 0
dernieresCoordonnees = None
continueLigne = True
# Récupère les coordonnées à dessiner
listeCoordonnees = recupererListeCoordonnees()

# Durée totale d'exécution
duree_totale = intervalle * nb_coords  # en millisecondes

drawCrossAt0_0() # On dessine la croix en (0,0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == MON_EVENEMENT and temps_ecoule < duree_totale:
            coordonnees = listeCoordonnees[i]
            if (dernieresCoordonnees != None): # pour éviter le problème avec la première paire de coordonnées
                draw_line_from_center(coordonnees.color, dernieresCoordonnees, coordonnees)
            dernieresCoordonnees = coordonnees
            i += 1
            temps_ecoule += intervalle
            pygame.display.flip()

# Nettoyage et fermeture de Pygame
pygame.quit()
