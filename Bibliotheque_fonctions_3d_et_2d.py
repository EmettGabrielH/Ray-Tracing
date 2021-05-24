from numpy import dot,linalg, zeros, uint8, log, array
from math import cos, sin, tan, pi, floor, inf, sqrt, acos
from random import randint,random

from sys import stdout

from time import time

"""
Classes
"""
class Vecteur:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def rgb(self):
        return (min(self.x,255), min(self.y,255),min(self.z,255))
    def __add__(self, vecteur2):
        if type(vecteur2) == int or type(vecteur2) == float:
            return Vecteur(self.x + vecteur2, self.y + vecteur2, self.z + vecteur2)
        return Vecteur(self.x + vecteur2.x, self.y + vecteur2.y, self.z + vecteur2.z)
    def __iadd__(self, vecteur2):
        self = self + vecteur2
        return self
    def __truediv__(self, vecteur2):
        if type(vecteur2) == int or type(vecteur2) == float:
            return Vecteur(self.x / vecteur2, self.y / vecteur2, self.z / vecteur2)
        return Vecteur(self.x / vecteur2.x, self.y / vecteur2.y, self.z / vecteur2.z)
    def __mul__(self, vecteur2):
        if type(vecteur2) == int or type(vecteur2) == float:
            return Vecteur(self.x * vecteur2, self.y * vecteur2, self.z * vecteur2)
        return Vecteur(self.x * vecteur2.x, self.y * vecteur2.y, self.z * vecteur2.z)
    def __sub__ (self, vecteur2):
        if type(vecteur2) == int or type(vecteur2) == float:
            return Vecteur(self.x - vecteur2, self.y - vecteur2, self.z - vecteur2)
        return Vecteur(self.x - vecteur2.x, self.y - vecteur2.y, self.z - vecteur2.z)
    def norme(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)
    def unitaire(self):
        n = self.norme()
        if n!= 0:
            return Vecteur(self.x/n, self.y / n, self.z / n)
        return Vecteur(0, 0, 0)
    def negatif(self):
        return self * (-1)
class Sphere:
    def __init__(self,couleur, position, rayon,reflexion,transparence):
        self.pos = position
        self.r = rayon
        self.col = couleur
        self.reflexion = reflexion
        self.transparence = transparence
        self.type = "Sphere"
    def intersection_droite(self,rayon):
        # droite d , passant par A de vecteur directeur u, vecteur unitaire
        SA = rayon.ori - self.pos
        b = 2 * scalaire(rayon.vect,SA)
        c = (SA.x**2 + SA.y**2 + SA.z**2) - self.r**2
        delta = b**2 - 4*c
        if delta == 0:
            return -b/2
        elif delta > 0:
            sqrt_delta = sqrt(delta)
            x = min((-b - sqrt_delta) /2,  (-b + sqrt_delta) /2 )
            return x
        else:
            return -1
class Plan:
    def __init__(self,couleur, position1, position2, position3,reflexion,transparence):
        self.pos1 = position1
        self.pos2 = position2
        self.pos3 = position3
        self.pos = position1
        self.col = couleur
        self.reflexion = reflexion
        self.transparence = transparence
        self.norm = self.normal()
        self.equa = self.equation()
        self.type = "Plan"
    def normal(self):
        return vectoriel(self.pos1-self.pos2,self.pos3-self.pos2).unitaire()
    def equation(self):
        norm = self.normal()
        d = -scalaire(norm,self.pos1)
        return (norm.x,norm.y,norm.z,d)
    def intersection_droite(self,rayon):
        a,b,c,d = self.equa
        A = a*rayon.vect.x + b* rayon.vect.y + c*rayon.vect.z
        if A != 0:
            return -(a*rayon.ori.x +b*rayon.ori.y+ c*rayon.ori.z +d)/ A
        return -1
