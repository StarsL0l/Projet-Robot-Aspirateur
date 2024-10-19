import random as rd
import pygame
from config import Poussière,Nettoyé, Mur, Obstacle, BLACK, GRAY, WHITE, SCREEN, blockSize_x, blockSize_y, x, y

def initialize_grid(grid, BLOCKS_X, BLOCKS_Y):
    # Initialiser la grille avec des murs et des obstacles
    for i in range(BLOCKS_X):
        grid[i][0] = grid[i][-1] = Mur
    for j in range(BLOCKS_Y):
        grid[0][j] = grid[-1][j] = Mur

    num_obstacles = rd.randint(10, 15)
    for _ in range(num_obstacles):
        while True:
            x_alea = rd.randint(1, BLOCKS_X - 2)
            y_alea = rd.randint(1, BLOCKS_Y - 2)
            if grid[x_alea][y_alea] == Poussière:
                grid[x_alea][y_alea] = Obstacle
                break

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
