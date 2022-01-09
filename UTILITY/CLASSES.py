from UTILITY.CONSTANTS import COLORKEY

import pygame

from random import random as RDOM
from math import cos as COS, sin as SIN, acos as ACOS

def map(x, a, b, c, d):
    """ Envoie 'x' de ['a', 'b'] dans ['c', 'd']. Ceci est une application linéaire. On doit avoir 'a' différent de 'b'. """
    return (d - c) / (b - a) * (x - a) + c
    
def copy(tab : list, d = 1) -> list:
    if d == 1:
        return [tabi for tabi in tab]
    elif d == 2:
        return [[tabii for tabii in tabi] for tabi in tab]
    else:
        raise Warning("oups, mauvais format pour copier une liste...")

class Vect2D:
    "Vecteur réel dans le R-espace vectoriel R2, muni du produit scalaire usuel. Soient u = (x, y) et v = (a, b) avec x, y, a, b des réels, et µ un réel non nul. Les opérations suivantes sont permises:\n\tu + v = (x + a, y + b)\n\tu += v\n\tu - v = (x - a, y - b)\n\tu -= v\n\t-u = (-x, -y)\n\tu * µ = (µx, µy)\n\tµ * u = (µx, µy)\n\tu *= µ\n\tu / µ = (x/µ, y/µ)\n\tµ / u = (x/µ, y/µ)\n\tu /= µ\n\tu//v renvoie (x, y, a, b)\n\tabs(u) = ||u||\n\tu|v = (u|v)\n\tu.lst() renvoie u sous forme de liste\n\tu.integer() = (int(x), int(y)))"
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        
    def __add__(self, other):
        return Vect2D(self.x + other.x, self.y + other.y)
        
    def __iadd__(self, other):
        return Vect2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vect2D(self.x - other.x, self.y - other.y)
        
    def __isub__(self, other):
        return Vect2D(self.x - other.x, self.y - other.y)
        
    def __neg__(self):
        return Vect2D(-self.x, -self.y)
        
    def __mul__(self, l):
        return Vect2D(l * self.x, l * self.y)
        
    def __rmul__(self, l):
        return Vect2D(l * self.x, l * self.y)
        
    def __imul__(self, l):
        return Vect2D(l * self.x, l * self.y)
        
    def __truediv__(self, l):
        return Vect2D(self.x / l, self.y / l)
        
    def __itruediv__(self, l):
        return Vect2D(self.x / l, self.y / l)
        
    def __itruediv__(self, l):
        return Vect2D(self.x / l, self.y / l)
        
    def __floordiv__(self, other):
        return (self.x, self.y, other.x, other.y)
        
    def __abs__(self):
        return (self|self)**0.5
        
    def __or__(self, other):
        return self.x * other.x + self.y * other.y
        
    def __ror__(self, other):
        return self.x * other.x + self.y * other.y
        
    def __invert__(self):
        return self|self
        
    def __repr__(self):
            return "({}, {})".format(self.x, self.y)
            
            
    def lst(self):
        "Renvoie le vecteur sous forme de liste, pour pouvoir l'utiliser sans devoir décomposer manuellement les coordonées de ce dernier dans une liste."
        return (self.x, self.y)
        
    def integer(self):
        "Renvoie le vecteur avec des coordonnées entières, arrondi inférieur."
        return Vect2D(int(self.x), int(self.y))
        
    def rotate(self, theta):
        "Permet de faire tourner le vecteur d'un angle theta"
        self.x, self.y = self.x*COS(theta) - self.y*SIN(theta), self.x*SIN(theta) + self.y*COS(theta)
        
    def angle(self):
        "Calcule l'angle theta que fait le vecteur avec l'axe des abscisses."
        theta = ACOS(self.x/abs(self))
        if self.y != 0:
            theta *= self.y/abs(self.y)
        return theta
        
    def copy(self):
        "Permet de copier une instance de la classe Vect2D, sans les problèmes de référence."
        return Vect2D(self.x, self.y)
        
def Vect2D_rand(a = 0, b = 1):
    """ Donne un vecteur de |R^2 dont les composantes sont dans ['a', 'b']."""
    return Vect2D(map(RDOM(), 0, 1, a, b), map(RDOM(), 0, 1, a, b))

def Vect2D_fromAngle(angle):
    """ Donne un vecteur unitaire de |R^2 d'argument 'angle'."""
    return Vect2D(COS(angle), SIN(angle))       
    
    
