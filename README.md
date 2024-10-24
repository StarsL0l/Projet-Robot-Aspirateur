# Projet-Robot-Aspirateur

## Description

Ce projet vise à concevoir et mettre en œuvre un prototype de robot aspirateur capable de naviguer de manière autonome. Le robot utilise divers capteurs et algorithmes pour se déplacer efficacement tout en évitant les obstacles.

## Contenu du projet

- `config.py` : Contient les configurations et paramètres nécessaires au le fonctionnement du robot.
- `grid.py` : Gère la création et la manipulation de la grille de navigation.
- `main.py` : Fichier pour exécuter les fonctions du robot avec une interface.
- `robot.py` : Code source définissant le comportement et les actions du robot aspirateur.
- `main2.py` : Fichier pour exécuter uniquement la fonction de balayage.
- `algo_balayage.py` : Algorithme de balayage.
- `random_algo.py` : Algorithme de déplacement aléatoire.
- `moyenne_algo.py` : Programme qui permet de calculer le nombre moyen d'étapes que le robot doit faire dans une même pièce, en simulant plusieurs fois `random_algo.py` (l'utilisateur entre le nombre voulu).


  
## Fonctionnalités

- **Navigation autonome** : Le robot se déplace de manière indépendante dans une zone définie.
- **Évitement d'obstacles** : Utilisation de capteurs pour détecter et éviter les obstacles sur son chemin.

## Installation

1. **Clonez le dépôt :** 
   
```bash
   git clone https://github.com/StarsL0l/Projet-Robot-Aspirateur.git
```

2. **Naviguez dans le répertoire du projet :**

```bash
   cd Projet-Robot-Aspirateur
```
3. **Installez les dépendances :**

```bash
   pip install -r requirements.txt
```
## Utilisation

- **Exécuter le projet :**
  
```bash
   python3 main.py
```

## Crédit
- LESIEUX Thomas
- BRIAUT Lilian
- BARTCZAK Antoine





