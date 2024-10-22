import pygame
import random as rd
from algorithms import random_algo
from config import *

# Variable globale pour le compteur
global_compteur = 0



def draw_return_button():
    """
    Fonction pour dessiner le bouton "Retour".
    """
    font = pygame.font.SysFont(None, taille_police)
    return_rect = pygame.Rect(10, 10, 2 * blockSize_x - 20, blockSize_y - 20)
    pygame.draw.rect(SCREEN, WHITE, return_rect)
    text = font.render("Retour", True, RED)
    text_rect = text.get_rect(center=(return_rect.centerx, return_rect.centery))
    SCREEN.blit(text, text_rect)
    return return_rect


def draw_replay_button():
    font = pygame.font.SysFont(None, taille_police)
    replay_rect = pygame.Rect(WINDOW_WIDTH // 2 - blockSize_x - marge_x, 2*WINDOW_HEIGHT//3 - marge_y, 2*blockSize_x, blockSize_y)
    pygame.draw.rect(SCREEN, RED, replay_rect)
    text = font.render("Rejouer", True, GREEN)
    text_rect = text.get_rect(center=(replay_rect.centerx, replay_rect.centery))
    SCREEN.blit(text, text_rect)
    return replay_rect


def run(return_to_menu):
    global global_compteur
    global SCREEN  # Utiliser la fenêtre existante

    while True:  # Boucle principale pour permettre de relancer
        font = pygame.font.SysFont(None, 50)

        # Variables pour gérer l'entrée utilisateur
        input_box = pygame.Rect(SCREEN.get_width() // 2 - 100, SCREEN.get_height() // 2 - 50, 200, 50)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        user_text = ''
        done = False
        simulation_count = 0

        # Bouton pour lancer la simulation
        button_rect = pygame.Rect(SCREEN.get_width() // 2 - 100, SCREEN.get_height() // 2 + 20, 200, 50)
        button_color = (0, 255, 0)

        clock = pygame.time.Clock()

        # Boucle initiale pour entrer le nombre de simulations
        while not done:
            SCREEN.fill((150, 150, 150))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    return_button = draw_return_button()
                    if return_button.collidepoint(event.pos):
                        return_to_menu()
                        return

                    if input_box.collidepoint(event.pos):
                        active = not active
                    elif button_rect.collidepoint(event.pos) and user_text:
                        try:
                            simulation_count = int(user_text)
                            if simulation_count > 0:
                                done = True
                        except ValueError:
                            user_text = ''
                    else:
                        active = False
                    color = color_active if active else color_inactive

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if active and user_text:
                            try:
                                simulation_count = int(user_text)
                                if simulation_count > 0:
                                    done = True
                            except ValueError:
                                user_text = ''
                    elif event.key == pygame.K_BACKSPACE and active:
                        user_text = user_text[:-1]
                    elif active and event.unicode.isdigit():
                        user_text += event.unicode

            pygame.draw.rect(SCREEN, color, input_box, 2)
            text_surface = font.render(user_text, True, WHITE)
            SCREEN.blit(text_surface, (input_box.x + 5, input_box.y + 5))

            pygame.draw.rect(SCREEN, button_color, button_rect)
            button_text = font.render("Démarrer", True, BLACK)
            button_text_rect = button_text.get_rect(center=button_rect.center)
            SCREEN.blit(button_text, button_text_rect)

            draw_return_button()

            pygame.display.flip()
            clock.tick(30)

        # Exécution des simulations
        total_iterations = 0
        global_compteur_list = []

        for i in range(simulation_count):
            
            # Gérer les événements avant chaque simulation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return_to_menu()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return_button = draw_return_button()
                    if return_button.collidepoint(event.pos):
                        return_to_menu()
                        return

            try:
                steps = random_algo.run(return_to_menu, display_simulation=False)
                global_compteur_list.append(steps)
                total_iterations += steps
            except Exception as e:
                print(f"Erreur lors de l'exécution de random_algo.run: {e}")
                return_to_menu()
                return


            # Mettre à jour la barre de progression
            SCREEN.fill((150, 150, 150))
            progress_text = font.render(f"Simulation {i + 1}/{simulation_count}", True, WHITE)
            progress_rect = progress_text.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2 - 50))
            SCREEN.blit(progress_text, progress_rect)

            progress_width = 400
            progress_height = 30
            progress_x = (SCREEN.get_width() - progress_width) // 2
            progress_y = SCREEN.get_height() // 2

            pygame.draw.rect(SCREEN, WHITE, (progress_x, progress_y, progress_width, progress_height), 2)
            progress = (i + 1) / simulation_count
            pygame.draw.rect(SCREEN, GREEN, (progress_x, progress_y, int(progress_width * progress), progress_height))

            draw_return_button()

            pygame.display.flip()
            pygame.time.delay(10)  # Réduit le délai pour une mise à jour plus fréquente

        # Affichage des résultats
        if simulation_count > 0:
            moyenne_iterations = total_iterations / simulation_count
            SCREEN.fill((150, 150, 150))

            result_text = font.render(f"Moyenne d'étapes: {moyenne_iterations:.2f}", True, GREEN)
            result_rect = result_text.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2))
            SCREEN.blit(result_text, result_rect)

            return_button = draw_return_button()
            replay_button = draw_replay_button()

            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return_to_menu()
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if return_button.collidepoint(event.pos):
                            return_to_menu()
                            return
                        elif replay_button.collidepoint(event.pos):
                            waiting = False  # Sortir de la boucle d'attente pour relancer
                            break  # Sortir de la boucle for

                pygame.time.delay(100)  # Petit délai pour ne pas surcharger le processeur

        else:
            return_to_menu()
            return

    # Cette ligne ne devrait jamais être atteinte, mais on la laisse par sécurité
    return_to_menu()
