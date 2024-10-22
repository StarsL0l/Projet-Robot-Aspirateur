import pygame
import random as rd
from grid import initialize_grid, draw_grid
from robot import move_robot
from config import *


# Variable globale pour l'état de la texture
global_texture_enabled = texture

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

def draw_replay_button():
    font = pygame.font.SysFont(None, taille_police)
    replay_rect = pygame.Rect(WINDOW_WIDTH // 2 - blockSize_x - marge_x, WINDOW_HEIGHT - blockSize_y - marge_y, 2*blockSize_x, blockSize_y)
    pygame.draw.rect(SCREEN, WHITE, replay_rect)
    text = font.render("Rejouer", True, GREEN)
    text_rect = text.get_rect(center=(replay_rect.centerx, replay_rect.centery))
    SCREEN.blit(text, text_rect)
    return replay_rect

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


def move(stack, grid, robot_x, robot_y, orientation):
    # Nettoyer la case actuelle
    if grid[robot_x][robot_y] == Poussière:
        grid[robot_x][robot_y] = Sol

    # Vérifier s'il reste des cases à nettoyer
    if any(Poussière in row for row in grid):
        # Déplacer le robot
        new_x, new_y, new_orientation = getNextPosition(robot_x, robot_y, orientation, grid)

        if (new_x, new_y) == (robot_x, robot_y):  # Impasse détectée
            if stack:  # Retour en arrière si nécessaire
                robot_x, robot_y, orientation = stack.pop()
                orientation = inverse_orientation(orientation)  # Inverser l'orientation
        else:
            # Sauvegarder la position et l'orientation actuelles
            orientation = new_orientation
            if not stack or (robot_x, robot_y) not in [(pos[0], pos[1]) for pos in stack]:
                stack.append((robot_x, robot_y, orientation))
            robot_x, robot_y = new_x, new_y

    return stack, grid, robot_x, robot_y, orientation

def run(return_to_menu):
    global global_texture_enabled
    
    while True:  # Boucle principale pour permettre de rejouer
        # Initialisation de la grille
        grid = [[Poussière for _ in range(BLOCKS_Y)] for _ in range(BLOCKS_X)]
        initialize_grid(grid, BLOCKS_X, BLOCKS_Y)
        
        # Placement du robot
        robot_x, robot_y = rd.randint(1, BLOCKS_X - 2), rd.randint(1, BLOCKS_Y - 2)
        while grid[robot_x][robot_y] != Poussière:
            robot_x, robot_y = rd.randint(1, BLOCKS_X - 2), rd.randint(1, BLOCKS_Y - 2)

        orientation = 0  # Orientation initiale du robot
        stack = [(robot_x, robot_y, orientation)]  # Pile avec les positions et orientations
        texture_enabled = global_texture_enabled
        compteur = 0  # Compteur pour les étapes

        cleaning_finished = False
        # Boucle de simulation
        while not cleaning_finished:
            SCREEN.fill((150, 150, 150))  # Couleur de fond
            draw_grid(grid, BLOCKS_X, BLOCKS_Y, texture_enabled)  
            move_robot(grid, robot_x, robot_y, orientation, texture_enabled)  

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
                        return
                    elif texture_button.collidepoint(event.pos):
                        texture_enabled = not texture_enabled

            compteur += 1
            # Déplacer le robot
            stack, grid, robot_x, robot_y, orientation = move(stack, grid, robot_x, robot_y, orientation)

            # Vérifier si toutes les cases accessibles sont nettoyées
            cleaning_finished = all(cell != Poussière for row in grid for cell in row if cell != Mur and cell != Obstacle)

            pygame.display.update()
            pygame.time.delay(delay)

        # Afficher une dernière fois pour montrer la dernière case nettoyée
        SCREEN.fill((150, 150, 150))
        draw_grid(grid, BLOCKS_X, BLOCKS_Y, texture_enabled)
        move_robot(grid, robot_x, robot_y, orientation, texture_enabled)
        return_button = draw_return_button()
        texture_button = draw_texture_button(texture_enabled)
        pygame.display.update()
        pygame.time.delay(delay)  # Ajouter un petit délai pour voir la dernière case nettoyée

        # Affichage du message de fin
        font = pygame.font.SysFont(None, 50)
        text = font.render(f"Nettoyage terminé ! Cela a pris {compteur} étapes", True, (241, 148, 138))
        text_rect = text.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2))
        rect = pygame.Rect(text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20)
        pygame.draw.rect(SCREEN, (30, 132, 73), rect)
        SCREEN.blit(text, text_rect)

        replay_button = draw_replay_button()

        pygame.display.update()

        # Attendre le clic sur Rejouer ou Retour
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if return_button.collidepoint(event.pos):
                        return_to_menu()
                        return
                    elif replay_button.collidepoint(event.pos):
                        global_texture_enabled = texture_enabled  # Sauvegarder l'état de la texture
                        waiting = False  # Sortir de la boucle d'attente pour rejouer
                    elif texture_button.collidepoint(event.pos):
                        texture_enabled = not texture_enabled
                        global_texture_enabled = texture_enabled  # Mettre à jour la variable globale
                        SCREEN.fill((150, 150, 150))
                        draw_grid(grid, BLOCKS_X, BLOCKS_Y, texture_enabled)
                        move_robot(grid, robot_x, robot_y, orientation, texture_enabled)
                        return_button = draw_return_button()
                        texture_button = draw_texture_button(texture_enabled)
                        replay_button = draw_replay_button()
                        SCREEN.blit(text, text_rect)
                        pygame.display.update()

            pygame.time.delay(100)  # Petit délai pour ne pas surcharger le processeur
