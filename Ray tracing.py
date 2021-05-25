# Projet MEGA
# Projet de Ray Tracing developpe par Emett
# Fonctionne avec les bibliotheques OpenCv (pour la video), Numpy, PIL (pour generer les images), math, random, sys, pickle (pour generer les fichier 3d), et time
from Bibliotheque_fonctions_3d_et_2d import *
from Bibliotheque_fonctions_graphiques import *

def speculaire(u,n,l,lampe):
    if scalaire(l,n) > 0:
        return lampe.col * scalaire(l,((u-2)*scalaire(n,u) * n).unitaire())**lampe.alpha
    return Vecteur(0,0,0)
def coloration (rayon,world,camera):
    # Avec reflet
    # Donne la couleur d'un pixel
    objet_rebond, n_objet_rebond =  camera, camera
    couleur = Vecteur(0,0,0)
    indice_reflexion = 1
    for nb_rebond in range(camera.rebond):
        distance_min = inf
        for objet  in world.obj:
            if objet != objet_rebond:
                d_M =  objet.intersection_droite(rayon)
                if 0< d_M <distance_min:
                    distance_min = d_M
                    M =  (rayon.vect*d_M) + rayon.ori
                    
                    if type(objet) == Sphere:
                        reflected_ray =  rayon.reflexion((M - objet.pos).unitaire())
                    else:
                        reflected_ray =  rayon.reflexion(objet.norm)
                        
                    n_objet_rebond = objet
                    
        objet_rebond = n_objet_rebond
        
        if objet_rebond != camera:
            indice_objet = indice_reflexion*(1-objet_rebond.reflexion)
            
            if type(objet_rebond) == Sphere:
                n = (M - objet_rebond.pos).unitaire()
            else:
                n =  objet_rebond.norm
            
            scal,spec = 0, Vecteur(0,0,0)
            for lampe in world.lamp:
                l = (lampe.pos - M).unitaire()
                spec += speculaire(rayon.vect,n,l,lampe)
                scal = max(scalaire(n,l),scal)
                
            couleur_objet =objet_rebond.col*scal + spec
            couleur  += couleur_objet*indice_objet
            indice_reflexion *= objet_rebond.reflexion
            
        if nb_rebond+1 == camera.rebond or objet_rebond == camera:
            if objet_rebond == camera:
                return None
            return couleur.rgb()
        
        rayon.vect = reflected_ray.unitaire()
        rayon.ori = M
        
def coloration2 (rayon,world,camera):
    # Sans refexion, une seul lampe
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
            if type(objet) == Sphere:
                n = (OM - objet.pos).unitaire()
            else:
                n = objet.norm
            spec = speculaire(rayon.vect,n,l,lampe)
            couleur = (objet.col * max(scalaire(n,l),0) + spec).rgb()
    return couleur

def Ray_tracing(world, image, camera):
    # Genere le rendu
    rendu = zeros((image.l,image.h,3), dtype=uint8)
    rendu.fill(camera.fond)
    m_l, m_h = image.l/2, image.h/2
    for x in range(image.l):
        for y in range(image.h):
            rayon = Rayon(camera.pos, (Vecteur(x - m_l,y - m_h, camera.D)).unitaire())
            rayon.vect = (rayon.rotation(camera.rot)).unitaire()
            couleur = coloration(rayon,world,camera)
            if couleur != None:
                rendu[x,y] = couleur
                
    stdout.write("Generation rendu: %d s\n" %(time()-debut))
    enregistrer_image(image.nom,rendu)
    #afficher_image(rendu)
    stdout.write("Enregistrement rendu: %d s\n" %(time()-debut))
    
def generateur_world(n,nombre_lampes,nombre_triangles,nombre_spheres, nombre_plans):
    # permet de generer une scène avec des lampes, des triangles et des sphères
    objets = []
    lampes = []
    for _ in range(nombre_spheres):
        objets.append(Sphere(Vecteur(randint(0,255),randint(0,255),randint(0,255)),Vecteur(randint(-10,10),randint(-10,10),randint(-10,10)),randint(1,5)*random(),random(),random()))
    for _ in range(nombre_triangles):
        triangle = Triangle(Vecteur(randint(0,255),randint(0,255),randint(0,255)) ,Vecteur(randint(-6,6),randint(-6,6),randint(-6,6)), Vecteur(randint(-6,6),randint(-6,6),randint(-6,6)), Vecteur(randint(-6,6),randint(-6,6),randint(-6,6)),random(),random())
        objets.append(triangle)
    for _ in range(nombre_lampes):
        lampes.append(Lampe( Vecteur(randint(220,255),randint(220,255),randint(220,255)), Vecteur(randint(-20,6),randint(-20,6),randint(-20,6)), randint(60,100)))
    for _ in range(nombre_plans):
        plan = Plan(Vecteur(randint(0,255),randint(0,255),randint(0,255)) ,Vecteur(randint(-6,6),randint(-6,6),randint(-6,6)), Vecteur(randint(-6,6),randint(-6,6),randint(-6,6)), Vecteur(randint(-6,6),randint(-6,6),randint(-6,6)),random(),random())
        objets.append(plan)
    world = World(objets,lampes)
    ecrire_fichier("world n°%d" %n, world)
    return 1

def main():
    # Prend environ 100s
    global debut
    debut = time()
    n_w = 13
    n = 1
    
    generateur_world(n_w,3,0,0,4)
    world = lire_fichier("world n°%d" %n_w)
    image = Image_(300,300,"Rendu %d" %n)
    camera = Camera(Vecteur(0,0,-10),Vecteur(0,0,0),50,400,3)
    
    stdout.write("Generation scene: %d s\n" %(time()-debut))
    Ray_tracing(world, image, camera)
    
    """
    liste_images = []
    for n in range(24,100):
        liste_images.append("Rendu %d.png" %n)
        image = Image_(300,300,"Rendus video\Rendu %d" %n)
        world = lire_fichier("world n°%d" %n_w)
        camera = Camera(Vecteur(0,n/40,-10),Vecteur(n/40,n/40,n/40),50,400,3)
        Ray_tracing(world, image, camera)
    creation_video ("Video 2", liste_images,15)
    #"""
main()
