from UTILITY.UTILITY import *
import random as rd
import numpy as np
from time import time
from math import pi

### RENDU GRAPHIQUE
LARGEUR     = 7
HAUTEUR     = 13
RATIO       = 44

LARGEUR = 12 
HAUTEUR = 20
RATIO   = 30

### ETAT DU JEU
etat_jeu           = ""
etat_jeu_precedent = "" # utile quand le joueur veut aller dans le bestiaire en pleine partie !  

### LE SCORE
score       = 0
combo       = 0
point       = 0

### L'ANIMATION 
frames      = 0
pas         = 0

### GRILLE
grille      = []
alignements = []

### LES ETATS DES CASES DE LA GRILLE
VIDE          = "VIDE"
ETATS_BRIQUES = [RED, GREEN, BLUE, CYAN, YELLOW, MAGENTA]
BRIQUES       = []

### LE BARREAU
x           = 0
y           = 0
k           = 3

### LES CREATURES
creaturesConnues = []
creatureSelectionnee = 0

### VITESSE DE JEU ET TEMPS
# the speed is doubled every tau0 frames
maxspeed    = 10
f0          = 360
tau0        = 1500
tau         = tau0/np.log(2)
f           = lambda t : int((f0 - maxspeed) * np.exp(-t/tau)) + maxspeed

SPEED       = 0

temps        = 0
instants_de_jeu = []

def creerGrille(largeur : int, hauteur : int) -> list:
    
    return [[VIDE for _ in range(hauteur)] for _ in range(largeur)]
    
def afficherGrille(grille : list, x_b : int, y_b : int, alignements : list) -> None:
    
    largeur = len(grille)
    hauteur = len(grille[0])

    background(BLACK)
    for x in range(largeur):
        for y in range(hauteur):
            if (x, hauteur - 1 - y) in alignements:
                strokeWeight(3)
                stroke(WHITE)
            else:
                strokeWeight(1)
                stroke(GRAY)
            if grille[x][hauteur - 1 - y] == VIDE:
                if x == x_b and hauteur - 1 - y < y_b:
                    fill(DARK_GRAY)
                else:
                    fill(BLACK)
            else:
                fill(ETATS_BRIQUES[grille[x][hauteur - 1 - y]])
            rectangle((RATIO*x, RATIO*y), RATIO, RATIO)
       
       
def chargerBriques():
    briques = []
    
    prefixes = ["rouge", "vert", "bleu", "cyan", "jaune", "magenta"]
    for prefixe in prefixes:
        brique = []
        brique.append(Image(prefixe + "_0000.png"))
        brique.append(Image(prefixe + "_0001.png"))
        brique.append(Image(prefixe + "_0010.png"))
        brique.append(Image(prefixe + "_0011.png"))
        brique.append(Image(prefixe + "_0100.png"))
        brique.append(Image(prefixe + "_0101.png"))
        brique.append(Image(prefixe + "_0110.png"))
        brique.append(Image(prefixe + "_0111.png"))
        brique.append(Image(prefixe + "_1000.png"))
        brique.append(Image(prefixe + "_1001.png"))
        brique.append(Image(prefixe + "_1010.png"))
        brique.append(Image(prefixe + "_1011.png"))
        brique.append(Image(prefixe + "_1100.png"))
        brique.append(Image(prefixe + "_1101.png"))
        brique.append(Image(prefixe + "_1110.png"))
        brique.append(Image(prefixe + "_1111.png"))
        briques.append(brique)
    return briques
    
### GESTION DU BARREAU
def grilleLibre(grille : list, k : int) -> list:
    largeur = len(grille)
    hauteur = len(grille[0])
    
    libre = []
    for x in range(largeur):
        colonneLibre = True
        for j in range(k):
            if grille[x][hauteur - 1 - j] != VIDE:
                colonneLibre = False
        if colonneLibre: libre.append(x)
    return libre
    
def creerBarreau(grille : list, x : int, y : int, k : int) -> None:
    n = len(ETATS_BRIQUES)
    indices = [k for k in range(n)] 
    couleurs = [rd.choice(indices) for _ in range(k)]
    while couleurs.count(couleurs[0]) == len(couleurs):
        couleurs = [rd.choice(indices) for _ in range(k)]
    for i in range(k):
        grille[x][y + i] = couleurs[i]
    
def descente(grille : list, x : int, y : int, k : int) -> bool:
    if y > 0 and grille[x][y - 1] == VIDE:
        for i in range(k):
            grille[x][y - 1 + i] = grille[x][y + i]
        grille[x][y + k - 1] = VIDE
        return True
    else:
        return False

