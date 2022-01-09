import pygame
from pygame.locals import *

from random import randint as RINT

from UTILITY.CONSTANTS import *
from UTILITY.CLASSES import *
import UTILITY.INFO as INFO

def aide():
    with open("README.txt", 'r') as f:
        print(f.read())
    
def canvas(x, y, font = 40):
    "Permet de créer un ecran, ainsi que les attributs  'w', 'h', 'width' et 'height', pour récupérer la taille de cet écran dans le corps du programme."
    # global SCREEN, w, h, width, height, clock, FONT, CENTER, LEFT, RIGHT, TOP, BOTTOM, TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT
    pygame.init()
    INFO.SCREEN = pygame.display.set_mode((int(x), int(y)), DOUBLEBUF, RESIZABLE)
    INFO.width, INFO.height = INFO.w, INFO.h = INFO.SCREEN.get_size()
    INFO.clock = pygame.time.Clock()
    INFO.FONT = pygame.font.Font(None, font)
    INFO.CENTER = (INFO.width/2, INFO.height/2)
    INFO.LEFT = (0, INFO.height/2)
    INFO.RIGHT = (INFO.width, INFO.height/2)
    INFO.TOP = (INFO.width/2, 0)
    INFO.BOTTOM = (INFO.width/2, INFO.height)
    INFO.TOP_LEFT = (0, 0)
    INFO.TOP_RIGHT = (INFO.width, 0)
    INFO.BOTTOM_LEFT = (0, INFO.height)
    INFO.BOTTOM_RIGHT = (INFO.width, INFO.height)
    frame(60)
    
def frame(newFps):
    "Modifie la cadence de raffraichissement maximale de l'écran."
    INFO.FPS = newFps
    
