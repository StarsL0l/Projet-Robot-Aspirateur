import pygame
import random as rd
from grid import initialize_grid, draw_grid
from robot import move_robot
from config import (BLOCKS_X, BLOCKS_Y, SCREEN, CLOCK, Poussière, texture, 
                   WHITE, RED, GREEN, GRAY, WINDOW_WIDTH, WINDOW_HEIGHT)

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

def inverse_orientation(orientation):
    return (orientation + 180) % 360

def getNextPosition(i, j, orientation, grid):
    # Essayer d'aller à gauche
    if grid[i - 1][j] == Poussière: 
        return i - 1, j, 90
    
    # Essayer d'aller en bas
    if grid[i][j + 1] == Poussière: 
        return i, j + 1, 180
    
    # Essayer d'aller en haut
    if grid[i][j - 1] == Poussière: 
        return i, j - 1, 0

    # Essayer d'aller à droite
    if grid[i + 1][j] == Poussière: 
        return i + 1, j, 270

    # Si aucune direction n'est possible, rester sur place
    return i, j, orientation


def run(return_to_menu):
    # Initialisation de la grille
    grid = [[Poussière for _ in range(BLOCKS_Y)] for _ in range(BLOCKS_X)]
    initialize_grid(grid, BLOCKS_X, BLOCKS_Y)
    
    # Placement du robot
    robot_x, robot_y = rd.randint(1, BLOCKS_X - 2), rd.randint(1, BLOCKS_Y - 2)
    while grid[robot_x][robot_y] != Poussière:
        robot_x, robot_y = rd.randint(1, BLOCKS_X - 2), rd.randint(1, BLOCKS_Y - 2)

    orientation = 0  # Orientation initiale du robot
    stack = [(robot_x, robot_y, orientation)]  # Pile avec les positions et orientations
    cleaning_finished = False

    texture_enabled = texture
    compteur = 0  # Compteur pour les étapes

    # Boucle principale
    while True:
        SCREEN.fill((150, 150, 150))  # Couleur de fond
        draw_grid(grid, BLOCKS_X, BLOCKS_Y, texture_enabled)  # Utiliser texture_enabled au lieu de texture
        move_robot(grid, robot_x, robot_y, orientation, texture_enabled)  # Même chose ici

        # Afficher les deux boutons
        return_button = draw_return_button()
        texture_button = draw_texture_button(texture_enabled)

        # Gestion des événements modifiée pour inclure le bouton texture
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
            # Déplacer le robot
            compteur += 1 
            new_x, new_y, new_orientation = getNextPosition(robot_x, robot_y, orientation, grid)

            if (new_x, new_y) == (robot_x, robot_y):  # Impasse détectée
                if stack:  # Retour en arrière si nécessaire
                    robot_x, robot_y, orientation = stack.pop()
                    orientation = inverse_orientation(orientation)  # Inverser l'orientation
                else:
                    cleaning_finished = True  # Aucune autre position à explorer
            else:
                robot_x, robot_y = new_x, new_y
                orientation = new_orientation
                stack.append((robot_x, robot_y, orientation))  # Sauvegarder la position et l'orientation actuelles

        # Affichage du message de fin si nettoyage terminé
        if cleaning_finished:
            font = pygame.font.SysFont(None, 50)
            text = font.render(f"Nettoyage terminé ! Cela a pris {compteur} étapes", True, (241, 148, 138))
            text_rect = text.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2))
            rect = pygame.Rect(text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20)
            pygame.draw.rect(SCREEN, (30, 132, 73), rect)
            SCREEN.blit(text, text_rect)

        pygame.display.update()

        # Attendre un peu pour ralentir l'animation
        time.sleep(0)

