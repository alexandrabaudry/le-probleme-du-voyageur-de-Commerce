from __future__ import (absolute_import, division, print_function)

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import time
from fonction import Ville, CircuitPossible, Circuit, Population, Algorithme

nombre_executions = 20
taille_groupe = 10

# Liste pour stocker les temps d'exécution
execution_times = []

# Boucle pour effectuer plusieurs exécutions
for _ in range(nombre_executions):
    
    start = time.time()
    
    for i in range(10000):
        i**i
    
    execution_times.append(time.time() - start)

print(execution_times[-1])

# Programme principale 

if __name__ == '__main__':
   
   gc = CircuitPossible()   

   #on cree nos villes
   ville1 = Ville(3.002556, 45.846117, 'Clermont-Ferrand')
   gc.joindreVille(ville1)
   ville2 = Ville(-0.644905, 44.896839, 'Bordeaux')
   gc.joindreVille(ville2)
   ville3 = Ville(-1.380989, 43.470961, 'Bayonne')
   gc.joindreVille(ville3)
   ville4 = Ville(1.376579, 43.662010, 'Toulouse')
   gc.joindreVille(ville4)
   ville5 = Ville(5.337151, 43.327276, 'Marseille')
   gc.joindreVille(ville5)
   ville6 = Ville(7.265252, 43.745404, 'Nice')
   gc.joindreVille(ville6)
   ville7 = Ville(-1.650154, 47.385427, 'Nantes')
   gc.joindreVille(ville7)
   ville8 = Ville(-1.430427, 48.197310, 'Rennes')
   gc.joindreVille(ville8)
   ville9 = Ville(2.414787, 48.953260, 'Paris')
   gc.joindreVille(ville9)
   ville10 = Ville(3.090447, 50.612962, 'Lille')
   gc.joindreVille(ville10)
   ville11 = Ville(5.013054, 47.370547, 'Dijon')
   gc.joindreVille(ville11)
   ville12 = Ville(4.793327, 44.990153, 'Valence')
   gc.joindreVille(ville12)
   ville13 = Ville(2.447746, 44.966838, 'Aurillac')
   gc.joindreVille(ville13)
   ville14 = Ville(1.750115, 47.980822, 'Orleans')
   gc.joindreVille(ville14)
   ville15 = Ville(4.134148, 49.323421, 'Reims')
   gc.joindreVille(ville15)
   ville16 = Ville(7.506950, 48.580332, 'Strasbourg')
   gc.joindreVille(ville16)
   ville17 = Ville(1.233757, 45.865246, 'Limoges')
   gc.joindreVille(ville17)
   ville18 = Ville(4.047255,48.370925, 'Troyes')
   gc.joindreVille(ville18)
   ville19 = Ville(0.103163,49.532415, 'Le Havre')
   gc.joindreVille(ville19)
   ville20 = Ville(-1.495348, 49.667704, 'Cherbourg')
   gc.joindreVille(ville20)
   ville21 = Ville(-4.494615, 48.447500, 'Brest')
   gc.joindreVille(ville21)
   ville22 = Ville(-0.457140, 46.373545, 'Niort')
   gc.joindreVille(ville22)
   ville23=Ville(2.8948332,42.6886591,'Perpignan')
   gc.joindreVille(ville23)
   ville24=Ville(-3.3702449,47.7482524,'Lorient')
   gc.joindreVille(ville24)
   
    # Initialisation de la population
   pop = Population(gc, 50, True)

   # Algorithme génétique
   a = Algorithme(gc)
   meilleure_population_data = []
   execution_times = []  # Liste pour stocker les temps d'exécution

    # Boucle pour effectuer plusieurs exécutions
   for _ in range(nombre_executions):
       start = time.time()

        # Créez une nouvelle instance de la population à chaque itération
       pop = Population(gc, 50, True)
        
        # Évolution de la population
       for i in range(1000):
           pop = a.Evolution_Population(pop)
        
        # Collectez les données de la meilleure population
       longitudes = []
       latitudes = []
       noms = []
       meilleure_population = pop.getFittest()

       for i in range(meilleure_population.tailleCircuit()):
           ville = meilleure_population.getVille(i)
           longitudes.append(ville.longitude)
           latitudes.append(ville.latitude)
           noms.append(ville.nom)

       meilleure_population_data.append((longitudes, latitudes, noms))

        # Enregistrez le temps d'exécution
       execution_times.append(time.time() - start)

    # Affichage des temps d'exécution
   print("Temps d'exécution pour chaque itération:", execution_times)

    # Tracé du graphique du temps d'exécution
   plt.figure(figsize=(16, 12))
   plt.plot(range(len(execution_times)), execution_times, marker='+')
   plt.xlabel('Exécution')
   plt.ylabel('Temps (s)')
   plt.title("Évolution du temps d'exécution")
   plt.grid(True)
   plt.show()

    # Divisez les 50 cartes en groupes de 10
nombre_executions = 50
taille_groupe = 10

# Boucle pour effectuer plusieurs exécutions
for groupe in range(nombre_executions // taille_groupe):
    fig, axes = plt.subplots(2, 5, figsize=(20, 15))

    for i in range(taille_groupe):
        index_execution = groupe * taille_groupe + i
        if index_execution >= nombre_executions:
            break

        ax = axes[i // 5, i % 5]

        longitudes, latitudes, noms = meilleure_population_data[index_execution]

        map = Basemap(llcrnrlon=-5.5, llcrnrlat=42.3, urcrnrlon=9.3, urcrnrlat=51., resolution='i', projection='tmerc', lat_0=45.5, lon_0=-3.25, ax=ax)
        map.drawcoastlines()
        map.drawmapboundary(fill_color='aqua')
        map.fillcontinents(color='coral', lake_color='aqua')
        map.drawcoastlines()
        map.drawcountries()
        x, y = map(longitudes, latitudes)
        map.plot(x, y, 'bo', markersize=12)
        for nom, xpt, ypt in zip(noms, x, y):
            ax.text(xpt + 5000, ypt + 25000, nom)
        map.plot(x, y, 'D-', markersize=10, linewidth=2, color='k', markerfacecolor='b')
        plt.title(f"Groupe {groupe + 1} - Carte {i + 1}")

    plt.tight_layout()
    plt.show()