def deplacerBarreau(grille : list, x : int, y : int, k : int, direction : [-1, 1]) -> bool:
    largeur = len(grille)
    
    if (direction == -1 and x > 0) or (direction == 1 and x < largeur - 1):
        libre = True
        for i in range(k):
            if grille[x + direction][y + i] is not VIDE:
                libre = False
        if libre:
            for i in range(k):
                grille[x + direction][y + i] = grille[x][y + i]
                grille[x][y + i] = VIDE
            x += direction
    return x
        
def permuterBarreau(grille : list, x : int, y : int, k : int) -> None:
    haut = grille[x][y + k - 1]
    for i in range(k - 1):
        grille[x][y + k - 1 - i] = grille[x][y + k - 2 - i]
    grille[x][y] = haut
        
def descenteRapide(grille : list, x : int, y : int, k : int) -> int:
    delta = 0
    y_ = y - 1
    while y_ >= 0 and grille[x][y_] == VIDE:
        y_ -= 1
        delta += 1
    if delta != 0:
        for i in range(k):
            grille[x][y - delta + i] = grille[x][y + i]
            grille[x][y + i] = VIDE
    return y - delta
# # #
        
### GESTION DE LA GRILLE ET DES SCORES UNE FOIS UN COUP DU JOUEUR EFFECTUE
def detecteAlignement(rangee : list) -> tuple:
    n = len(rangee)
    marking = [False for _ in range(n)]
    m = 0
    etat = rangee[0]
    for i in range(n):
        if etat == rangee[i]:
            m += 1
        else:
            if etat is not VIDE and m >= 3:
                for j in range(m):
                    marking[i - 1 - j] = True
            m = 1
            etat = rangee[i]
    if etat is not VIDE and m >= 3:
        for j in range(m):
            marking[n - 1 - j] = True
    return marking
    
def scoreRangee(grille : list, i: int, j : int, dx : int, dy : int) -> int:
    def creerRangee(grille : list, i: int, j : int, dx : int, dy : int) -> list:
        rangee = []
        largeur = len(grille)
        hauteur = len(grille[0])
        x, y = i, j
        while 0 <= x < largeur and 0 <= y < hauteur:
            rangee.append(grille[x][y])
            x += dx
            y += dy
        return rangee
        
    def nettoyerRangee(i : int, 
                       j : int, 
                       dx : [-1, 0, 1], 
                       dy : [-1, 0, 1], 
                       marking : list) -> list:
        marquage = []
        for l in range(len(marking)):
            if marking[l]:
                marquage.append((i + l*dx, j + l*dy))
        return marquage
        
    return nettoyerRangee(i, j, dx, dy, detecteAlignement(creerRangee(grille, i, j, dx, dy)))
    
def marquerAlignements(grille : list) -> tuple:
    largeur = len(grille)
    hauteur = len(grille[0])
    marquage = []

    def inspecterRangee(grille : list, i: int, j : int, dx : int, dy : int, marquage : list) -> None:
        net = scoreRangee(grille, i, j, dx, dy)
        marquage += net
        
    inspecterRangee(grille, 0, 0, 0, 1, marquage)
    inspecterRangee(grille, largeur - 1, 0, 0, 1, marquage)
          
    for x in range(1, largeur - 1):
        inspecterRangee(grille, x, 0, 0,  1, marquage)
        inspecterRangee(grille, x, 0, 1,  1, marquage)
        inspecterRangee(grille, x, 0, -1, 1, marquage)
        
    for y in range(hauteur):
        inspecterRangee(grille, 0, y, 1, 0, marquage)
        inspecterRangee(grille, 0, y, 1, 1, marquage)
        
        inspecterRangee(grille, largeur - 1, y, -1, 1, marquage)
    
    return marquage

def effacerAlignements(grille : list, alignements : list) -> None:
    for block in alignements:
        x = block[0]
        y = block[1]
        grille[x][y] = VIDE

def tassementGrille(grille) -> bool:
    tasse = False
    largeur = len(grille)
    
    def descenteColonne(grille : list, x : int) -> bool:
        hauteur = len(grille[0])
        tasse_ = False
        for y in range(1, hauteur):
            if grille[x][y] is not VIDE:
                delta = 0
                y_ = y - 1
                while y_ >= 0 and grille[x][y_] == VIDE:
                    y_ -= 1
                    delta += 1
                grille[x][y - delta] = grille[x][y]
                if delta > 0: tasse_ = True; grille[x][y] = VIDE
        return tasse_
        
    for x in range(largeur):
        if descenteColonne(grille, x): tasse = True
    return tasse
# # #

