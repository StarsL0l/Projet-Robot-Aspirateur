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

def draw_replay_button():
    font = pygame.font.SysFont(None, taille_police)
    replay_rect = pygame.Rect(WINDOW_WIDTH // 2 - blockSize_x - marge_x, WINDOW_HEIGHT - blockSize_y - marge_y, 2*blockSize_x, blockSize_y)
    pygame.draw.rect(SCREEN, WHITE, replay_rect)
    text = font.render("Rejouer", True, GREEN)
    text_rect = text.get_rect(center=(replay_rect.centerx, replay_rect.centery))
    SCREEN.blit(text, text_rect)
    return replay_rect

# Variable globale pour l'état de la texture
global_texture_enabled = texture

def run(return_to_menu, display_simulation=True):
    global global_compteur
    global global_texture_enabled
    
    while True:  # Boucle principale pour permettre de rejouer
        global_compteur = 0  # Réinitialisation du compteur global

        # Initialisation de la grille
        grid = [[Poussière for _ in range(BLOCKS_Y)] for _ in range(BLOCKS_X)]
        initialize_grid(grid, BLOCKS_X, BLOCKS_Y)
        
        # Placement du robot
        robot_x, robot_y = rd.randint(1, BLOCKS_X - 2), rd.randint(1, BLOCKS_Y - 2)
        while grid[robot_x][robot_y] != Poussière:
            robot_x, robot_y = rd.randint(1, BLOCKS_X - 2), rd.randint(1, BLOCKS_Y - 2)
        orientation = 0
        texture_enabled = global_texture_enabled
        
        cleaning_finished = False
        compteur = 0  # Compteur pour les étapes
        MAX_ITERATIONS = 30000  # Limite de sécurité
        
        while not cleaning_finished and compteur < MAX_ITERATIONS:
            if display_simulation:
                # Si l'affichage est activé, dessiner les éléments visuels
                SCREEN.fill((150, 150, 150))
                draw_grid(grid, BLOCKS_X, BLOCKS_Y, texture_enabled)
                move_robot(grid, robot_x, robot_y, orientation, texture_enabled)
                return_button = draw_return_button()
                texture_button = draw_texture_button(texture_enabled)
            
            # Gestion des événements, même si l'affichage est désactivé
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return compteur
                if event.type == pygame.MOUSEBUTTONDOWN and display_simulation:
                    if return_button.collidepoint(event.pos):
                        return_to_menu()
                        return compteur
                    elif texture_button.collidepoint(event.pos):
                        texture_enabled = not texture_enabled

            # Incrémenter le compteur
            compteur += 1
            
            # Nettoyer la case actuelle
            if grid[robot_x][robot_y] == Poussière:
                grid[robot_x][robot_y] = Nettoyé
            
            # Choix aléatoire d'une direction : 0=haut, 1=droite, 2=bas, 3=gauche
            direction = rd.randint(0, 3)
            
            # Initialisation du déplacement
            dx, dy = 0, 0
            
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
            
            new_x, new_y = robot_x + dx, robot_y + dy
            
            # Vérification des limites ET des obstacles
            if (1 <= new_x < BLOCKS_X - 1 and 
                1 <= new_y < BLOCKS_Y - 1 and 
                grid[new_x][new_y] != Obstacle and
                grid[new_x][new_y] != Mur):
                robot_x, robot_y = new_x, new_y
                    
            # Vérifier si toutes les cases accessibles sont nettoyées
            cleaning_finished = all(cell != Poussière for row in grid for cell in row if cell != Mur and cell != Obstacle)

            if display_simulation:
                pygame.display.update()
            pygame.time.delay(delay if display_simulation else 0)  # Retard uniquement si l'affichage est activé

        global_compteur = compteur

        # Afficher une dernière fois pour montrer la dernière case nettoyée
        if display_simulation:
            SCREEN.fill((150, 150, 150))
            draw_grid(grid, BLOCKS_X, BLOCKS_Y, texture_enabled)
            move_robot(grid, robot_x, robot_y, orientation, texture_enabled)
            return_button = draw_return_button()
            texture_button = draw_texture_button(texture_enabled)
            pygame.display.update()
            pygame.time.delay(delay)  # Ajouter un petit délai pour voir la dernière case nettoyée

            font = pygame.font.SysFont(None, 50)
            text = font.render(f"{'Nettoyage terminé' if cleaning_finished else 'Limite atteinte'} ! {compteur} étapes", True, (241, 148, 138))
            text_rect = text.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2))
            rect = pygame.Rect(text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20)
            pygame.draw.rect(SCREEN, (30, 132, 73), rect)
            SCREEN.blit(text, text_rect)
            
            replay_button = draw_replay_button()
            
            pygame.display.update()
            
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return compteur
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if return_button.collidepoint(event.pos):
                            return_to_menu()
                            return compteur
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
        
        if not display_simulation:
            return compteur  # Retourne le nombre d'étapes si l'affichage est désactivé

    # Cette ligne ne devrait jamais être atteinte, mais on la laisse par sécurité
    return compteur