class Triangle:
    def __init__(self,couleur, position1, position2, position3,reflexion,transparence):
        self.pos1 = position1
        self.pos2 = position2
        self.pos3 = position3
        self.pos = (position1 + position2 + position3)/3
        self.reflexion = reflexion
        self.transparence = transparence
        self.col = couleur
        self.type = "Triangle"
        self.norm = self.normal()
    def normal(self):
        return vectoriel(self.pos1-self.pos2,self.pos3-self.pos2).unitaire()
    def equation(self):
        norm = self.normal()
        d = -scalaire(norm,self.pos1)
        return (norm.x,norm.y,norm.z,d)
    def intersection_droite(self, rayon):
        scal = scalaire(rayon.vect,self.norm)
        if scal == 0:
            return -1
        else:
            d_triangle = -scalaire(self.norm,rayon.ori + (self.norm * scalaire(self.norm,self.pos1)).negatif()) / scal
            q = rayon.vect * d_triangle + rayon.ori

            A = scalaire(vectoriel(self.pos3 - self.pos1,q - self.pos1), self.norm)
            B = scalaire(vectoriel(self.pos2 - self.pos3,q - self.pos3), self.norm)
            C = scalaire(vectoriel(self.pos1 - self.pos2,q - self.pos2), self.norm)
            if A>=0 and B>=0 and C>=0:
                return d_triangle
            else:
                return -1
class Lampe:
    def __init__(self,couleur, position,alpha):
        self.pos = position
        self.col = couleur
        self.alpha = alpha # entre 10 et 100
        self.type = "Lampe"
        
class World:
    def __init__(self, liste_objets, liste_lampes):
        self.obj = liste_objets
        self.lamp = liste_lampes
class Camera:
    def __init__(self, position, rotation,fond, distance,rebonds):
        self.pos = position
        self.rot = rotation    # en radian
        self.fond = fond
        self.D = distance
        self.rebond = rebonds  # nombre de rebond du rendi
class Image_:
    def __init__(self,longueur, hauteur, nom_image):
        self.l = longueur
        self.h = hauteur
        self.nom = nom_image
        
class Rayon:
    def __init__(self,origine, vecteur):
        self.ori = origine
        self.vect = vecteur
    def rotation(self, rotations):
        # avec self.ori = (0,0,0)
        vecteur = (self.vect.x, self.vect.y, self.vect.z)
        for axe in range(2):
            vecteur =  rotation_(vecteur, axe, rotations)
        return Vecteur(float(vecteur[0]),float(vecteur[1]),float(vecteur[2]))
    def reflexion(self, axis):
        return (self.vect- (axis * 2 *scalaire(self.vect, axis)))
"""
Transformations
"""

def dilatation (point, Cx, Cy, Cz):
    # point = [x,y,z]
    return dot(point, ((Cx,0,0) , (0,Cy,0) , (0,0,Cz)))

def rotation_(point, axe, angles):
    # angle en radian

    if axe == 0:             #x
        angle = angles.x
        s = sin(angle)
        c = cos(angle)
        return dot(point, ((1,0,0) , (0,c,-s), (0,s,c) ))
    elif axe == 1:         #y
        angle = angles.y
        s = sin(angle)
        c = cos(angle)
        return dot(point, ((c,0,s) , (0,1,0) , (-s,0,c)))
    elif axe == 2:          #z
        angle = angles.z
        s = sin(angle)
        c = cos(angle)
        return dot(point, ((c,-s,0), (s,c,0) , (0,0,1) ))
    
def translation(point , Tx, Ty, Tz):
    # point = [x,y,z,1]
    return dot(point, ((1,0,0,0) , (0,1,0,0) , (0,0,1,0) , (Tx,Ty,Tz,1)))
"""
Fonctions
"""
def scalaire(u,v):
    return u.x *v.x + u.y * v.y + u.z * v.z
def vectoriel(u,v):
    return Vecteur( (u.y*v.z) - (v.y*u.z) , (u.z*v.x) - (v.z*u.x) , (u.x*v.y) - (v.x*u.y) )
def angle_vect(u, v):
    return (acos (scalaire(u,v) / (u.norme() * v.norme())) ) / (2*pi)