### GESTION DES CREATURES
def chargerCreaturesConnues(nameOfFile = "creatures.txt") -> list:
    f = open(nameOfFile, mode = 'r')
    creatures = f.readlines()
    f.close()
    
    n = len(creatures)
    for i in range(n):
        creatures[i] = creatures[i].replace("\n", "")
        creatures[i] = creatures[i].split("|")
        
        # la créature
        creatures[i][0] = creatures[i][0].split(":")
        for j in range(len(creatures[i][0])):
            creatures[i][0][j] = creatures[i][0][j].split(".")
            for l in range(len(creatures[i][0][j])):
                creatures[i][0][j][l] = int(creatures[i][0][j][l])
        # la fréquence des couleurs
        creatures[i][1] = creatures[i][1].split(".")
        for j in range(len(creatures[i][1])):
            creatures[i][1][j] = int(creatures[i][1][j])
        
    return creatures
    
def construireCreatures(grille : list, marquage : list, nameOfFile = "creatures.txt") -> None:
    n = len(ETATS_BRIQUES)
    creatures = [[] for _ in range(n)]
    for x, y in marquage:
        creatures[grille[x][y]].append((x, y))
    
    def naissanceCreature(creature : list) -> list:
        Xs, Ys = [], []
        for (x, y) in creature:
            Xs.append(x)
            Ys.append(y)
            
        dx, dy = min(Xs), min(Ys)
        largeur = max(Xs) - min(Xs) + 1
        hauteur = max(Ys) - min(Ys) + 1
        creature_ = [[0 for _ in range(hauteur)] for _ in range(largeur)]
        for (x, y) in creature:
            creature_[x - dx][hauteur - 1 - (y - dy)] = 1
        
        return creature_
    
    return [[naissanceCreature(creatures[i]), i] for i in range(len(creatures)) if creatures[i] != []]
    
def alignementDansCreature(rangee : list) -> tuple:
    n = len(rangee)
    
    nombre_alignements = 0
    longueur = 0
    valeur = rangee[0]
    for bloc in rangee:
        if valeur == bloc:
            longueur += 1
        else:
            if longueur >= 3 and valeur: nombre_alignements += 1
            longueur = 1
            valeur = bloc
    if longueur >= 3 and valeur:
        nombre_alignements += 1
    
    return nombre_alignements
    
def scoreRangeeCreature(creature : list, i: int, j : int, dx : int, dy : int) -> int:
    def creerRangee(creature : list, i: int, j : int, dx : int, dy : int) -> list:
        rangee = []
        largeur = len(creature)
        hauteur = len(creature[0])
        x, y = i, j
        while 0 <= x < largeur and 0 <= y < hauteur:
            rangee.append(creature[x][y])
            x += dx
            y += dy
        return rangee
        
    return alignementDansCreature(creerRangee(creature, i, j, dx, dy))
    
def calculerScoreCreature(creature : list) -> int:
    largeur = len(creature)
    hauteur = len(creature[0])
    nombre_alignements = []

    def inspecterRangee(creature : list, i: int, j : int, dx : int, dy : int, nombre_alignements : list) -> None:
        n_a = scoreRangeeCreature(creature, i, j, dx, dy)
        nombre_alignements.append(n_a)
        
    inspecterRangee(creature, 0, 0, 0, 1, nombre_alignements)
    if largeur != 1:
        inspecterRangee(creature, largeur - 1, 0, 0, 1, nombre_alignements)
          
    for x in range(1, largeur - 1):
        inspecterRangee(creature, x, 0, 0,  1, nombre_alignements)
        inspecterRangee(creature, x, 0, 1,  1, nombre_alignements)
        inspecterRangee(creature, x, 0, -1, 1, nombre_alignements)
        
    for y in range(hauteur):
        inspecterRangee(creature, 0, y, 1, 0, nombre_alignements)
        inspecterRangee(creature, 0, y, 1, 1, nombre_alignements)
        
        inspecterRangee(creature, largeur - 1, y, -1, 1, nombre_alignements)
    
    return sum([sum(colonne) for colonne in creature]), sum(nombre_alignements)
    
    
def trierCreatures(creaturesConnues : list) -> list:
    n = len(creaturesConnues)
    creatures_temp = []
    for i in range(n):
        poids, complexite = calculerScoreCreature(creaturesConnues[i][0]) 
        points            = poids * complexite
        
        total_de_capture  = sum(creaturesConnues[i][1])
        total_de_capture  = float("inf") if total_de_capture == 0 else 1/total_de_capture
        
        h                 = len(creaturesConnues[i][0][0])
        l                 = len(creaturesConnues[i][0])
        surface           = h * l
        
        creatures_temp.append((points, poids, complexite, surface, total_de_capture, creaturesConnues[i][1], i))
    creatures_temp.sort()
    return [creaturesConnues[creatures_temp[i][-1]] for i in range(n)]
        
    
