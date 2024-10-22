import pygame

# Taille des blocs et de la fenêtre
WINDOW_HEIGHT = WINDOW_WIDTH = 1000
BLOCKS_X = BLOCKS_Y = 18  # Nombre de blocs 

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
delay = 100 # en ms

# Taille des blocs
blockSize_x = WINDOW_WIDTH // BLOCKS_X
blockSize_y = WINDOW_HEIGHT // BLOCKS_Y
marge_x = WINDOW_WIDTH % BLOCKS_X
marge_y = WINDOW_HEIGHT % BLOCKS_Y

# Taille de la police
taille_police = blockSize_x//2

# Nombres d'obstacles
obstacle_min = 5
obstacle_max = 10

# Coordonnées de la grille
x = [k for k in range(0, WINDOW_WIDTH, blockSize_x)]
y = [k for k in range(0, WINDOW_HEIGHT, blockSize_y)]

# Texture activée ou non
texture = True
