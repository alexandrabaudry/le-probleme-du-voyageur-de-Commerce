
#from __future__ import (absolute_import, division, print_function)
from __future__ import (absolute_import, division, print_function)

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import time
#----------------------------------------------On calcule le temps d'execution du programme---------------------------------------------#


#----------------------------------------------On définie la classe ville avec les coordonnées géographiques---------------------------------------------#
class Ville:
   def __init__(self, longitude, latitude, nom):      # Initialisation d'une ville
      self.longitude = longitude
      self.latitude = latitude
      self.nom = nom
   

   def distance(self, ville):				# Distance de ville à Ville 
      distanceX = (ville.longitude-self.longitude)*40000*math.cos((self.latitude+ville.latitude)*math.pi/360)/360
      distanceY = (self.latitude-ville.latitude)*40000/360
      distance = math.sqrt( (distanceX*distanceX) + (distanceY*distanceY) )
      return distance
#----------------------------------------------On Définie la classe des circuits possibles sur une carte ---------------------------------------------#
class CircuitPossible:
   villesDestinations = []
   
   def joindreVille(self, ville): 			# relier 2 Villes entre elles
      self.villesDestinations.append(ville)
   
   def getVille(self, index):				#Obtenir l'index d'une Ville
      return self.villesDestinations[index]
   
   def Nbr_Villes(self):				# Fonction qui retourne le nombre de Villes sur un parcours
      return len(self.villesDestinations)
#----------------------------------------------On Définit la classe Circuit  --------------------------------------------------------------------------#
class Circuit:
   def __init__(self, CircuitPossible, circuit=None):    		#Initialisation d'un circuit
      self.CircuitPossible = CircuitPossible
      self.circuit = []
      self.fitness = 0.0
      self.distance = 0
      if circuit is not None:
         self.circuit = circuit
      else:
         for i in range(0, self.CircuitPossible.Nbr_Villes()):
            self.circuit.append(None)

   def __len__(self): 							# Calcul longueur d'un circuit
      return len(self.circuit)
   
   def __getitem__(self, index):					#accéder à la valeur d’une liste, d’un dictionnaire ou d’un tuple à partir d’un index spécifique.
      return self.circuit[index]

   def __setitem__(self, key, value):					#méthode utilisée pour attribuer une valeur à un élément.
      self.circuit[key] = value

   def Nouvel_Individu(self):						# Nouvelle ville donc nouveau chemin possible
     for indiceVille in range(0, self.CircuitPossible.Nbr_Villes()):
        self.setVille(indiceVille, self.CircuitPossible.getVille(indiceVille))
     random.shuffle(self.circuit)

   def getVille(self, circuitPosition):
     return self.circuit[circuitPosition]

   def setVille(self, circuitPosition, ville):
     self.circuit[circuitPosition] = ville
     self.fitness = 0.0
     self.distance = 0

   def getFitness(self):
     if self.fitness == 0:
        self.fitness = 1/float(self.getDistance())
     return self.fitness

   def getDistance(self):
     if self.distance == 0:
        circuitDistance = 0
        for indiceVille in range(0, self.tailleCircuit()):
           villeOrigine = self.getVille(indiceVille)
           villeArrivee = None
           if indiceVille+1 < self.tailleCircuit():
              villeArrivee = self.getVille(indiceVille+1)
           else:
              villeArrivee = self.getVille(0)
           circuitDistance += villeOrigine.distance(villeArrivee)
        self.distance = circuitDistance
     return self.distance

   def tailleCircuit(self):
     return len(self.circuit)

   def contientVille(self, ville):
     return ville in self.circuit
     
#----------------------------------------------------- On définit la classe Population----------------------------------------------------------------#
class Population:
   def __init__(self, CircuitPossible, SizePopulation, init): 	#Initialisation
      self.circuits = []
      for i in range(0, SizePopulation):
         self.circuits.append(None)
      
      if init:
         for i in range(0, SizePopulation):
            nouveauCircuit = Circuit(CircuitPossible)
            nouveauCircuit.Nouvel_Individu()
            self.SaveCircuit(i, nouveauCircuit)
      
   def __setitem__(self, key, value):
      self.circuits[key] = value
   
   def __getitem__(self, index):
      return self.circuits[index]
   
   def SaveCircuit(self, index, circuit):				# Enregistrement d'un circuit 
      self.circuits[index] = circuit
   
   def getCircuit(self, index):
      return self.circuits[index]
   
   def getFittest(self):
      fittest = self.circuits[0]
      for i in range(0, self.SizePopulation()):
         if fittest.getFitness() <= self.getCircuit(i).getFitness():
            fittest = self.getCircuit(i)
      return fittest
   
   def SizePopulation(self):
      return len(self.circuits)
      
#------------------------------------------------On définit la classe Algorithmes ----------------------------------------------------------------------#
class Algorithme:
   def __init__(self, CircuitPossible):
      self.CircuitPossible = CircuitPossible
      self.tauxMutation = 0.015
      self.tailleTournoi = 5
      self.elitisme = True
   
   def Evolution_Population(self, pop):
      nouvellePopulation = Population(self.CircuitPossible, pop.SizePopulation(), False)
      elitismeOffset = 0
      if self.elitisme:
         nouvellePopulation.SaveCircuit(0, pop.getFittest())
         elitismeOffset = 1
         
      for i in range(elitismeOffset, nouvellePopulation.SizePopulation()):
         parent1 = self.selectionTournoi(pop)
         parent2 = self.selectionTournoi(pop)
         enfant = self.Croisement(parent1, parent2)
         nouvellePopulation.SaveCircuit(i, enfant)
         
      for i in range(elitismeOffset, nouvellePopulation.SizePopulation()):
         self.Mutation(nouvellePopulation.getCircuit(i))
         
      return nouvellePopulation


   def Croisement(self, parent1, parent2):
      enfant = Circuit(self.CircuitPossible)
         
      startPos = int(random.random() * parent1.tailleCircuit())
      endPos = int(random.random() * parent1.tailleCircuit())
         
      for i in range(0, enfant.tailleCircuit()):
         if startPos < endPos and i > startPos and i < endPos:
            enfant.setVille(i, parent1.getVille(i))
         elif startPos > endPos:
            if not (i < startPos and i > endPos):
               enfant.setVille(i, parent1.getVille(i))
         
      for i in range(0, parent2.tailleCircuit()):
         if not enfant.contientVille(parent2.getVille(i)):
            for ii in range(0, enfant.tailleCircuit()):
               if enfant.getVille(ii) == None:
                  enfant.setVille(ii, parent2.getVille(i))
                  break
      
      return enfant
   
   def Mutation(self, circuit):
     for circuitPos1 in range(0, circuit.tailleCircuit()):
        if random.random() < self.tauxMutation:
           circuitPos2 = int(circuit.tailleCircuit() * random.random())
           
           ville1 = circuit.getVille(circuitPos1)
           ville2 = circuit.getVille(circuitPos2)
           
           circuit.setVille(circuitPos2, ville1)
           circuit.setVille(circuitPos1, ville2)

   def selectionTournoi(self, pop):
     tournoi = Population(self.CircuitPossible, self.tailleTournoi, False)
     for i in range(0, self.tailleTournoi):
        randomId = int(random.random() * pop.SizePopulation())
        tournoi.SaveCircuit(i, pop.getCircuit(randomId))
     fittest = tournoi.getFittest()
     return fittest

     
