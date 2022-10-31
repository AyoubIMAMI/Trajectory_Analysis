# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 18:35:05 2019

@author: IMAMI Ayoub
"""



import PIL.Image as im
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from math import *
from scipy.signal import savgol_filter


"""
Choix des vidéos (Attention: Majuscule, ï)
"""

nom_choisi = input("Pendule - Panier - Cycloïde - Golf - Nom: ")

"""
Principe de base (valable pour le pendule, le panier et le cycloïde):
    
        1. Avec un clic de l'utilisateur, on récupère les coordonnées de l'objet en mouvement
           sur la première image.
           
        2. Ensuite, on parcours une zone autour de ces coordonnées à la recherche de tous les pixels
           ayant une couleur particulière (couleur de l'objet).
           
        3. A partir de ces pixels, on déduit les coordonnées du centre de l'objet.
        
        4. Enfin on réitère l'opération 2. et 3. pour toutes les autres images à partir des
           coordonnées de l'image précédente.
           
        5. Finalement, on obtient les coordonnées de l'objet en mouvement sur chaque image.
"""

if nom_choisi == "Pendule": #Une condition sur la vidéo choisi par l'utilisateur
    
    photo = im.open("Pendule000.JPEG") #On ouvre la première image pour permettre un clic de l'utilisateur
    photopix = np.array(photo.convert()) #On convertit l'image en tableau pour travailler sur les couleurs de chaque pixel
    taille=photopix.size #Information sur la taille du tableau (nombre de pixels)
    
    
    premiere_coord = [] #Liste dans laquelle seront stockées les coordonnées du clic de l'utilisateur
    def onclick(event):
        global coord
        """
         Partie permettant l'évènement du clic et l'obtention de la première coordonnée 
        """
        
        ix, iy = event.xdata, event.ydata
        print ('x = %d, y = %d'%(ix, iy))
    
        global premiere_coord
        premiere_coord.append((int(ix), int(iy)))
    
        if len(premiere_coord) == 1:
            fig.canvas.mpl_disconnect(cid)
            
        """
         Partie permettant l'évènement du clic et l'obtention de la première coordonnée 
        """
            
        photo = im.open("Pendule000.JPEG") #On ouvre la première photo
        photopix = np.array(photo.convert()) #On la convertit en tableau
            
        coordx = int(premiere_coord[0][0]) #On initialise 2 varibales correspondants aux premières coordonnées
        coordy = int(premiere_coord[0][1])
        
        liste_onclickx = [] #On crée 2 listes qui permettront le parcours de la zone autour des premières coordonnées
        liste_onclicky = []
        
        """
         On remplie les 2 listes de façons à pouvoir parcourir un carrée de 100x100 pixels 
        """
    
        for k in range(-50,51):
            coordx+=k
            liste_onclickx.append(coordx)
            coordx = int(premiere_coord[0][0])
        
        for k in range(-50,51):
            coordy+=k
            liste_onclicky.append(coordy)
            coordy = int(premiere_coord[0][1])
            
        """
         On remplie les 2 listes de façons à pouvoir parcourir un carrée de 100x100 pixels 
        """
               
        pts_gris = [] #Liste dans laquelle on stockera tous les pixels ayant environ la couleur de l'objet
        coord = [] #Liste dans laquelle on stockera les coordonnées de chaque image
        
        """
         On parcour le carrée de 100x100 pixels et on garde uniquement les pixels dont 
         le code couleur RGB correspond environ à celui de l'objet                     
        """
        
        for j in liste_onclickx:
            for i in liste_onclicky:
                if (95 < photopix[i,j][0] <= 115) and (40 < photopix[i,j][1] <= 60) and (60 < photopix[i,j][2] <= 80):
                    pts_gris.append([i,j])
                    
        """
         On parcour le carrée de 100x100 pixels et on garde uniquement les pixels dont 
         le code couleur RGB correspond environ à celui de l'objet                     
        """
                    
        milieu = int(len(pts_gris)/2) #On associe à la variable milieu la postion (dans la liste pts_gris) du pixel correspondant au centre de l'objet
        coord.append(pts_gris[milieu]) #On stock les coordonées du centre de l'objet de la première image
        
        coordx = int(coord[0][1]) #On ré-initialise les 2 varibales aux valeurs des premières coordonnées
        coordy = int(coord[0][0])
        
        """
         On crée une boucle qui ouvrira toutes les images, et, qui parcourira (pour chaque image) 
         un carrée de 100x100 pixels à partir des coordonnées de l'objet de l'image précèdente    
         afin de déduire les coordonnées de l'objet sur chaque image                              
        """
        
        for n in range(1,100):
        
            nom = "Pendule"+str(n).zfill(3)+".JPEG" #On modifie le nom de chaque nouvelle image à ouvrir
            
            #A partir d'ici, même principe que précèdemment
            photo = im.open(nom)
            photopix = np.array(photo.convert())
            
            liste_onclickx = []
            liste_onclicky = []
    
            for k in range(-50,51):
                coordx+=k
                liste_onclickx.append(coordx)
                coordx = int(coord[len(coord)-1][1])
        
            for k in range(-50,51):
                coordy+=k
                liste_onclicky.append(coordy)
                coordy = int(coord[len(coord)-1][0])
                  
            pts_gris = []
            
            for j in liste_onclickx:
                for i in liste_onclicky:
                    if (95 < photopix[i,j][0] <= 115) and (40 < photopix[i,j][1] <= 60) and(60 < photopix[i,j][2] <= 80):
                        pts_gris.append([i,j])
            
                    
            milieu = int(len(pts_gris)/2)
            coord.append(pts_gris[milieu])
            
            coordx = int(coord[len(coord)-1][1]) #On ré-initialise les 2 varibales aux valeurs des coordonnées qu'on vient de trouvés, pour l'image suivante
            coordy = int(coord[len(coord)-1][0]) 
            
        print(coord)
        
        return coord
    
        """
         On crée une boucle qui ouvrira toutes les images, et, qui parcourira (pour chaque image) 
         un carrée de 100x100 pixels à partir des coordonnées de l'objet de l'image précèdente    
         afin de déduire les coordonnées de l'objet sur chaque image                              
        """
        
    """
     Partie permettant l'ouverture d'une image et la réalisation du clic 
    """
        
    fig = plt.figure()
    plt.imshow(photopix) 
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    
    """
     Partie permettant l'ouverture d'une image et la réalisation du clic 
    """
    
        
        
elif nom_choisi == "Panier":
    
    photo = im.open("Panier00.PNG")
    photopix = np.array(photo.convert())
    taille=photopix.size
    
    premiere_coord = []
    def onclick(event):
        
        global coord
        
        ix, iy = event.xdata, event.ydata
        print ('x = %d, y = %d'%(ix, iy))
    
        global premiere_coord
        premiere_coord.append((int(ix), int(iy)))
    
        if len(premiere_coord) == 1:
            fig.canvas.mpl_disconnect(cid)
            
        photo = im.open("Panier00.PNG")
        photopix = np.array(photo.convert())  
            
        coordx = int(premiere_coord[0][0])
        coordy = int(premiere_coord[0][1])
        
        liste_onclickx = []
        liste_onclicky = []
    
        for k in range(-50,51):
            coordx+=k
            liste_onclickx.append(coordx)
            coordx = int(premiere_coord[0][0])
        
        for k in range(-50,51):
            coordy+=k
            liste_onclicky.append(coordy)
            coordy = int(premiere_coord[0][1])
               
        pts_gris = []
        coord = []
        
        for j in liste_onclickx:
            for i in liste_onclicky:
                if (190 < photopix[i,j][0] <= 250) and (70 < photopix[i,j][1] <= 120) and(20 < photopix[i,j][2] <= 105):
                    pts_gris.append([i,j])
                    
        milieu = int(len(pts_gris)/2)
        coord.append(pts_gris[milieu])
        
        coordx = int(coord[0][1])
        coordy = int(coord[0][0])
         
        for n in range(1,32):

            nom = "Panier"+str(n).zfill(2)+".PNG"
        
            photo = im.open(nom)
            photopix = np.array(photo.convert())
            
            liste_onclickx = []
            liste_onclicky = []
    
            for k in range(-50,51):
                coordx+=k
                liste_onclickx.append(coordx)
                coordx = int(coord[len(coord)-1][1])
        
            for k in range(-50,51):
                coordy+=k
                liste_onclicky.append(coordy)
                coordy = int(coord[len(coord)-1][0])
                  
            pts_gris = []
            
            for j in liste_onclickx:
                for i in liste_onclicky:
                    if (190 < photopix[i,j][0] <= 250) and (70 < photopix[i,j][1] <= 120) and(20 < photopix[i,j][2] <= 105):
                        pts_gris.append([i,j])
            
            milieu = int(len(pts_gris)/2)
            coord.append(pts_gris[milieu])
            
            coordx = int(coord[len(coord)-1][1])
            coordy = int(coord[len(coord)-1][0]) 
            
        print(coord)
        return coord
        
    
    fig = plt.figure()
    plt.imshow(photopix) 
    cid = fig.canvas.mpl_connect('button_press_event', onclick)



elif nom_choisi == "Cycloïde":
    
    photo = im.open("Cycloide508.JPEG")
    photopix = np.array(photo.convert())
    taille=photopix.size
    
    premiere_coord = []
    def onclick(event):
        
        global coord
        
        ix, iy = event.xdata, event.ydata
        print ('x = %d, y = %d'%(ix, iy))
    
        global premiere_coord
        premiere_coord.append((int(ix), int(iy)))
    
        if len(premiere_coord) == 1:
            fig.canvas.mpl_disconnect(cid)
            
        photo = im.open("Cycloide508.JPEG")
        photopix = np.array(photo.convert())  
            
        coordx = int(premiere_coord[0][0])
        coordy = int(premiere_coord[0][1])
        
        #Comme l'utilisateur à le choix entre 3 cibles, on crée 3 variables auxquels on associe
        #un code couleur corespondant aux couleurs du pixel sélectionné par l'utilisateur via le clic
        #qui nous serviras dans le parcours du carré (ici 30x30 pixels)
        R = photopix[coordy,coordx][0]
        V = photopix[coordy,coordx][1]
        B = photopix[coordy,coordx][2]
        
        liste_onclickx = []
        liste_onclicky = []
    
        for k in range(-15,16):
            coordx+=k
            liste_onclickx.append(coordx)
            coordx = int(premiere_coord[0][0])
        
        for k in range(-15,16):
            coordy+=k
            liste_onclicky.append(coordy)
            coordy = int(premiere_coord[0][1])
               
        pts_gris = []
        coord = []
        
        for j in liste_onclickx:
            for i in liste_onclicky:
                #Grace aux 3 variable R,V et B, on impose qu'une seule condition sur les couleurs
                #des pixels parcouru dans le carré 30x30 pixels et cela peu importe le choix de l'utilisateur
                if (R-30 < photopix[i,j][0] <= R+30) and (V-30 < photopix[i,j][1] <= V+30) and(B-30 < photopix[i,j][2] <= B+30):
                    pts_gris.append([i,j])
                    
        milieu = int(len(pts_gris)/2)
        coord.append(pts_gris[milieu])
        
        coordx = int(coord[0][1])
        coordy = int(coord[0][0])
        
        for n in range(508,671):

            nom = "Cycloide"+str(n).zfill(3)+".JPEG"
        
            photo = im.open(nom)
            photopix = np.array(photo.convert())
            
            liste_onclickx = []
            liste_onclicky = []
    
            for k in range(-15,16):
                coordx+=k
                liste_onclickx.append(coordx)
                coordx = int(coord[len(coord)-1][1])
        
            for k in range(-15,16):
                coordy+=k
                liste_onclicky.append(coordy)
                coordy = int(coord[len(coord)-1][0])
                  
            pts_gris = []
            
            for j in liste_onclickx:
                for i in liste_onclicky:
                    if (R-30 < photopix[i,j][0] <= R+30) and (V-30 < photopix[i,j][1] <= V+30) and(B-30 < photopix[i,j][2] <= B+30):
                        pts_gris.append([i,j])
            
            milieu = int(len(pts_gris)/2)
            coord.append(pts_gris[milieu])
            
            coordx = int(coord[len(coord)-1][1])
            coordy = int(coord[len(coord)-1][0]) 
            
        print(coord)
        
        return coord
        
    
    fig = plt.figure()
    plt.imshow(photopix)
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    
elif nom_choisi == "Golf": #Une condition sur la vidéo choisi par l'utilisateur
    
    coord = [] #Liste dans laquelle on stockera les coordonnées de chaque image
    for n in range(32): #Boucle permettant l'ouverture de toutes les images et le parcours d'une zone de ces dernières
    
        pts_blanc = [] #Liste dans laquelle on stockera tous les pixels ayant environ la couleur de l'objet (ici blanc)
        
        nom = "Golf"+str(n).zfill(2)+".PNG" #On modifie le nom des photos
        
        photo = im.open(nom) #On ouvre les photos
        photopix = np.array(photo.convert('L')) #On convertit les photos en tableau
        photopixflou = ndimage.gaussian_filter(photopix, sigma=15) #On applique un flitre pour floutter la photo et ainsi éliminer les pixels blanc parasites (n'appartenant pas à l'objet)
        
        #On parcours une zone de 1080x550 pixels
        for i in range(1080):
            for j in range(750,1300):
                #On vérifie que les pixels parcourus soient blancs
                if 210 < photopixflou[i,j] <= 255:
                    pts_blanc.append([i,j])
                    
        milieu = int(len(pts_blanc)/2) #On associe à la variable milieu la postion (dans la liste pts_blanc) du pixel correspondant au centre de l'objet
        coord.append(pts_blanc[milieu]) #Liste dans laquelle on stock les coordonnées de l'objet de chaque image
        
    print(coord)
    


"-----------------------------------------------------------------------------"

        
    

" tracée de la trajectoire de l'objet "

def draw_trajectoire(coordonnés_points):
    """
     trace la trajectoire de l'objet
    """
    abscisse = []
    ordonnée = []
    
    for i in range(len(coordonnés_points)):
        """
         récupération des cordonnées
        """
        ordonnée.append(coordonnés_points[i][0])
        abscisse.append(coordonnés_points[i][1])
    """
     'lissage' de la courbe
    """
    ordonnée = savgol_filter(ordonnée, 13, 5)
    abscisse = savgol_filter(abscisse, 13, 5)
    
    """
     tracé de la courbe
    """
    plt.clf()
    plt.grid(True)
    plt.xlabel("coordonées en pixels")
    plt.ylabel("coordonnée en pixels")
    plt.title("trajectoire de l'objet en fonction du temps")
    plt.plot(abscisse, ordonnée, label = "trajectoire")
    plt.legend(loc = 1)
    ax = plt.axis()
    plt.axis((ax[0],ax[1],ax[3],ax[2]))
    plt.axis("equal")
    
" mise à l'échelles des coordonées "

def split_x_y(coordonnés_points):
    """
     séparation des coordonnées x et y
    """
    x = []
    y = []
    
    for i in range(len(coordonnés_points)):
        x.append(coordonnés_points[i][1])
        y.append(coordonnés_points[i][0])
    return x, y

    
def configure_space_time(f, k, q):
    """
     converti les pixels en m
     &
     affecte une untité de temps pour chaque valeur
    """
    for i in range(len(f)):
        f[i] = f[i]*k
        f[i] = [i*q,f[i]]
    return f

def configure_x_y(coordonnés_points, Rapport_pixels_metre ,images_par_seconde):
    """
     réunion des fonctions : split_x_y & configure_space_time
    """
    f = coordonnés_points
    
    fonction_x = configure_space_time(split_x_y(f)[0] ,Rapport_pixels_metre ,images_par_seconde)
    fonction_y = configure_space_time(split_x_y(f)[1] ,Rapport_pixels_metre ,images_par_seconde)
    
    return fonction_x, fonction_y


" calcule de dérivé centrée "

def dérivé_centrée(f):
    """
     donne une dérive aproché d'apres le point qui précede et le point suivant
    """
    dérivé_f = []
    
    for i in range(len(f)-1):
        dérivé_f.append([0,0])
        dérivé_f[i][0] = (f[i][0] + f[i+1][0])/2
        dérivé_f[i][1] =(f[i+1][1] - f[i][1])/(f[i+1][0] - f[i][0])
    return dérivé_f


" tracée de la norme de la vitesse de l'objet "

def draw_vitesse(vitesse_x, vitesse_y):
    """
     trace le norme de la vitesse d'après les deux composantes sur X et sur y
    """
    
    time = []
    vitesse = []
    
    """
     calcule de la norme de la vitesse
    """
    for i in range(len(vitesse_x)):
        time.append(vitesse_x[i][0])
        norme_vitesse = sqrt(vitesse_x[i][1]**2 + vitesse_y[i][1]**2)
        vitesse.append(norme_vitesse)
    
    """
     tracé de la norme en fonction du temps
    """
    plt.grid(True)
    plt.xlabel("temps en s")
    plt.ylabel("vitesse en m/s")
    plt.title("norme de la vitesse en fonction du temps")
    plt.plot(time, vitesse, label = "norme de la vitesse")
    plt.legend(loc = 1)
    

" tracée des vecteurs vitesses "

def draw_vecteur(coordonnés_points, vitesse_x, vitesse_y, fréquence_vecteur):
    """
     trace de 1/n vecteur vitesse sur la trajectoire (n = fréquence_vecteur)
    """
    position_x = []
    position_y = []
    norme_x = []
    norme_y = []
    
    """
     liste des vecteur à afficher 
    """
    for i in range(len(coordonnés_points)-1):
        if i % fréquence_vecteur == 0:
            position_x.append(coordonnés_points[i][1])
            position_y.append(coordonnés_points[i][0])
            norme_x.append(vitesse_x[i][1])
            norme_y.append(-vitesse_y[i][1])
    
    abscisse = []
    ordonnée = []
    
    """
     tracé de la trajectoire et des vecteurs
    """
    for i in range(len(coordonnés_points)):
        abscisse.append(coordonnés_points[i][1])
        ordonnée.append(coordonnés_points[i][0])
    
    ordonnée = savgol_filter(ordonnée, 13, 5)
    abscisse = savgol_filter(abscisse, 13, 5)
    
    plt.grid(True)
    plt.title("vitesse en fonction de la position")
    plt.xlabel("position en m")
    plt.ylabel("position en m")
    plt.plot(abscisse, ordonnée, label = "trajectoire")
    ax = plt.axis()
    plt.axis((ax[0],ax[1],ax[3],ax[2]))
    plt.axis("equal")
    plt.quiver(position_x, position_y, norme_x, norme_y, scale_units = "xy")


" tracée de l'accélération "

def draw_accélération(accélération_x, accélération_y):
    """
     trace la norme de l'accélération d'après les composantes sur X et sur Y
    """
    time = []
    accélération = []
    
    """
     calcule de la norme de l'accéleration
    """
    for i in range(len(accélération_x)):
        time.append(accélération_x[i][0])
        norme_accélération = sqrt(accélération_x[i][1]**2 + accélération_y[i][1]**2)
        accélération.append(norme_accélération)
    
    """
     tracé de la norme de l'accélération
    """
    plt.grid(True)
    plt.xlabel("temps en s")
    plt.ylabel("vitesse en m/s**2")
    plt.title("norme de l'accélération en fonction du temps")
    plt.plot(time, accélération, label = "norme de l'accélération")
    plt.legend(loc = 1)


" tracé portrait de phase "

def draw_portrait_phase(fonction_x, vitesse_x, vitesse_y):
    """
     trace le portrait de phase d'apres les composantes de la position & de la vitesse
    """
    distance = []
    vitesse = []
    
    """
     calcule des vitesses et des distances
    """
    for i in range(len(vitesse_x)):
        distance.append(fonction_x[i][1])
        vitesse.append(vitesse_x[i][1])

    vitesse = savgol_filter(vitesse, 13, 5)
    distance = savgol_filter(distance, 13, 5)
    
    """
     tracé de la vitesse en foction de la distance
    """
    plt.grid(True)
    plt.xlabel("distance en m")
    plt.ylabel("vitesse en m/s")
    plt.title("portrait de phase")
    plt.plot(distance, vitesse)
    

    

" aquisition d'informations par l'utilisateur "


    
def calcul_etalon():
    global Rapport_pixels_metre
    global longeur
    global etalon
    global coord_eta
    

    if nom_choisi == "Panier": #Condition sur la vidéo choisi
        longeur = float(input("Longeur en m : ")) #l'utilisateur entre une longeur de référence utile à l'étalon
        photo = im.open("Panier00.PNG")
        photopix = np.array(photo.convert())
        
        coord_eta = []
        def onclick(event):
            ix, iy = event.xdata, event.ydata
            print ('x = %d, y = %d'%(ix, iy))
        
            global coord_eta
            global Rapport_pixels_metre
            coord_eta.append((int(ix), int(iy)))
            print (coord_eta)
        
            if len(coord_eta) == 2:
                fig.canvas.mpl_disconnect(cid)
                
                etalon = int(sqrt((coord_eta[1][0] - coord_eta[0][0])**2 + ((480-coord_eta[1][1]) - (480-coord_eta[0][1]))**2)) #Distance entre 2 points
                print(longeur,"m correspondent à ",etalon," pixels") #Information pour l'utilisateur
                Rapport_pixels_metre = longeur / etalon #Rapport utile pour les calcul de vitesses et accélérations
                return  Rapport_pixels_metre
    
        fig = plt.figure()
        plt.imshow(photopix)
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
    
    #Même principe que précédemment
    if nom_choisi  == "Cycloïde":
        longeur = int(input("Longeur : "))
        photo = im.open("Cycloide000.JPEG")
        photopix = np.array(photo.convert())
        
        coord_eta = []
        def onclick(event):
            global Rapport_pixels_metre
            ix, iy = event.xdata, event.ydata
            print ('x = %d, y = %d'%(ix, iy))
        
            global coord_eta
            coord_eta.append((int(ix), int(iy)))
            print (coord_eta)
        
            if len(coord_eta) == 2:
                fig.canvas.mpl_disconnect(cid)
                
                etalon = int(sqrt((coord_eta[1][0] - coord_eta[0][0])**2 + ((720-coord_eta[1][1]) - (720-coord_eta[0][1]))**2))
                print(longeur,"m correspondent à ",etalon," pixels")
                Rapport_pixels_metre = longeur / etalon
                return Rapport_pixels_metre
        
        fig = plt.figure()
        plt.imshow(photopix)
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
    
    
    
    if nom_choisi ==  "Pendule":
        longeur = int(input("Longeur : "))
        photo = im.open("Pendule000.JPEG")
        photopix = np.array(photo.convert())
        
        coord_eta = []
        def onclick(event):
            global Rapport_pixels_metre
            ix, iy = event.xdata, event.ydata
            print ('x = %d, y = %d'%(ix, iy))
        
            global coord_eta
            coord_eta.append((int(ix), int(iy)))
            print (coord_eta)
        
            if len(coord_eta) == 2:
                fig.canvas.mpl_disconnect(cid)
                
                etalon = int(sqrt((coord_eta[1][0] - coord_eta[0][0])**2 + ((720-coord_eta[1][1]) - (720-coord_eta[0][1]))**2))
                print(longeur,"m correspondent à ",etalon," pixels")
                Rapport_pixels_metre = longeur / etalon
                return Rapport_pixels_metre
        
        fig = plt.figure()
        plt.imshow(photopix)
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
    
    
    
    
    
    if nom_choisi == "Golf":
        print("Diamètre de la balle de Golf: 0.043m ") #Pas de mesure de référence sur la vidéo
        print("Veuillez cliquer aux extrémités de la balle") #On précise ce que doit faire l'utilisateur pour avoir son étalon
        longeur = float(input("Diamètre : "))
        photo = im.open("Golf00.PNG")
        photopix = np.array(photo.convert())
        
        coord_eta = []
        def onclick(event):
            global Rapport_pixels_metre
            ix, iy = event.xdata, event.ydata
            print ('x = %d, y = %d'%(ix, iy))
        
            global coord_eta
            coord_eta.append((int(ix), int(iy)))
            print (coord_eta)
        
            if len(coord_eta) == 2:
                fig.canvas.mpl_disconnect(cid)
                
                etalon = int(sqrt((coord_eta[1][0] - coord_eta[0][0])**2 + ((1080-coord_eta[1][1]) - (1080-coord_eta[0][1]))**2))
                print(longeur,"m correspondent à ",etalon," pixels")
                Rapport_pixels_metre = longeur / etalon
            
                return Rapport_pixels_metre
        
        fig = plt.figure()
        plt.imshow(photopix)
        cid = fig.canvas.mpl_connect('button_press_event', onclick)    


def tracée_courbe():
            global coordonnés_points
            
            coordonnés_points = coord
            images_par_seconde = 1 / int(input("entré la frenquence d'images par seconde de la vidéo : "))
            
            
            "--calcule des positions--"
         
            global fonction_x
            global fonction_y
            
            fonction_x = configure_x_y(coordonnés_points, Rapport_pixels_metre ,images_par_seconde)[0]
            fonction_y = configure_x_y(coordonnés_points, Rapport_pixels_metre ,images_par_seconde)[1]
            
            
            "--calcule des vitesse--"
            
            global vitesse_x
            global vitesse_y
            
            vitesse_x = dérivé_centrée(fonction_x)
            vitesse_y = dérivé_centrée(fonction_y)
            
            
            "--calcule des accélerations--"
         
            global accélération_x
            global accélération_y
            
            accélération_x = dérivé_centrée(vitesse_x)
            accélération_y = dérivé_centrée(vitesse_y)
        