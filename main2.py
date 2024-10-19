import sys
import pygame
import random as rd
import time

# Définition des couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

#définition des objets
Poussière = 0
Nettoyé = 1
Mur = 2
Obstacle = 3

# Nombre et taille des blocs souhaités
SIZE = 50
BLOCKS_X = 15  # Nombre de blocs en largeur
BLOCKS_Y = 15  # Nombre de blocs en hauteur

# Définition de la taille de l'écran
WINDOW_HEIGHT = BLOCKS_X * SIZE
WINDOW_WIDTH = BLOCKS_Y * SIZE

# Calculer la taille des blocs en fonction du nombre souhaité
blockSize_x = WINDOW_WIDTH // BLOCKS_X
blockSize_y = WINDOW_HEIGHT // BLOCKS_Y

# Définition des coordonnées
x = [k for k in range(0, WINDOW_WIDTH, blockSize_x)]
y = [k for k in range(0, WINDOW_HEIGHT, blockSize_y)]

# Grille pour suivre l'état de nettoyage et les obstacles
grid = [[Poussière for _ in range(BLOCKS_Y)] for _ in range(BLOCKS_X)]

texture = False


def initialize_grid():
    # Création des murs extérieurs
    for i in range(BLOCKS_X):
        grid[i][0] = grid[i][-1] = Mur  # Murs du haut et du bas
    for j in range(BLOCKS_Y):
        grid[0][j] = grid[-1][j] = Mur  # Murs de gauche et de droite
    
    # Création d'obstacles aléatoires
    num_obstacles = rd.randint(10, 15)  # Nombre d'obstacles entre 30 et 50
    for _ in range(num_obstacles):
        while True:
            x_alea = rd.randint(1, BLOCKS_X - 2)
            y_alea = rd.randint(1, BLOCKS_Y - 2)
            if grid[x_alea][y_alea] == Poussière:
                grid[x_alea][y_alea] = 3
                break

def inverse_orientation(orientation):
    # Inverser l'orientation lors du retour en arrière
    return (orientation + 180) % 360

def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    font = pygame.font.SysFont(None, 50, bold=True)

    initialize_grid()
    
    #placement du robot en aléatoire
    robot_x, robot_y = rd.randint(1, BLOCKS_X - 2), rd.randint(1, BLOCKS_Y - 2)
    while grid[robot_x][robot_y] != Poussière:
        robot_x, robot_y = rd.randint(1, BLOCKS_X - 2), rd.randint(1, BLOCKS_Y - 2)


    orientation = 0  # Orientation initiale du robot
    stack = [(robot_x, robot_y, orientation)]  # Pile avec les positions et orientations
    cleaning_finished = False

    compteur = 0  # Compteur pour les étapes

    while True:
        SCREEN.fill(GRAY)
        drawGrid()
        moveRobot(robot_x, robot_y, orientation)

        #print(f"-------------\norientation {orientation}\nstack {stack[-1][-1]}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not cleaning_finished:
            # Déplacer le robot
            compteur += 1 
            new_x, new_y, new_orientation = getNextPosition(robot_x, robot_y, orientation)

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
                

        if cleaning_finished:
            text = font.render(f"Nettoyage terminé ! Cela a pris {compteur} étapes", True, RED)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            SCREEN.blit(text, text_rect)

        pygame.display.update()

        # Attendre un peu pour ralentir l'animation
        time.sleep(0.1)

def drawGrid():
    for i in range(BLOCKS_X):
        for j in range(BLOCKS_Y):
            rect = pygame.Rect(x[i], y[j], blockSize_x, blockSize_y)
            if grid[i][j] == Poussière:  # Poussières
                
                # Mise en comentaire de la la texture de la pousière car cela fait trop surcharger
                # et ralenti la simulation
                # 
                # if not texture:
                #     image = pygame.image.load("dust_icon.png")
                #     image = pygame.transform.scale(image, (blockSize_x, blockSize_y))
                #     SCREEN.blit(image, (x[i], y[j]))
                # else:
                    pygame.draw.rect(SCREEN, GRAY, rect, 0)

            elif grid[i][j] == Nettoyé:  # Nettoyé
                pygame.draw.rect(SCREEN, WHITE, rect, 0)

            elif grid[i][j] == Mur:  # Murs
                if texture:
                    image = pygame.image.load("data/wall_icon.jpg")
                    image = pygame.transform.scale(image, (blockSize_x, blockSize_y))
                    SCREEN.blit(image, (x[i], y[j]))
                else:
                    pygame.draw.rect(SCREEN, BLACK, rect, 0)

            elif grid[i][j] == Obstacle:  # Obstacle
                if texture:
                    image = pygame.image.load("data/wood.jpeg")
                    image = pygame.transform.scale(image, (blockSize_x, blockSize_y))
                    SCREEN.blit(image, (x[i], y[j]))
                else:
                    pygame.draw.rect(SCREEN, BLACK, rect, 0)

            pygame.draw.rect(SCREEN, BLACK, rect, 1)

def moveRobot(i, j, orientation):
    # Marquer la case comme nettoyée
    grid[i][j] = Nettoyé
    
    # Dessiner le robot avec orientation
    if texture:
        image = pygame.image.load("data/robot_aspi.png")
        image = pygame.transform.scale(image, (blockSize_x, blockSize_y))
        image = pygame.transform.rotate(image, orientation)
        SCREEN.blit(image, (x[i], y[j]))
    else:
        rect = pygame.Rect(x[i], y[j], blockSize_x, blockSize_y)
        pygame.draw.rect(SCREEN, BLUE, rect, 0)



def getNextPosition(i, j, orientation):
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

    # Si aucune direction n'est possible, rester sur place et garder la même orientation
    return i, j, orientation

if __name__ == "__main__":
    main()
