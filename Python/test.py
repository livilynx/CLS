#!/usr/bin/python
# -*-coding:utf-8 -*

import Utilities.calcul as ut
import Utilities.suppVitesseExcess as sup
# import Utilities.carte as mp
import RWFormats.lecture as rd
import RWFormats.nettoyage as laver
import RWFormats.recuperation as recup

fichierTest1 = open("fichierTest1.txt", "w")
fichierTest2 = open("fichierTest2.txt", "w")

# pour les cartes
# from mpl_toolkits.basemap import Basemap
# import matplotlib.pyplot as plt
# import numpy as np

<<<<<<< HEAD
#path ="/Users/atnd/Documents/ENSEEIHT/ProjetLong/CLS/tortues/DIAG/25532.DIAG"
#path ="/home/jcombani/3A/Projet long/tortues/DIAG/10248.DIAG"
path = "/Users/Benoit/Documents/GitHub/CLS/tortues/DIAG/10248.DIAG"

=======
#path ="/Users/atnd/Documents/ENSEEIHT/ProjetLong/CLS/tortues/DIAG/10248.DIAG"
path ="/home/jcombani/3A/Projet long/tortues/DIAG/10248.DIAG"
>>>>>>> 7d87aab99caf2b6f871a73ed2f1002012ec35e93

liste = rd.lectureToutDiag(path)
liste = laver.monsieurPropre(liste, "lat")
liste = ut.correctionChoixLoc(liste)
liste = sup.suppVitesseExcess(liste,recup.recuperation,ut.convertArrayOfTime,ut.calculVitesses,3)
<<<<<<< HEAD
lat = recup.recuperation(liste,'lat')
lon = recup.recuperation(liste,'lon')
for j in range(len(liste)):
	fichierTest1.write(str(lat[j]))
	fichierTest1.write("\n")
	fichierTest2.write(str(lon[j]))
	fichierTest2.write("\n")

fichierTest1.close()	
fichierTest2.close()	


# liste = ut.regressionLineaire(2, liste, 0.02, recup.recuperation)
# print(len(liste))
# latitudes = map(float, recup.recuperation(liste, "lat"))
# longitudes = map(float, recup.recuperation(liste, "lon"))
# #print(latitudes)
# #print(longitudes)

# mp.tracerCarte(longitudes, latitudes)
=======
print(len(liste))

latitudes = map(float, recup.recuperation(liste, "lat"))
longitudes = map(float, recup.recuperation(liste, "lon"))

liste = ut.regressionLineaire(1, liste, 0.2, recup.recuperation)
print(len(liste))

latitudes2 = map(float, recup.recuperation(liste, "lat"))
longitudes2 = map(float, recup.recuperation(liste, "lon"))


mp.tracerCarte([longitudes, longitudes2],[latitudes, latitudes2], ["b", "r"])
>>>>>>> 7d87aab99caf2b6f871a73ed2f1002012ec35e93

