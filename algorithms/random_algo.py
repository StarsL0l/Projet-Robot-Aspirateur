import pygame
import random as rd
from grid import initialize_grid, draw_grid
from robot import move_robot
from config import (BLOCKS_X, BLOCKS_Y, SCREEN, CLOCK, Poussière, Obstacle, texture, 
                   WHITE, RED, GREEN, WINDOW_WIDTH, WINDOW_HEIGHT)

def draw_return_button():
    font = pygame.font.SysFont(None, 30)
    return_rect = pygame.Rect(10, 10, 130, 30)
    pygame.draw.rect(SCREEN, WHITE, return_rect)
    text = font.render("Retour", True, RED)
    text_rect = text.get_rect(center=(return_rect.centerx, return_rect.centery))
    SCREEN.blit(text, text_rect)
    return return_rect

def draw_texture_button(texture_enabled):
    font = pygame.font.SysFont(None, 30) 
    texture_rect = pygame.Rect(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 40, 140, 35)
    pygame.draw.rect(SCREEN, WHITE, texture_rect)
    text = font.render("Texture: ON" if texture_enabled else "Texture: OFF", True, GREEN if texture_enabled else RED)
    text_rect = text.get_rect(center=(texture_rect.centerx, texture_rect.centery))
    SCREEN.blit(text, text_rect)
    return texture_rect

def run(return_to_menu):
    # Initialisation de la grille
    grid = [[Poussière for _ in range(BLOCKS_Y)] for _ in range(BLOCKS_X)]
    initialize_grid(grid, BLOCKS_X, BLOCKS_Y)
    
    # Position initiale du robot
    robot_x = rd.randint(1, BLOCKS_X - 2)
    robot_y = rd.randint(1, BLOCKS_Y - 2)
    orientation = 0
    texture_enabled = texture
    
    while True:
        SCREEN.fill((150, 150, 150))
        
        # Choix aléatoire d'une direction : 0=haut, 1=droite, 2=bas, 3=gauche
        direction = rd.randint(0, 3)
        
        # Initialisation du déplacement
        dx = 0
        dy = 0
        
        # Calcul du déplacement selon la direction
        if direction == 0:    # Haut
            dy = -1
            orientation = 0
        elif direction == 1:  # Droite
            dx = 1
            orientation = 270
        elif direction == 2:  # Bas
            dy = 1
            orientation = 180
        else:                 # Gauche
            dx = -1
            orientation = 90
            
        new_x = robot_x + dx
        new_y = robot_y + dy
        
        # Vérification des limites ET des obstacles
        if (1 <= new_x < BLOCKS_X - 1 and 
            1 <= new_y < BLOCKS_Y - 1 and 
            grid[new_x][new_y] != Obstacle):
            robot_x = new_x
            robot_y = new_y
        
        # Affichage
        draw_grid(grid, BLOCKS_X, BLOCKS_Y, texture_enabled)
        move_robot(grid, robot_x, robot_y, orientation, texture_enabled)
        
        # Affichage des boutons
        return_button = draw_return_button()
        texture_button = draw_texture_button(texture_enabled)
        
        pygame.display.update()
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.collidepoint(event.pos):
                    return_to_menu()
                elif texture_button.collidepoint(event.pos):
                    texture_enabled = not texture_enabled
        
        pygame.time.delay(100)
