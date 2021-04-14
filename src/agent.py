# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 10:06:00 2021
#chrono 200 300 400 SUR ALEA
#Anneau
@author: Roza
"""
import random
from math import exp
import numpy as np
class Agent():
        def __init__(self,w):
            super().__init__()
            self.g_skill = random.uniform(-1,1)
            self.fitness = 0
            self.genomeList = []
            self.energy = 4
            self.wait = 0
            self.max_energy = 6
            self.sigma = 0.1
            self.listening = 0
            self.fitness_vector = []
            self.w=w
            self.maturity  = 0
            
        def __str__(self):
            return " ".join((str(self.g_skill),str(self.fitness)))
        
        def reactivate(self):
            self.energy = 4
            self.genomeList = []
            self.fitness = 0
            self.fitness_vector = []
            self.wait = 0
            self.listening = 0
            self.maturity = 0
        
        def add_neighbour(self,agent):
            self.neighbours.append(agent)
        
        def add_neighbours(self, agents):
            for a in agents:
                self.add_neighbour(a)
            
        def broadcast(self,a):
            if not self.is_stopped() and self.maturity> self.w :
                if a.wait == 0:
                        a.genomeList.append((self.g_skill,self.fitness))

        def apply_variation_random(self):
            
                liste = self.genomeList
                if liste:           
                    self.g_skill = np.random.choice([elem[0] for elem in liste] ) + random.gauss(0, self.sigma)
                    self.g_skill = min(1, self.g_skill)
                    self.g_skill = max(-1, self.g_skill)
                    self.genomeList = []
                else:
                    self.g_skill = None
        def apply_variation_fitness_prop(self):
                liste = self.genomeList
                if len(liste)>0:
                    x = [elem[1] for elem in liste]
                    if sum(x)== 0:
                        self.g_skill = np.random.choice([elem[0] for elem in liste] ) + random.gauss(0, self.sigma)
                        self.g_skill = min(1, self.g_skill)
                        self.g_skill = max(-1, self.g_skill)
                    else:
                        self.g_skill = np.random.choice([elem[0] for elem in liste],p= np.array(x)/sum(x) ) + random.gauss(0, self.sigma)
                        self.g_skill = min(1, self.g_skill)
                        self.g_skill = max(-1, self.g_skill)
                    self.genomeList = []
                else:
                    self.g_skill = None
                    

        def apply_variation_rank_prop(self):
                liste = self.genomeList
                if len(liste)>0:

                    x = list(range(1, len(liste)+1))
                    if sum(x)== 0:
                        self.g_skill = np.random.choice([elem[0] for elem in liste] ) + random.gauss(0, self.sigma)
                        self.g_skill = min(1, self.g_skill)
                        self.g_skill = max(-1, self.g_skill)
                    else:
                        self.g_skill = np.random.choice([elem[0] for elem in sorted(liste, key=lambda tup: tup[1])],p= np.array(x)/sum(x) )  + random.gauss(0, self.sigma)
                        self.g_skill = min(1, self.g_skill)
                        self.g_skill = max(-1, self.g_skill)
                    self.genomeList = []
                else:
                    self.g_skill = None
        def apply_variation_fitness(self):
                liste = self.genomeList
                if len(liste)>0:
                    c = random.gauss(0, self.sigma)
                    #print(c , max(self.genomeList, key = lambda i : i[1])[0]  )
                    self.g_skill = max(liste, key = lambda i : i[1])[0]  + c
                    self.g_skill = min(1, self.g_skill)
                    self.g_skill = max(-1, self.g_skill)
                    self.genomeList = []
                else:
                    self.g_skill = None
        def get_neighbours(self):
            return self.neighbours
                
        def get_genome(self):
            return self.g_skill
        
        def get_fitness(self):
            return self.fitness
        def f_syn(self, env):
            if self.g_skill > 0 and env.R1<= 0:
                return 0
            if self.g_skill < 0 and env.R2<= 0:
                return 0
            if self.g_skill > 0 :    
                env.R1 -= 1
                return 1/(1 + exp(10*(-2*self.g_skill+1)))
            if self.g_skill < 0 :
                env.R2 -= 1
                return 1/(1 + exp(10*((2*self.g_skill)+1)))
            else:
                return 0

        def compute_fitness(self, env):
            if not self.is_stopped():
                x=self.f_syn(env)
                self.fitness_vector.append(x)
                self.energy = min(self.max_energy , self.energy+ x)                
                if self.maturity > self.w :
                    self.fitness_vector.pop(0)
                    self.fitness =sum(self.fitness_vector)


            
        ''' def get_group(self):

            if self.g_skill>=0 :
                return 0
            elif self.g_skill<0:
                return 1'''

            
        def move(self, env):
            self.maturity += 1
            if self.is_stopped():
                env.R1 -= 0.5
                env.R2 -= 0.5
                if self.wait > 0  or self.listening >0:
                    self.charge()
            else :
                self.energy = max(0 , self.energy-1)
                if self.energy == 0:
                    #self.genomeList = []
                    self.wait = random.randint(4, 15)

        
        def is_stopped(self):
            if self.wait > 0  or self.listening >0 or self.g_skill == None:
                return True
            else:
                return False
        
        
        def charge(self):
            if self.wait > 0:
                self.wait -= 1
                if self.wait == 0:
                    self.energy = 4
                    self.listening = 4
            else:
                self.listening -= 1
        
                