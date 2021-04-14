# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 20:51:21 2021

@author: roza
"""
from agent import Agent
from gen_graph import Graph
import random
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import graphviz as pgv
import plot
nb_agent = 10
nb_it = 1000
lifetime = 400
density=2/nb_agent
w = 100
class Env():
    def __init__(self):
        self.R1 = nb_agent*nb_it *lifetime/2
        self.R2 = nb_agent*nb_it *lifetime/2        

def gen_from_density(n,d): 
    g1 = Graph(n,d)
    g = []
    for i in range(n):
        g.append(Agent(w))
    g1.gen_graph()
    graph = pgv.Digraph()
    for i in range(n):
        graph.node(str(g[i].g_skill))
    for e in g1.edges_final:
        graph.edge(str(g[e[0]].g_skill), str(g[e[1]].g_skill)) 
    return g, g1.edges_final

def gen_star(n):
    g = []
    center = Agent(w)
    g.append(center)
    for i in range(n-1):
        new = Agent()
        new.add_neighbour(center)
        center.add_neighbour(new)
        g.append(new)
    return g

def gen_complet(n):
    g = []
    for i in range(n):
        g.append(Agent())
    for i in range(n):
        g[i].add_neighbours(g[0:i])
        g[i].add_neighbours(g[i+1:n])
    return g
    
def gen_ring(n):
    g = []
    for i in range(n):
        g.append(Agent(w))

    e = [(i,(i+1)%n) for i in range(n)]
    
    return g,e
def gen_chaine(n):
    g = []
    for i in range(n):
        g.append(Agent(w))

    e = [(i,i+1) for i in range(n-1)]
    
    return g,e
        
def exp(nb_agent):
    res = dict()
    methods = ['fitness prop', 'random', 'Best', 'rank prop']
    gskills = dict()

    for method in range(2):
        print(methods[method])
        c3 = []
        for j in range(20):
            i = 0
            for e in np.linspace(-1,1,21):
                gskills[round(e,1)] = i
                i += 1
            graph,edges = gen_from_density(nb_agent, 2/nb_agent)
            env = Env()
            for i in range(nb_it):
                for k in range(lifetime):
                    env.R1 = nb_agent/2
                    env.R2 = nb_agent/2    
                    for a in graph:
                        a.move(env)
                        a.compute_fitness(env)
                    for e in edges:
                        graph[e[0]].broadcast(graph[e[1]])
                        graph[e[1]].broadcast(graph[e[0]])
                n = 0
                for a in graph:
                    if method == 0:                        
                        a.apply_variation_fitness_prop()                      
                    if method == 1:
                        a.apply_variation_random()
                    if method == 2:
                        a.apply_variation_fitness()
                    if method == 3:
                        a.apply_variation_rank_prop()
                    n += 1
            cpt = 0   
            for a in graph:                
                if not a.is_stopped() :
                        cpt  += 1
            c3.append(cpt)
            print(cpt)

        print(c3)


if __name__ == '__main__':
    exp(300)