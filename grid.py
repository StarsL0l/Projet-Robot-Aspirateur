import random as rd
import pygame
from config import *

def initialize_grid(grid, BLOCKS_X, BLOCKS_Y):
    # Initialiser la grille avec des murs et des obstacles
    for i in range(BLOCKS_X):
        grid[i][0] = grid[i][-1] = Mur
    for j in range(BLOCKS_Y):
        grid[0][j] = grid[-1][j] = Mur

    # Création d'obstacles aléatoire 
    num_obstacles = rd.randint(obstacle_min, obstacle_max)
    for _ in range(num_obstacles):
        while True:
            x_alea = rd.randint(1, BLOCKS_X - 2)
            y_alea = rd.randint(1, BLOCKS_Y - 2)
            if grid[x_alea][y_alea] == Poussière:
                grid[x_alea][y_alea] = Obstacle
                break
    
    # Mise en place des pièces
    piece(grid)

    # Remplissage des poussières enfermé
    encercle(grid)

def draw_grid(grid, BLOCKS_X, BLOCKS_Y, texture):
    # Dessiner la grille avec les textures
    for i in range(BLOCKS_X):
        for j in range(BLOCKS_Y):
            rect = pygame.Rect(x[i], y[j], blockSize_x, blockSize_y)
            if grid[i][j] == Poussière:
                pygame.draw.rect(SCREEN, GRAY, rect, 0)
            elif grid[i][j] == Nettoyé:
                pygame.draw.rect(SCREEN, WHITE, rect, 0)
            elif grid[i][j] == Mur:
                if texture:
                    image = pygame.image.load("data/wall_icon.jpg")
                    image = pygame.transform.scale(image, (blockSize_x, blockSize_y))
                    SCREEN.blit(image, (x[i], y[j]))
                else:
                    pygame.draw.rect(SCREEN, BLACK, rect, 0)
            elif grid[i][j] == Obstacle:
                if texture:
                    image = pygame.image.load("data/wood.jpeg")
                    image = pygame.transform.scale(image, (blockSize_x, blockSize_y))
                    SCREEN.blit(image, (x[i], y[j]))
                else:
                    pygame.draw.rect(SCREEN, BLACK, rect, 0)

            pygame.draw.rect(SCREEN, BLACK, rect, 1)

def piece(grid):
    # Création des cloisons
    # Cloison centrale
    for i in range(BLOCKS_Y):
        grid[BLOCKS_X // 2][i] = Mur
    for i in range(3):
        grid[(BLOCKS_X // 2 - 1) + i][BLOCKS_Y // 4] = Poussière
        grid[(BLOCKS_X // 2 - 1) + i][3*BLOCKS_Y // 4] = Poussière
    
    # Colison des deux pièces de gauche
    for i in range(BLOCKS_X//2):
        grid[i][BLOCKS_Y // 2] = Mur
    # Création d'une porte de manière aléatoire
    # Création de la porte une fois sur deux
    if rd.choice([True, False]):
        porte_alea = rd.randint(1, (BLOCKS_Y // 2) - 1)
        for i in range(3):
            grid[porte_alea][(BLOCKS_Y // 2 - 1) + i] = Poussière

def encercle(grid):
    for i in range(BLOCKS_X):
                for j in range(BLOCKS_Y):
                    if grid[i][j] == Poussière:
                        if grid[i+1][j] and grid[i-1][j] and grid[i][j+1] and grid[i][j-1] == (Obstacle or Mur):
                            grid[i][j] = Obstacle