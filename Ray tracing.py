# Projet MEGA
# Projet de Ray Tracing developpe par Emett
# Fonctionne avec les bibliotheques OpenCv (pour la video), Numpy, PIL (pour generer les images), math, random, sys, pickle (pour generer les fichier 3d), et time
from Bibliotheque_fonctions_3d_et_2d import *
from Bibliotheque_fonctions_graphiques import *

def speculaire(u,n,l,lampe):
    if scalaire(l,n) > 0:
        r = ((u-2)*scalaire(n,u) * n).unitaire()
        speculaire = lampe.col * scalaire(l,r)**lampe.alpha
    else:
        speculaire = Vecteur(0,0,0)
    return speculaire
def coloration (rayon,world,couleur,camera):
    # Avec reflet
    # Donne la couleur d'un pixel
    objet_rebond,n_objet_rebond = camera, camera
    indice_rebond = 0.001
    for nb_rebond in range(camera.rebond):
        distance_min = inf
        for objet  in world.obj:
            if objet != objet_rebond:
                d_M =  objet.intersection_droite(rayon)
                if 0< d_M <distance_min:
                    distance_min = d_M
                    M =  (rayon.vect*d_M) + rayon.ori
                    if objet.type == "Sphere":
                        reflected_ray =  rayon.reflexion((M - objet.pos).unitaire())
                    if objet.type == "Triangle":
                        reflected_ray =  rayon.reflexion(objet.norm)
                    n_objet_rebond = objet
                    
        objet_rebond = n_objet_rebond
        
        if objet_rebond != camera:
            indice_rebond += 1-objet_rebond.reflexion
            couleur  += objet_rebond.col*(1-objet_rebond.reflexion)
        if nb_rebond+1 == camera.rebond or objet_rebond == camera:
            if nb_rebond == 0:
                return None
            spec = Vecteur(0,0,0)
            for lampe in world.lamp:
                l = (lampe.pos - objet.pos).unitaire()
                n = (rayon.vect - objet.pos).unitaire()
                spec += speculaire(rayon.vect,n,l,lampe)
                couleur *= max(scalaire(n,l),0)
            return ( couleur * len(world.lamp) * max(scalaire(n,l),0)/(indice_rebond) + spec).rgb()
        rayon.vect = reflected_ray.unitaire()
        rayon.ori = M
        
def coloration2 (rayon,world,couleur,camera):
    # Sans refexion
    # Donne la couleur d'un pixel
    distance_min = inf
    couleur = None
    for objet in world.obj:
        d_M =  objet.intersection_droite(rayon)
        if 0< d_M <distance_min :
            distance_min = d_M
            OM =  rayon.vect*d_M + rayon.ori
            lampe = world.lamp[0]
            l = (lampe.pos - OM).unitaire()
            if objet.type == "Sphere":
                n = (OM - objet.pos).unitaire()
            elif objet.type == "Triangle":
                n = objet.norm.unitaire()
            spec = speculaire(rayon.vect,n,l,lampe)
            couleur = (objet.col * max(scalaire(n,l),0) + spec).rgb()
    return couleur

def Ray_tracing(world, image, camera):
    # Genere le rendu
    rendu = zeros((image.l,image.h,3), dtype=uint8)
    rendu.fill(image.fond)
    m_l, m_h = image.l/2, image.h/2
    for x in range(image.l):
        for y in range(image.h):
            u = (Vecteur(x - m_l,y - m_h, camera.D)).unitaire()
            rayon = Rayon(camera.pos, u)
            rayon.vect = (rayon.rotation(camera.rot)).unitaire()
            couleur = coloration(rayon,world,Vecteur(0,0,0),camera)
            if couleur != None:
                rendu[x,y] = couleur
                
    stdout.write("Generation rendu: %d s\n" %(time()-debut))
    enregistrer_image(image.nom,rendu)
    #afficher_image(rendu)
    stdout.write("Enregistrement rendu: %d s\n" %(time()-debut))
    
def generateur_world(n,nombre_lampes,nombre_triangles,nombre_spheres):
    # permet de generer une scène avec des lampes, des triangles et des sphères
    objets = []
    lampes = []
    for _ in range(nombre_spheres):
        objets.append(Sphere(Vecteur(randint(0,255),randint(0,255),randint(0,255)),Vecteur(randint(-6,6),randint(-6,6),randint(-6,6)),randint(1,3),random()))
    for _ in range(nombre_triangles):
        triangle = Triangle(Vecteur(randint(0,255),randint(0,255),randint(0,255)) ,Vecteur(randint(-6,6),randint(-6,6),randint(-6,6)), Vecteur(randint(-6,6),randint(-6,6),randint(-6,6)), Vecteur(randint(-6,6),randint(-6,6),randint(-6,6)),random())
        objets.append(triangle)
    for _ in range(nombre_lampes):
        lampes.append(Lampe( Vecteur(randint(0,255),randint(0,255),randint(0,255)), Vecteur(randint(-6,0),randint(-6,0),randint(-6,0)), 100))
    
    world = World(objets,lampes)
    ecrire_fichier("world n°%d" %n, world)
    return 1

def main():
    # Prend environ 100s
    global debut
    debut = time()
    n_w = 10
    n = 1
    
    #generateur_world(n_w,2,5,10)
    world = lire_fichier("world n°%d" %n_w)
    image = Image_(500,500,50,"Rendu %d" %n)
    camera = Camera(Vecteur(0,0,-10),Vecteur(n/20,0,0),400,3)
    
    stdout.write("Generation scene: %d s\n" %(time()-debut))
    Ray_tracing(world, image, camera)
    
    """
    liste_images = []
    for n in range(1,4):
        liste_images.append("Rendu %d.png" %n)
        image = Image_(500,500,Vecteur(100,100,100),"Rendus video\Rendu %d" %n)
        world = lire_fichier("world n°%d" %n_w)
        camera = Camera(Vecteur(0,0,-10),Vecteur(n/20,0,0),400,4)
        print(time()-debut)
        Ray_tracing(world, image, camera)
    creation_video ("Video", liste_images,20)
    """
main()



                  
