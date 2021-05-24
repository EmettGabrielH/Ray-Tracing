from PIL import Image
from numpy import dot,linalg, zeros, uint8, log, array
from pickle import *

from cv2 import imread,VideoWriter_fourcc,VideoWriter
"""
Traitement Fichiers
"""
def ecrire_fichier(nom_fichier, data):
    with open("Objet 3d\{}".format(nom_fichier), 'wb') as fichier:
        mon_pickler = Pickler(fichier)
        mon_pickler.dump(data)
def lire_fichier(nom_fichier):
    with open("Objet 3d\{}".format(nom_fichier), 'rb') as fichier:
        mon_depickler = Unpickler(fichier)
        data = mon_depickler.load()
    return data

"""
Traitement Images
"""
def lire_image (nom_image):
    img = image.imread("{}.png".format(nom_image))
    if img.dtype == float32:
        img = (img * 255).astype(uint8)
    return img

def enregistrer_image(nom_image,data):
    im = Image.fromarray(data)
    im.save("{}.png".format(nom_image))
def afficher_image(data):
    rendu = Image.fromarray(data, 'RGB')
    rendu.show()

"""
Vidéo
"""

def creation_video (nom_fichier, liste_images,fps):
    path_img = "Rendus video/"
    frame=imread(path_img+liste_images[0])
    print(path_img+liste_images[0])
    h,l,c=frame.shape
    fourcc = VideoWriter_fourcc(*'XVID')
    out = VideoWriter('{}.mp4'.format(nom_fichier),fourcc, fps, (l,h))
    for i in range(len(liste_images)):
        frame=imread(path_img+liste_images[i])
        out.write(frame)
    out.release()