def gererNouvellesCreatures(creatures : list, creaturesCapturees : list) -> list:
    def lesMemesCreatures(creatureA : list, creatureB : list) -> bool:
        lA = len(creatureA)
        hA = len(creatureA[0])
        lB = len(creatureB)
        hB = len(creatureB[0])
        if lA != lB or hA != hB: return False
        else:
            normal = True
            # miroir = True
            for x in range(lA):
                for y in range(hA):
                    if creatureA[x][y]          != creatureB[x][y]:          normal = False
                    # if creatureA[lA - 1 - x][y] != creatureB[lA - 1 - x][y]: miroir = False
            return normal #or miroir
        
    nouvelles = []
    for (creatureB, i_couleur) in creaturesCapturees:
        connue = False
        for A in range(len(creatures)):
            if lesMemesCreatures(creatures[A][0], creatureB):
                connue = True
                creatures[A][1][i_couleur] += 1
                break
        if not connue: 
            creatures.append([creatureB, [1 if i == i_couleur else 0 for i in range(len(ETATS_BRIQUES))]]) 
            nouvelles.append(creatures[-1])
            
        
    return trierCreatures(creatures), nouvelles
    
    
def calculerFamille(creature : list) -> list:
    def retournement_hoziontal(creature : list) -> list:
        return [[creature[len(creature) - 1 - i][j] for j in range(len(creature[0]))] for i in range(len(creature))]
    def retournement_vertical(creature : list) -> list:
        return [[creature[i][len(creature[0]) - 1 - j] for j in range(len(creature[0]))] for i in range(len(creature))]
    def rotation(creature : list) -> list:
        return retournement_hoziontal([[creature[i][j] for i in range(len(creature))] for j in range(len(creature[0]))])
    
    famille = []
    crea = creature
    for _ in range(4):
        if crea not in famille: famille.append(crea) 
        creah  = retournement_hoziontal(crea)
        if creah not in famille: famille.append(creah)
        creav  = retournement_vertical(crea)
        if creav not in famille: famille.append(creav)
        creahv = retournement_vertical(creah)
        if creahv not in famille: famille.append(creahv)
        crea = rotation(crea)
    
    return famille
    
