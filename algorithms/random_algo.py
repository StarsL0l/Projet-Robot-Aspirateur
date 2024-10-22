import pygame
import random as rd
from grid import initialize_grid, draw_grid
from robot import move_robot
from config import *


def draw_return_button():
    font = pygame.font.SysFont(None, taille_police)
    return_rect = pygame.Rect(10, 10, 2*blockSize_x - 20, blockSize_y - 20)
    pygame.draw.rect(SCREEN, WHITE, return_rect)
    text = font.render("Retour", True, RED)
    text_rect = text.get_rect(center=(return_rect.centerx, return_rect.centery))
    SCREEN.blit(text, text_rect)
    return return_rect

def draw_texture_button(texture_enabled):
    font = pygame.font.SysFont(None, taille_police) 
    texture_rect = pygame.Rect((WINDOW_WIDTH - 2*blockSize_x - marge_x) - 10, WINDOW_HEIGHT - blockSize_y + 10 - marge_y, 2*blockSize_x, blockSize_y - 20)
    pygame.draw.rect(SCREEN, WHITE, texture_rect)
    text = font.render("Texture: ON" if texture_enabled else "Texture: OFF", True, GREEN if texture_enabled else RED)
    text_rect = text.get_rect(center=(texture_rect.centerx, texture_rect.centery))
    SCREEN.blit(text, text_rect)
    return texture_rect

def run(return_to_menu):
    # Initialisation de la grille
    grid = [[Poussière for _ in range(BLOCKS_Y)] for _ in range(BLOCKS_X)]
    initialize_grid(grid, BLOCKS_X, BLOCKS_Y)
    
    # Placement du robot
    robot_x, robot_y = rd.randint(1, BLOCKS_X - 2), rd.randint(1, BLOCKS_Y - 2)
    while grid[robot_x][robot_y] != Poussière:
        robot_x, robot_y = rd.randint(1, BLOCKS_X - 2), rd.randint(1, BLOCKS_Y - 2)
    orientation = 0
    texture_enabled = texture
    
    cleaning_finished = False
    compteur = 0  # Compteur pour les étapes

    while True:
        SCREEN.fill((150, 150, 150))
        # Affichage
        draw_grid(grid, BLOCKS_X, BLOCKS_Y, texture_enabled)
        move_robot(grid, robot_x, robot_y, orientation, texture_enabled)
        
        # Affichage des boutons
        return_button = draw_return_button()
        texture_button = draw_texture_button(texture_enabled)
        
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

        if not cleaning_finished:
            # Incrémenter le compteur
            compteur += 1
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
                grid[new_x][new_y] != Obstacle and
                grid[new_x][new_y] != Mur):
                robot_x = new_x
                robot_y = new_y
                        
            #Scan grid
            nb_poussiere = 0
            for i in range(BLOCKS_X):
                for j in range(BLOCKS_Y):
                    if grid[i][j] == Poussière:
                        nb_poussiere += 1
            if nb_poussiere == 0:
                cleaning_finished = True
        
        if cleaning_finished:
            font = pygame.font.SysFont(None, 50)
            text = font.render(f"Nettoyage terminé ! Cela a pris {compteur} étapes", True, (241, 148, 138))
            text_rect = text.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2))
            rect = pygame.Rect(text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20)
            pygame.draw.rect(SCREEN, (30, 132, 73), rect)
            SCREEN.blit(text, text_rect)


        pygame.display.update()
        pygame.time.delay(delay)