class Image:
    
    def __init__(self, image):
        ## tous les paramètres initiaux de l'image 
        self.name = image
        self.load(self.name)
        self.rootW, self.rootH = self.image.get_size()
        
        ## image qui est affichée 
        self.rImage = self.image
        self.w, self.h = self.rootW, self.rootH
        
        ## initialement, pas de rotation et pas de zoom
        self.angle = 0
        self.zoom = 1
        
        ## représente le "décalage" qu'il faut prendre en compte pour afficher l'image par rapport à son centre
        self.blitting = Vect2D() #Vect2D(self.w//2, self.h//2)
        
    def load(self, image):
        "Chargement d'un sprite pour le point matériel. La transparence est gérée, la hitbox est également créée."
        self.image = pygame.image.load("images/" + image).convert()
        self.image.set_colorkey(COLORKEY)
        
    def get_rootSize(self):
        "Donne la taille de l'image initiale."
        return (self.rootW, self.rootH)
        
    def get_size(self):
        "Donne la taille de l'image."
        return (self.w, self.h)
        
    def copy(self):
        "Permet de copier une instance de la classe Image, sans les problèmes de référence."
        return Image(self.name)
    
    def horizontalFlip(self):
        "Renverse l'image horizontalement. Agit directement sur l'image initiale."
        self.image = pygame.transform.flip(self.image, True, False)
        self.rootW, self.rootH = self.image.get_size()
        
    def verticalFlip(self):
        "Renverse l'image verticalement. Agit directement sur l'image initiale."
        self.image = pygame.transform.flip(self.image, False, True)
        self.rootW, self.rootH = self.image.get_size()
        
    def flip(self, horizontal, vertical):
        "Renverse l'image, horizontalement, verticalement, ou les deux à la fois. Agit directement sur l'image initiale."
        self.image = pygame.transform.flip(self.image, horizontal, vertical)
        self.rootW, self.rootH = self.image.get_size()
        
    def rotate(self, delta):
        "Fait pivoter l'image d'un angle delta, en radian et dans le sens trigonométrique."
        self.angle += delta
        self.build()
    
    def forceRotate(self, angle):
        "Force l'image à adopter un certain angle."
        self.angle = angle
        self.build()
        
    def scale(self, facteur):
        "Effectue une remise à l'échelle 'facteur' de l'image. 'facteur' est une proportion de la taille de l'image. 1 coorespond à aucun zoom par exmeple. Si 'facteur' est nul, une valeur proche de zéro est affectée par défaut pour éviter de rester bloqué avec une image de taille 0x0."
        self.zoom *= facteur
        if self.zoom == 0:
            self.zoom = 0.00000001
        self.build()
            
    def visible(self):
        "Indique si l'image est visible. L'image n'est pas visible ssi une de ses deux dimensions est nulle."
        return (int(self.rootW*self.zoom) > 0 and int(self.rootH*self.zoom) > 0)
            
    def resetAngle(self):
        "Remets l'image à son inclinaison initiale."
        self.angle = 0
        self.build()
        
    def resetZoom(self):
        "Remets l'image à sa taille initiale."
        self.zoom = 1
        self.build()
    
    def reset(self):
        "Remets l'image dans l'état exact où elle a été chargée."
        self.resetAngle()
        self.resetZoom()
        
    def shuffle(self):
        "'Mélange' l'image, aléatoirement. C'est-à-dire qu'elle est retournée, dans n'importe quel sens.Agit directement sur l'image initiale."
        self.flip(randint(0, 1), randint(0, 1))
        self.build()
        
    def build(self):
        ## calcul de la nouvelle taille (de l'image d'origine), en fonction du niveau de zoom
        self.w = int(self.rootW * self.zoom)
        self.h = int(self.rootH * self.zoom)
        
        ## calcul de la taille de l'image, après rotation (taille apparente de l'image)
        W = abs(self.w * cos(self.angle)) + abs(self.h * sin(self.angle))
        H = abs(self.h * cos(self.angle)) + abs(self.w * sin(self.angle))
        
        self.blitting = Vect2D(W/2, H/2)
        
        ## transformation de l'image
        self.rImage = pygame.transform.scale(self.image, (self.w, self.h))
        self.rImage = pygame.transform.rotate(self.rImage, self.angle*180/pi)
        
    def blit(self, screen, pos):
        "Affichage de l'image. La position donnée en paramètre correspond au centre de l'image."
        ## affichage de l'image
        screen.blit(self.rImage, (pos[0] - self.blitting.x, pos[1] - self.blitting.y))
