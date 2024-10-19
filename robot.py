import pygame
from config import Nettoyé, BLUE, SCREEN, blockSize_x, blockSize_y, x, y

def move_robot(grid, i, j, orientation, texture):
    # Marquer la case comme nettoyée
    grid[i][j] = Nettoyé
    
    # Dessiner le robot avec sa texture et orientation
    if texture:
        image = pygame.image.load("data/robot_aspi.png")
        image = pygame.transform.scale(image, (blockSize_x, blockSize_y))
        image = pygame.transform.rotate(image, orientation)
        SCREEN.blit(image, (x[i], y[j]))
    else:
        rect = pygame.Rect(x[i], y[j], blockSize_x, blockSize_y)
        pygame.draw.rect(SCREEN, BLUE, rect, 0)