def montrerCreature(x : int, y : int, c : int, creature : list, informations = True) -> None:
    l = len(creature[0])
    h = len(creature[0][0])
    d = max(l, h)
    s = c / d
    
    fill(BLACK)
    rectangle((x, y), l*s, h*s)
    
    stroke(BLACK)
    strokeWeight(1)
    fill(GRAY)
    for i in range(l):
        for j in range(h):
            if creature[0][i][j]: rectangle((x + i*s, y + j*s), s, s)
            
    stroke(LIGHT_GRAY)
    strokeWeight(3)
    noFill()
    rectangle((x, y), l*s, h*s)
    
    if informations:
        poids, complexite = calculerScoreCreature(creature[0])
        write(str(poids * complexite), RED, (x + 50, y - 50))
        
        nombre_de_captures = sum(creature[1])
        angles = [2*pi * creature[1][i]/nombre_de_captures for i in range(len(creature[1]))]
        
        angle = 0
        for i in range(len(angles)):
            pygame.draw.arc(INFO.SCREEN, ETATS_BRIQUES[i], (INFO.width//2, INFO.height//2 + 150, 100, 100), angle, angle + angles[i], 48)
            angle += angles[i]
        write(str(nombre_de_captures), WHITE, (x + 150, y + 300))
    
    
def sauvegarderCreatures(creaturesConnues : list, nameOfFile = "creatures.txt") -> None:
    f = open(nameOfFile, mode = "w")
    for creature in creaturesConnues:
        # la créature
        for i in range(len(creature[0])):
            for j in range(len(creature[0][i])):
                f.write(str(creature[0][i][j]))
                if j != len(creature[0][i]) - 1: f.write(".")
            if i != len(creature[0]) - 1: f.write(":")
        f.write("|")
        # la frequence de capture des couleurs
        for i in range(len(creature[1])):
            f.write(str(creature[1][i]))
            if i != len(creature[1]) - 1: f.write(".") 
        f.write("\n")
    f.close()
    return None
# # #
    
### LES SCORES
def sauvegarderEtMontrerScores(nameOfFile, score):
    ### EXTRACTION DES SCORES DAND LE FICHIER 'nameOfFile'
    f = open(nameOfFile, mode = "r")
    scores = f.readlines()
    f.close()
    n = len(scores)
    for i in range(n):
        scores[i] = scores[i].replace("\n", "")
        scores[i] = scores[i].replace("\t", "")
        scores[i] = scores[i].replace("-", "")
        scores[i] = scores[i].replace(".", "")
        scores[i] = scores[i].split(" ")
        
        # on remet le score sous forme d'entier
        scores[i][1] = scores[i][1].split(",")
        score_ = ""
        for s in scores[i][1]:
            score_ += s
        
        scores[i][0] = int(scores[i][0])         # le rang
        scores[i][1] = int(score_)               # le score
        scores[i].pop(2)                         # on enlève les mots en trop
        scores[i].pop(-2)
        
        scores[i][2] = scores[i][2].split("/")   # la date 
        for j in range(len(scores[i][2])):
            scores[i][2][j] = int(scores[i][2][j])
            
        scores[i][-1] = scores[i][-1].split(":") # l'heure 
        for j in range(len(scores[i][-1])):
            scores[i][-1][j] = int(scores[i][-1][j])
    # # #
            
        ## score, année, mois, jour, heure, minute, seconde
        scores[i] = [scores[i][1], scores[i][2][2], scores[i][2][1], scores[i][2][0], scores[i][3][0], scores[i][3][1], scores[i][3][2]]
        
    from datetime import datetime as dt
    date = dt.now()
    scores.append([score, int(date.year), 
                          int(date.month), 
                          int(date.day), 
                          int(date.hour), 
                          int(date.minute), 
                          int(date.second)])
    # # #
                          
    ### tri par ordre décroissant
    scores.sort()
    scores.reverse()
    # # #
    
    # on réécrit les scores dans le fichier textes des scores
    f = open(nameOfFile, mode = "w")
    print("Voici les meilleurs scores obtenus sur ce compte :\n")
    for i in range(n + 1):
        line = str(i + 1) + "- ....." + str(scores[i][0]) + " \tle " + str(scores[i][3]) + "/" + str(scores[i][2]) + "/" + str(scores[i][1]) + " à " + str(scores[i][4]) + ":" + str(scores[i][5]) + ":" + str(scores[i][6]) + "\n"
        f.write(line)
        if i < 10:
            print("\t{}".format(line))
    
    print()    
    f.close()
# # #

### RACCOURCIS
def commencerUnePartie():
    global grille, etat_jeu, score, temps, instants_de_jeu
    
    grille = creerGrille(LARGEUR, HAUTEUR)
    etat_jeu = "creer_barreau"
    score = 0
    temps = 0
    
    instants_de_jeu = []
# # #
            
def setup():
    canvas(LARGEUR * RATIO, HAUTEUR * RATIO + 30, font = 30)
    
    ### INITIALISATION
    global grille, pas, etat_jeu, etat_jeu_precedent, x, y, score, frames, temps, alignements, combo, creaturesConnues, nouvellesCreatures, creatureSelectionnee, point, instants_de_jeu, BRIQUES
    commencerUnePartie()
    alignements = []
    
    creaturesConnues = chargerCreaturesConnues()
    nouvellesCreatures = []
    creatureSelectionnee = 0
    
    BRIQUES = chargerBriques()
    
    pas      = 0
    combo    = 1
    point    = 0
    frames   = 10
    x, y     = None, None
    etat_jeu = "menu_principal_jeu"
    etat_jeu_precedent = "creer_barreau"
    # # #
    
    print(INFO.FONT.size("coucou"))
    
    
def draw():
    global grille, pas, etat_jeu, etat_jeu_precedent, x, y, score, frames, temps, alignements, combo, creaturesConnues, nouvellesCreatures, creatureSelectionnee, point, instants_de_jeu, BRIQUES
    
    ### MENU PRINCIPAL
    if etat_jeu in ["menu_principal_jeu", "menu_principal_bestiaire", "menu_principal_stats", "menu_principal_options", "menu_principal_quitter"]:
        # print("menu_principal")
        background(BLACK)
        couleur_jouer = couleur_bestiaire = couleur_quitter = couleur_stats = couleur_options = GRAY
        if etat_jeu == "menu_principal_jeu":
            couleur_jouer = WHITE
        elif etat_jeu == "menu_principal_bestiaire":
            couleur_bestiaire = WHITE
        elif etat_jeu == "menu_principal_stats":
            couleur_stats = WHITE
        elif etat_jeu == "menu_principal_options":
            couleur_options = WHITE
        elif etat_jeu == "menu_principal_quitter":
            couleur_quitter = WHITE
            
        write("Jouer", couleur_jouer, (10, 10))
        write("Bestiaire", couleur_bestiaire, (10, 50))
        write("Stats", couleur_stats, (10, 90))
        write("Options", couleur_options, (10, 130))
        write("Quitter", couleur_quitter, (10, 170))
        
        if K_DOWN in INFO.KEYS:
            if etat_jeu == "menu_principal_jeu":
                etat_jeu = "menu_principal_bestiaire"
            elif etat_jeu == "menu_principal_bestiaire":
                etat_jeu = "menu_principal_stats"
            elif etat_jeu == "menu_principal_stats":
                etat_jeu = "menu_principal_options"
            elif etat_jeu == "menu_principal_options":
                etat_jeu = "menu_principal_quitter"
        elif K_UP in INFO.KEYS:
            if etat_jeu == "menu_principal_quitter":
                etat_jeu = "menu_principal_options"
            elif etat_jeu == "menu_principal_options":
                etat_jeu = "menu_principal_stats"
            elif etat_jeu == "menu_principal_stats":
                etat_jeu = "menu_principal_bestiaire"
            elif etat_jeu == "menu_principal_bestiaire":
                etat_jeu = "menu_principal_jeu"
        elif K_RETURN in INFO.KEYS:
            if etat_jeu == "menu_principal_jeu":
                etat_jeu = etat_jeu_precedent
                instants_de_jeu.append(time())
            elif etat_jeu == "menu_principal_bestiaire":
                canvas(INFO.width + 300, INFO.height, font = 30)
                etat_jeu = "bestiaire_principal"
            elif etat_jeu == "menu_principal_stats":
                etat_jeu = "stats_principal"
            elif etat_jeu == "menu_principal_options":
                etat_jeu = "options_principal"
            elif etat_jeu == "menu_principal_quitter":
                INFO.CONTINUER = False
        if K_ESCAPE in INFO.KEYS:
            INFO.CONTINUER = False
    # # #
        
    ### LE BESTIAIRE
    elif etat_jeu in ["bestiaire_principal", "bestiaire_en_jeu"]:
        background(BLACK)
        N = len(creaturesConnues)
        c = 50
        surligner = [True if i == creatureSelectionnee else False for i in range(N)]
        
        dy = max((creatureSelectionnee + 1)*c - INFO.height, 0)

        for i in range(N):
            strokeWeight(2)
            stroke(GRAY)
            if surligner[i]: fill(WHITE)
            else:            fill(LIGHT_GRAY)
            rectangle((0, i*c - dy), 3*c, c)
            write(str(i), BLACK, (1.4*c, i*c - dy + 0.4*c))
            
        if creaturesConnues != []:
            montrerCreature(INFO.w/2, INFO.h/2 - 100, 200, creaturesConnues[creatureSelectionnee], sum(creaturesConnues[creatureSelectionnee][1]) != 0)
        
            
        if K_DOWN in INFO.KEYS and creatureSelectionnee < N - 1:
            creatureSelectionnee += 1
        elif K_UP in INFO.KEYS and creatureSelectionnee > 0:
            creatureSelectionnee -= 1
        elif K_ESCAPE in INFO.KEYS:
            canvas(INFO.width - 300, INFO.height, font = 30)
            if etat_jeu == "bestiaire_principal":
                etat_jeu = "menu_principal_bestiaire"
            elif etat_jeu == "bestiaire_en_jeu":
                etat_jeu = "menu_jeu_bestiaire"
            INFO.CONTINUER = True
    # # #    
        
    ### LES STATS
    elif etat_jeu in ["stats_principal", "stats_en_jeu"]:
        background(BLACK)
        write("stats", WHITE, (10, 10))
        if K_ESCAPE in INFO.KEYS:
            if etat_jeu == "stats_principal":
                etat_jeu = "menu_principal_stats"
            elif etat_jeu == "stats_en_jeu":
                etat_jeu = "menu_jeu_stats"
            INFO.CONTINUER = True
    # # #
    
    ### LES OPTIONS
    elif etat_jeu in ["options_principal", "options_en_jeu"]:
        background(BLACK)
        write("options", WHITE, (10, 10))
        if K_ESCAPE in INFO.KEYS:
            if etat_jeu == "options_principal":
                etat_jeu = "menu_principal_options"
            elif etat_jeu == "options_en_jeu":
                etat_jeu = "menu_jeu_options"
            INFO.CONTINUER = True
    # # #
    
    else:
        afficherGrille(grille, x, y, alignements)
        SPEED = f(temps)
        
        ### MENU EN JEU
        if etat_jeu in ["menu_jeu_jeu", "menu_jeu_recommencer", "menu_jeu_bestiaire", "menu_jeu_stats", "menu_jeu_options", "menu_jeu_principal"]:
            # print("menu en jeu")
            couleur_jouer = couleur_recommencer = couleur_bestiaire = couleur_stats = couleur_options = couleur_principal = GRAY
            if etat_jeu == "menu_jeu_jeu":
                couleur_jouer = WHITE
            elif etat_jeu == "menu_jeu_recommencer":
                couleur_recommencer = WHITE
            elif etat_jeu == "menu_jeu_bestiaire":
                couleur_bestiaire = WHITE
            elif etat_jeu == "menu_jeu_stats":
                couleur_stats = WHITE
            elif etat_jeu == "menu_jeu_options":
                couleur_options = WHITE
            elif etat_jeu == "menu_jeu_principal":
                couleur_principal = WHITE
                
            strokeWeight(3)
            stroke(LIGHT_GRAY)
            fill(BLACK)
            rectangle((INFO.width/2 - 150, INFO.height/2 - 50), 300, 300)
            write("Jouer", couleur_jouer, (10 + INFO.width/2 - 150, 10 + INFO.height/2 - 50))
            write("Recommencer", couleur_recommencer, (10 + INFO.width/2 - 150, 50 + INFO.height/2 - 50))
            write("Bestiaire", couleur_bestiaire, (10 + INFO.width/2 - 150, 90 + INFO.height/2 - 50))
            write("Stats", couleur_stats, (10 + INFO.width/2 - 150, 130 + INFO.height/2 - 50))
            write("Options", couleur_options, (10 + INFO.width/2 - 150, 170 + INFO.height/2 - 50))
            write("Menu principal", couleur_principal, (10 + INFO.width/2 - 150, 210 + INFO.height/2 - 50))
            
            if K_DOWN in INFO.KEYS:
                if etat_jeu == "menu_jeu_jeu":
                    etat_jeu = "menu_jeu_recommencer"
                elif etat_jeu == "menu_jeu_recommencer":
                    etat_jeu = "menu_jeu_bestiaire"
                elif etat_jeu == "menu_jeu_bestiaire":
                    etat_jeu = "menu_jeu_stats"
                elif etat_jeu == "menu_jeu_stats":
                    etat_jeu = "menu_jeu_options"
                elif etat_jeu == "menu_jeu_options":
                    etat_jeu = "menu_jeu_principal"
            elif K_UP in INFO.KEYS:
                if etat_jeu == "menu_jeu_principal":
                    etat_jeu = "menu_jeu_options"
                elif etat_jeu == "menu_jeu_options":
                    etat_jeu = "menu_jeu_stats"
                elif etat_jeu == "menu_jeu_stats":
                    etat_jeu = "menu_jeu_bestiaire"
                elif etat_jeu == "menu_jeu_bestiaire":
                    etat_jeu = "menu_jeu_recommencer"
                elif etat_jeu == "menu_jeu_recommencer":
                    etat_jeu = "menu_jeu_jeu"
            elif K_RETURN in INFO.KEYS:
                if etat_jeu == "menu_jeu_jeu":
                    etat_jeu = etat_jeu_precedent
                    instants_de_jeu.append(time())
                elif etat_jeu == "menu_jeu_recommencer":
                    commencerUnePartie()
                elif etat_jeu == "menu_jeu_bestiaire":
                    canvas(INFO.width + 300, INFO.height, font = 30)
                    etat_jeu = "bestiaire_en_jeu"
                elif etat_jeu == "menu_jeu_stats":
                    etat_jeu = "stats_en_jeu"
                elif etat_jeu == "menu_jeu_options":
                    etat_jeu = "options_en_jeu"
                elif etat_jeu == "menu_jeu_principal":
                    etat_jeu = "menu_principal_jeu"
            if K_ESCAPE in INFO.KEYS:
                etat_jeu = etat_jeu_precedent
                instants_de_jeu.append(time())
                INFO.CONTINUER = True
        # # #
            
        ### CREATION D'UN BARREAU
        elif etat_jeu == "creer_barreau":
            # print("spawn barreau")
            libres = grilleLibre(grille, k)
            # print(libres)
            if libres != []:
                x = rd.choice(libres)
                y = HAUTEUR - k
                creerBarreau(grille, x, y, k)
                etat_jeu = "jeu"
            else:
                instants_de_jeu.append(time())
                t = int(sum([-instants_de_jeu[i] if i % 2 == 0 else instants_de_jeu[i] for i in range(len(instants_de_jeu))]))
                instants_de_jeu = []
                etat_jeu = "perdu"
                print("Vous avez perdu, dommage ! Vous ferez mieux la prochaine fois !!")
                print("Votre score est de {} points".format(score))
                print("Durée de la partie : {} min {} s".format(t//60, t % 60))
                sauvegarderEtMontrerScores("scores.txt", score)
            temps += 1
        # # #
        
        else:
            ### PASSAGE AU MENU EN JEU
            if K_ESCAPE in INFO.KEYS and etat_jeu != "perdu":
                etat_jeu_precedent = etat_jeu
                etat_jeu = "menu_jeu_jeu"
                INFO.CONTINUER = True
                instants_de_jeu.append(time())
            # # #
            
            ### GESTION DE LA DISPARITION DES BLOCS GAGNANTS ET CALCULS DES SCORES
            elif etat_jeu == "disparaitre":
                # print("pas = {}".format(pas))
                if pas == 0:
                    # print("marquer les alignements")
                    alignements = marquerAlignements(grille)
                    creaturesCapturees = construireCreatures(grille, alignements)
                    creaturesConnues, nouvellesCreatures = gererNouvellesCreatures(creaturesConnues, creaturesCapturees)
                    point = 0
                    for creature in creaturesCapturees:
                        poids, complexite = calculerScoreCreature(creature[0])
                        point += poids * complexite
                    if point == 0:
                        # print("aucun alignement..")
                        etat_jeu = "creer_barreau"
                        combo = 0
                    else:
                        combo += 1
                    if nouvellesCreatures != []:
                        pas = 0
                        frames = 120
                        famille = []
                        for creature in nouvellesCreatures:
                            famille += calculerFamille(creature[0])
                        famille = [[crea, [0 for i in ETATS_BRIQUES]] for crea in famille]
                        creaturesConnues += famille[1:]
                        creaturesConnues = trierCreatures(creaturesConnues) 
                elif pas == frames:
                    # print("effacer les alignements")
                    effacerAlignements(grille, alignements)
                    score += point * combo
                    alignements = []
                    frames = 10
                    pas = 10
                elif pas == 2*frames:
                    # print("tassement de la grille")
                    pas = -1
                    if not tassementGrille(grille):
                        etat_jeu = "creer_barreau"
                pas += 1
                
                if nouvellesCreatures != []:
                    x = INFO.w/2 - 55
                    y = INFO.h/2 - 55
                    fill(BLACK)
                    stroke(GRAY)
                    rectangle((x, y), 100, 100)
                    write("Nouvelle", WHITE, (x + 10, y + 10))
                    write("creature" , WHITE, (x + 10, y + 40))
                    write("capturée !" , WHITE, (x + 10, y + 70))
                    
                    for creature in nouvellesCreatures:
                        montrerCreature(x + 5, y + 100, 150, creature, False)
                    
            # # #
                
            ### LE JOUEUR PEUT JOUER
            elif etat_jeu == "jeu":
                # print("coup du joueur")
                if K_LEFT in INFO.KEYS:
                    direction = -1
                elif K_RIGHT in INFO.KEYS:
                    direction = 1
                else:
                    direction = 0
                if K_DOWN in INFO.KEYS:
                    descendreRapide = True
                else:
                    descendreRapide = False
                if K_UP in INFO.KEYS:
                    permuter = True
                else:
                    permuter = False
                    
                if direction:
                    # print("deplace")
                    x = deplacerBarreau(grille, x, y, k, direction)
                if permuter:
                    # print("permuter")
                    permuterBarreau(grille, x, y, k)
                    
                if descendreRapide:
                    # print("rapide")
                    y = descenteRapide(grille, x, y, k)
                    # print("animation")
                    etat_jeu = "disparaitre"
                    pas = 0
                    combo = 0
                elif temps % SPEED == 0:
                    if descente(grille, x, y, k):
                        # print("descente")
                        y -= 1
                    else:
                        # print("animation")
                        etat_jeu = "disparaitre"
                        pas = 0
                        combo = 0
                temps += 1
            # # #
               
            ### DEFAITE
            elif etat_jeu == "perdu":
                stroke(LIGHT_GRAY)
                fill(0)
                rectangle((0, 0), INFO.w, 30)
                write("'Entrée' pour recommencer", WHITE, (10, 5))
                if K_ESCAPE in INFO.KEYS:
                    commencerUnePartie()
                    etat_jeu = "menu_principal_jeu"
                    INFO.CONTINUER = True
                elif K_RETURN in INFO.KEYS:
                    commencerUnePartie()
                    instants_de_jeu.append(time())
                        
            # # #
        
        if etat_jeu in ["jeu", "creer_barreau", "disparaitre", "menu_jeu_jeu", "menu_jeu_bestiaire", "menu_jeu_principal", "menu_jeu_recommencer", "menu_jeu_stats", "menu_jeu_options", "perdu"]:
            write("score = {}".format(score), WHITE, (RATIO * (1/2), RATIO * (HAUTEUR + 0.1)))
            if etat_jeu == "disparaitre" and point != 0:
                write("+ {} x {}".format(point, combo), WHITE, (RATIO * (4.7), RATIO * (HAUTEUR + 0.1)))
            
            
def finish():
    sauvegarderCreatures(creaturesConnues)
    
run(setup, draw, finish = finish)

# TODO 1 : définir un "score total de capture" pour savoir qui est le meilleur à la capture de créatures !
# TODO 2 : ajout de stats pour le joueur
# TODO 3 : ajout des options
# TODO 4 : rendre le jeu beau <3