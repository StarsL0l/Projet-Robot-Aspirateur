import sys
import pygame
from algorithms import random_algo, algo_balayage  # Import des algorithmes
from config import SCREEN, WINDOW_WIDTH, WINDOW_HEIGHT, GREEN, WHITE, RED, CLOCK

# Affichage du texte dans Pygame
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)
    return text_rect  # Retourne la zone rect pour rendre cliquable

# Menu graphique avec boutons cliquables
def menu():
    pygame.display.set_caption("Menu de sélection")
    
    font = pygame.font.SysFont(None, 50)
    selected = 0  # Option sélectionnée par défaut

    while True:
        SCREEN.fill((0, 0, 0))  # Fond noir

        # Dessiner les options de menu
        option1_rect = draw_text("1. Déplacement Aléatoire", font, GREEN if selected == 0 else WHITE, SCREEN, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3)
        option2_rect = draw_text("2. Algorithme de Balayage", font, GREEN if selected == 1 else WHITE, SCREEN, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        option3_rect = draw_text("3. Quitter", font, GREEN if selected == 2 else WHITE, SCREEN, WINDOW_WIDTH // 2, 2 * WINDOW_HEIGHT // 3)

        pygame.display.update()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:  # Navigation clavier
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 3
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % 3
                elif event.key == pygame.K_RETURN:  # Sélection avec Entrée
                    if selected == 0:
                        random_algo.run(menu)  # Passer le menu pour revenir après
                    elif selected == 1:
                        algo_balayage.run(menu)  # Passer le menu pour revenir après
                    elif selected == 2:
                        pygame.quit()
                        sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # Détection du clic
                if option1_rect.collidepoint(event.pos):
                    pygame.display.set_caption("Déplacement Aléatoire")
                    random_algo.run(menu)  # Lancer algo aléatoire
                elif option2_rect.collidepoint(event.pos):
                    pygame.display.set_caption("Algorithme de Balayage")
                    algo_balayage.run(menu)  # Lancer algorithme de balayage
                elif option3_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        CLOCK.tick(30)

def main():
    pygame.init()
    menu()

if __name__ == "__main__":
    main()
