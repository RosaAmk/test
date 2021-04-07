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
nb_agent = 100
nb_it = 1000
lifetime = 400
w = 100
density = 0.1
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
    '''
    graph = pgv.Digraph()
    for i in range(n):
        graph.node(str(g[i].g_skill))
    for e in g1.edges_final:
        graph.edge(str(g[e[0]].g_skill), str(g[e[1]].g_skill)) 
    '''
    return g, g1.edges_final

def gen_star(n):
    g = []
    center = Agent()
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
    prec = 0
    for i in range(n):
        current = Agent()
        g.append(current)
        if prec != 0:
            prec.add_neighbour(current)
            current.add_neighbour(prec)
        prec = current
    g[0].add_neighbour(g[n-1])
    g[n-1].add_neighbour(g[0])
    return g
def gen_chaine(n):
    g = []
    prec = 0
    for i in range(n):
        current = Agent()
        g.append(current)
        if prec != 0:
            prec.add_neighbour(current)
            current.add_neighbour(prec)
        prec = current
    return g
        
if __name__ == '__main__':
    res = dict()
    methods = [ 'random','fitness prop', 'rank prop', 'Best']
    gskills = dict()

    for method in range(4):
        print(methods[method])
        c2 = Counter()
        c3 = []
        for j in range(10):
            i = 0
            for e in np.linspace(-1,1,21):
                gskills[round(e,1)] = i
                i += 1
                gskills_mat =np.zeros((21,nb_it//100))
            graph,edges = gen_from_density(nb_agent,density)
            
            env = Env()

            for i in range(nb_it):
                print(i)
                for k in range(lifetime):
                    env.R1 = nb_agent/2
                    env.R2 = nb_agent/2    
                    for a in graph:
                        
                        a.move(env)
                        a.compute_fitness(env)
                    for e in edges:
                        graph[e[0]].broadcast(graph[e[1]])
                        graph[e[1]].broadcast(graph[e[0]])
                        #print(0 , a.is_stopped(),a.g_skill, a.energy, a.fitness)
                for a in graph:
                    if method == 0:
                        a.apply_variation_random()
                    if method == 1:                        
                        a.apply_variation_fitness_prop()                      
                    if method == 2:
                        a.apply_variation_rank_prop()
                    if method == 3:
                        a.apply_variation_fitness()

                    if i%100 == 0:
                        if a.g_skill != None:
                            gskills_mat[gskills[round(a.g_skill,1)] , i//100 ] += 1

                            
                            

                
                
            cpt = 0   
            for a in graph:
                if not a.is_stopped() :
                        cpt  += 1
                        
            #c2[cpt] += 1
            c3.append(cpt)
            #labels, values = zip(*sorted(c.items()))
            #indexes = np.arange(len(labels))
            plot.heatmap_plot([(i+1)*100 for i in range(nb_it//100)] ,gskills.keys(),  gskills_mat , methods[method])
            #plt.bar(indexes, values)
            #plt.xticks(indexes , labels)
            #plt.show()
            
        ''' 
        labels, values = zip(*sorted(c2.items()))
        indexes = np.arange(len(labels))
    
        plt.bar(indexes, values)
        plt.xticks(indexes , labels)
        plt.show()'''
        res[method] = c3
    
    data=[]
    labels=[]
    
    for k in res.keys():
        data.append(res[k])
        labels.append(methods[k])
    plot.violin_plots(data, labels, 'Violon plots with density == 0,1 with 100 agents')