def load(name, resize = None):
    "Charge une image située à l'adresse mémoire indiquée, si l'image est dans le même dossier que le programme, seul le nom de cette dernière suffit. Il est possible d'ajouter des paramètres :\n\tUn argument <=> redimensionnement en pourcentage, hauteur et largeur.\n\tDeux arguments <=> redimensionnement en pixels.\n\tDans le cas contraire, il ne se passe rien sur l'image à part le chargement."
    image = pygame.image.load(name).convert()
    image.set_colorkey(COLORKEY)
    if str(type(resize)) == "<class 'tuple'>" or str(type(resize)) == "<class 'list'>":
         image = pygame.transform.scale(image, (int(resize[0]), int(resize[1])))
    elif resize is not None:
        largeur, hauteur = image.get_size()
        image = pygame.transform.scale(image, (largeur*resize//100, hauteur*resize//100))
    return image
    
def ticks():
    "Renvoie le nombre de millisecondes écoulées depuis le début de l'exécution du programme."
    return pygame.time.get_ticks()

def seconds():
    "Renvoie le nombre de secondes écoulées depuis le début de l'exécution du programme."
    return pygame.time.get_ticks()/1000
    
def wait(t):
    "Stoppe le programme pendant la durée 't', en millisecondes."
    pygame.time.delay(t)
    
def stop():
    """ Permet de forcer l'arrêt du programme. """
    INFO.CONTINUER = False
    
def noLoop():
    """ Arrête la boucle graphique du programme. Marche aussi avec la touche F11. """
    INFO.LOOP = False
    
def loop():
    """ Relance la boucle graphique du programme. Marche aussi avec la touche F11. """
    INFO.LOOP = True
    
    
###### fonctions de 'dessin'
def background(back):
    "Affiche un fond de la couleur indiquée, ou bien une image que la fonction remets à la taille de l'écran. \n\tL'argument unique peut être un triplet de la forme (r, g, b), par exemple GREEN ou (0, 255, 0), ou bien un nombre seul, la couleur sera alors une nuance de gris. Vous pouvez également passer une image en paramètre, un fond noir sera placé derrière pour éviter les problème possible avec la transparence."
    t = str(type(back))
    if t == "<class 'pygame.Surface'>":
        background(0)
        show(pygame.transform.scale(back, (INFO.w, INFO.h)), INFO.TOP_LEFT)
    elif t == "<class 'tuple'>" or t == "<class 'list'>":
        pygame.draw.rect(INFO.SCREEN, back, (0, 0, INFO.w, INFO.h))
    else:
        pygame.draw.rect(INFO.SCREEN, (back, back, back), (0, 0, INFO.w, INFO.h))
        
def showFPS(color):
    "Affiche les FPS sur l'écran, dans le coin en bas à droite."
    INFO.SCREEN.blit(INFO.FONT.render(str(round(INFO.clock.get_fps(), 1)), 0, color), (INFO.w - 60, INFO.h - 35))
    
def write(string, color, pos):
    "Ecris sur l'écran le message en paramètre, à la couleur et à l'endroit demandés."
    INFO.SCREEN.blit(INFO.FONT.render(str(string), 0, color), pos)

def paint(s, color, bold = False):
    "Change la couleur d'une chaîne de caractère dans l'interpréteur."
    if bold:
        return '\033[1m\033[%dm%s\033[0m' % (color, s)
    else:
        return '\033[%dm%s\033[0m' % (color, s)
    
def show(image, position):
    "Affiche une image à la position indiquée. L'argument 'position' est une liste ou un couple de nombre."
    INFO.SCREEN.blit(image, position)
        
def dot(position):
    "Affiche un point aux coordonnées (x, y). L'argument 'position' est une liste ou un couple de nombre."
    if INFO.STROKE_WEIGHT != -1:
        pygame.draw.circle(INFO.SCREEN, INFO.STROKE, (int(position[0]), int(position[1])), INFO.STROKE_WEIGHT)
    
def stroke(color):
    "Permet de modifier la couleur des points et des contours des formes géométriques. \n\tL'argument peut être un triplet de la forme (r, g, b), par exemple GREEN ou (0, 255, 0), ou bien un nombre seul, la couleur sera alors une nuance de gris."
    if str(type(color)) == "<class 'tuple'>" or str(type(color)) == "<class 'list'>":
        INFO.STROKE = (int(color[0]), int(color[1]), int(color[2]))
    else:
        INFO.STROKE = (int(color), int(color), int(color))
    #     print("Mauvais format d'argument pour la fonction 'stroke'. Un paramètre pour une nuance de gris, trois paramètres pour une couleur du type (rouge, vert, bleu).")
    
def noStroke():
    "Désactive l'affichage des points et des contours des formes géométriques."
    INFO.STROKE_WEIGHT = -1
    
def strokeWeight(size):
    "Permet de modifier la taille des points et des contours des formes géométriques (en pixels)."
    INFO.STROKE_WEIGHT = size
        
def fill(color):
    "Permet de modifier la couleur de l'intérieur des formes géométriques.\n\tL'argument peut être un triplet de la forme (r, g, b), par exemple GREEN ou (0, 255, 0), ou bien un nombre seul, la couleur sera alors une nuance de gris."
    INFO.FILL = 0
    if str(type(color)) == "<class 'tuple'>" or str(type(color)) == "<class 'list'>":
        INFO.COLOR = (int(color[0]), int(color[1]), int(color[2]))
    else:
        INFO.COLOR = (int(color), int(color), int(color))
        # print("Mauvais format d'argument pour la fonction 'stroke'. Un paramètre pour une nuance de gris, trois paramètres pour une couleur du type (rouge, vert, bleu).")
        
def noFill():
    "Désactive l'affichage de l'intérieur des formes géométriques."
    INFO.FILL = -1
    
def randomColor():
    "Renvoie une couleur aléatoire, sous la forme d'un triplet (r, g, b)."
    return (RINT(0, 255), RINT(0, 255), RINT(0, 255))
    
def luminosity(color, lum):
    """ Renvoie une couleur dont toutes les composantes ont été multipliées par 'lum' dans [0, +inf[. """
    return normalize((int(color[0]*lum), int(color[1]*lum), int(color[2]*lum)))
    
def normalize(color):
    """ Fait en sorte que le format de couleur soit le bon. """
    col = [0, 0, 0]
    if color[0] < 0:     col[0] = 0
    elif color[0] > 255: col[0] = 255
    if color[1] < 0:     col[1] = 0
    elif color[1] > 255: col[1] = 255
    if color[2] < 0:     col[2] = 0
    elif color[2] > 255: col[2] = 255
    return (col[0], col[1], col[2])
    
def ellipse(position, w, h):
    "Dessine une ellipse selon les paramètres : \n\tL'ellipse est horizontale, inscrite dans un rectangle de largeur 'w' et de hauteur 'h', dont le coin droit est aux coordonnées 'position'. L'argument 'position' est donc une liste ou un couple de nombre."
    if INFO.FILL != -1:
        pygame.draw.ellipse(INFO.SCREEN, INFO.COLOR, (int(position[0]), int(position[1]), int(w), int(h)), INFO.FILL)
    if INFO.STROKE_WEIGHT > 0:
        pygame.draw.ellipse(INFO.SCREEN, INFO.STROKE, (int(position[0]), int(position[1]), int(w), int(h)), INFO.STROKE_WEIGHT)  

def circle(position, r):
    "Dessine un cercle centré sur les coordonnées 'position' et de rayon r (en pixels). L'argument 'position' est donc une liste ou un couple de nombre."
    if INFO.FILL != -1:
        pygame.draw.circle(INFO.SCREEN, INFO.COLOR, (int(position[0]), int(position[1])), int(r), INFO.FILL)
    if INFO.STROKE_WEIGHT > 0:
        pygame.draw.circle(INFO.SCREEN, INFO.STROKE, (int(position[0]), int(position[1])), int(r), INFO.STROKE_WEIGHT)
    
def rectangle(position, w, h):
    "Dessine un rectangle de largeur 'w' et de hauteur 'h', dont le coin droit est aux coordonnées 'position'. L'argument 'position' est donc une liste ou un couple de nombre."
    if INFO.FILL != -1:
        pygame.draw.rect(INFO.SCREEN, INFO.COLOR, (int(position[0]), int(position[1]), int(w), int(h)), INFO.FILL) 
    if INFO.STROKE_WEIGHT > 0:
        pygame.draw.rect(INFO.SCREEN, INFO.STROKE, (int(position[0]), int(position[1]), int(w), int(h)), INFO.STROKE_WEIGHT)

def line(p1, p2):
    if INFO.STROKE_WEIGHT > 0:
        pygame.draw.line(INFO.SCREEN, INFO.STROKE, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), INFO.STROKE_WEIGHT)
        
def beginShape():
    "Crée une forme vierge."
    global SHAPE
    SHAPE = []

def addToShape(position):
    "Permet d'ajouter des points à la forme, ce sont en réalité des sommets aux coordonnées position. L'argument 'position' est donc une liste ou un couple de nombre."
    global SHAPE
    try:
        SHAPE.append((int(position[0]), int(position[1])))
    except NameError:
        pygame.quit()
        e = "Aucune forme n'a été crée et vous tentez de lui ajouter des sommets... Appelez beginShape()."
        raise Warning(e)
    
def endShape(closed = True):
    "Dessine la forme qui à été créée au préalable bien-sûr. Si close est 'True' alors le contour de la forme est fermé. Sinon il est ouvert entre le premier sommet et le dernier sommet."
    try:
        if len(SHAPE) < 3:
            e = "Une forme doit impérativement contenir plus de trois points."
            raise Warning(e)
        if INFO.FILL != -1:
            pygame.draw.polygon(INFO.SCREEN, INFO.COLOR, SHAPE, INFO.FILL) 
        if INFO.STROKE_WEIGHT > 0:
            pygame.draw.lines(INFO.SCREEN, INFO.STROKE, closed, SHAPE, INFO.STROKE_WEIGHT)
    except NameError:
        pygame.quit()
        e = "Aucune forme n'a été crée et vous tentez de la dessiner... Appelez beginShape()."
        raise Warning(e)
    
def loadPixel():
    "Crée une surface modifiable dont la taille est cellende l'écran. La courleur par défaut est commandée par la fonction 'fill()'.\n\tATTENTION, GROSSE PERTE DE PERFORMANCES SI VOUS UTILISEZ CETTE FONCTION ET MODIFIEZ TOUS LES PIXELS DE L'ECRAN."
    global PIXEL
    PIXEL = pygame.surface.Surface((INFO.w, INFO.h))
    PIXEL.fill(INFO.COLOR)
    
def showPixel():
    "Affiche la surface qui à été créée avec loadPixel()."
    try:
        show(PIXEL, (0, 0))
    except NameError:
        pygame.quit()
        e = "Vous n'avez pas appeler la fonction 'loadPixel()' avant d'afficher tous les pixels..."
        raise Warning(e)

def pixel(position, color):
    "Modifie le pixel aux coordonnées 'position' et lui assigne la couleur en paramètre. L'argument 'position' est donc une liste ou un couple de nombre."
    try:
        PIXEL.fill(color, (int(position[0]), int(position[1]), 1, 1))
    except NameError:
        pygame.quit()
        e = "Vous n'avez pas appeler la fonction 'loadPixel()' avant de modifier les pixels..."
        raise Warning(e)
######


###### fonctions 'utilitaires'
def error(setup, draw):
    "vérifie si les méthodes 'setup' et 'draw' ont bien été crées"

    try:
        type(setup)
    except Exception:
        pygame.quit()
        e = "\n\tLa méthode 'setup' n'a pas été créée, cela pourrait poser des problèmes quant au fontionnement du programme. L'exécution du programme a donc été bloquée."
        raise Warning(e)
        
    try:
        type(draw)
    except Exception:
        pygame.quit()
        e = "\n\tLe système a arrêté l'exécution du programme car la méthode 'draw' n'a pas été créée. Cela rend la poursuite de l'exécution impossible"
        raise Warning(e)

def downloadMethods(clic, keydown, finish, debug):
    "fonction qui s'occupe de charger les fontions optionnelles du programme:\n\tclic() : appel lorsque l'utilisateur clique sur n'importe quel bouton de la souris.\n\tkeydown() : appel lorsque l'utilisateur appuie sur n'importe quelle touche du clavier"
    
    def temp():
        pass
    fcts = []
    
    if clic: fcts.append(clic)
    else:    fcts.append(temp)
    
    if keydown: fcts.append(keydown)
    else:       fcts.append(temp)
    
    if finish: fcts.append(finish)
    else:      fcts.append(temp)
    
    if debug: fcts.append(debug)
    else:      fcts.append(temp)
            
    return fcts
######


######
######
### code principal, à vos risques et périls

def run(setup, draw, clic = None, keydown = None, finish = None, debug = None):
    
    print()
    print("******************************************************************")
    print("Vous utilisez la version 'TIPE' de l'outil UTILITY. Bon courage...")
    print("******************************************************************")
    print()

    error(setup, draw)
        
    ### SETUP()
    setup()
    clic, keydown, finish, debug = downloadMethods(clic, keydown, finish, debug)
    ###
    
    if INFO.CONTINUER:
        try:
            type(INFO.SCREEN)
            INFO.CONTINUER = True
        except:
            INFO.CONTINUER = False
        
        
    while INFO.CONTINUER:
        INFO.KEYS = []
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                INFO.CONTINUER = False
            if event.type == MOUSEBUTTONDOWN:
                INFO.CLIC_X, INFO.CLIC_Y = event.pos[0], event.pos[1]
                INFO.CLIC = Vect2D(INFO.CLIC_X, INFO.CLIC_Y)
                INFO.CLIC_BUTTON = event.button
                clic()
            if event.type == MOUSEMOTION:
                INFO.MOUSE_X, INFO.MOUSE_Y = event.pos
                INFO.MOUSE = Vect2D(INFO.MOUSE_X, INFO.MOUSE_Y)
            if event.type == KEYDOWN:
                INFO.KEYBOARD_NUM = event.key
                INFO.KEYBOARD_CHAR = event.unicode
                INFO.KEYS.append(INFO.KEYBOARD_NUM)
                if INFO.KEYBOARD_NUM == K_F12: INFO.DEBUG = not INFO.DEBUG
                if INFO.KEYBOARD_NUM == K_F11: INFO.LOOP = not INFO.LOOP
                keydown()
            if event.type == KEYUP:
                INFO.KEYBOARD_NUM = None
                INFO.KEYBOARD_CHAR = None
        INFO.clock.tick(INFO.FPS)
        
        ### DRAW()
        if INFO.LOOP: draw()
        ###
        
        if INFO.DEBUG: debug()
        
        pygame.display.flip()
    
    finish()
    pygame.quit()

######
######