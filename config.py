import pygame

# Taille des blocs et de la fenêtre
SIZE = 50
BLOCKS_X = 15  # Nombre de blocs en largeur
BLOCKS_Y = 15  # Nombre de blocs en hauteur

WINDOW_HEIGHT = BLOCKS_X * SIZE
WINDOW_WIDTH = BLOCKS_Y * SIZE

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Objets
Poussière = 0
Nettoyé = 1
Mur = 2
Obstacle = 3

# Initialisation Pygame et fenêtre
pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()

# Taille des blocs
blockSize_x = WINDOW_WIDTH // BLOCKS_X
blockSize_y = WINDOW_HEIGHT // BLOCKS_Y

# Coordonnées de la grille
x = [k for k in range(0, WINDOW_WIDTH, blockSize_x)]
y = [k for k in range(0, WINDOW_HEIGHT, blockSize_y)]

# Texture activée ou non
texture = True
