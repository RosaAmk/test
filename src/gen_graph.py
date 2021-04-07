
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 19:26:55 2021

@author: roza
"""
import graphviz as pgv
import random
import numpy as np

class Graph():
    def __init__(self,n, d):
        self.n = n
        self.d = d
        self.parent = [i for i in range(n)]
        self.rang = n*[0]
        self.cpt = n*[0]    
        self.edges_final = []

    def join( self, a ,b ):
        self.cpt[a] += 1
        self.cpt[b] += 1
        self.Union(self.parent,self.rang,a,b)
                             
    def gen_graph(self):
        if(self.d < 2/self.n):
            print('impossible')
            return 0
        edges = [(i,j) for i in range(self.n) for j in range(i+1,self.n)]       
        while len(self.edges_final)/((self.n)*(self.n-1)) < self.d/2 :
            e = random.choice(edges)
            self.edges_final.append(e)
            edges.remove(e)
            self.join(e[0], e[1])
        removable = self.get_Removable(self.edges_final)
        while(len(set([self.Find(self.parent,elem) for elem in range(self.n)])) > 1 ): 
            removable = self.get_Removable(removable)                   
            a = random.choice(removable)
            removable.remove(a)  
            self.supprime(a)
            Missing = self.get_connecting()
            e = random.choice(Missing)
            while e == a:
                e = random.choice(Missing)
            self.edges_final.append(e)
            self.join(e[0], e[1])
        

        
    def get_connecting(self):
        comp = set([self.Find(self.parent, x) for x in range(self.n)])
        Missing = []
        l = []
        for elem in comp:
            s = [i for i in range(self.n) if self.Find(self.parent,i)== elem]
            l.append(s)
        if len(l) > 1:
            for i in range(len(l)):
                for j in range(i+1,len(l)):
                    Missing.extend([(min(a,b),max(a,b) ) for a in l[i] for b in l[j]])       
        return Missing
        
    def get_Removable(self, from_list):
        rem = []
        for e in from_list:
            if self.superflue(e):
                rem.append(e)
        return rem
    def superflue(self,e):
        c = self.Find(self.parent,e[0])
        l = [a for a in self.edges_final if self.Find(self.parent,a[0]) == c and e != a]
        n = set([x for elem in l for x in elem ])
        n.add(e[0])
        n.add(e[1])
        connex = dict()
        rang = dict()
        for elem in n:
            connex[elem] = elem
            rang[elem] = 0
        for edge in l:
            self.Union(connex,rang,edge[0], edge[1])
        return len(set([self.Find(connex,elem) for elem in n])) == 1
        


    
        
    def supprime(self, e):
        self.cpt[e[0]] -=   1   
        self.cpt[e[1]] -=   1 
        self.edges_final.remove(e)
        m = self.Find(self.parent,e[0])
        l = [i for i in range(self.n) if self.Find(self.parent,i)== m]
        self.cpt = [0 if self.Find(self.parent, v)==m else self.cpt[v] for v in range(self.n)]
        self.parent = [i if self.Find(self.parent, i)==m else self.Find(self.parent, i) for i in range(self.n)]
        self.rang = [0 if self.Find(self.parent, i)==m else self.rang[i] for i in range(self.n)]
        for i in range(len(l)):
            for j in range(i+1,len(l)):
                if (l[i],l[j]) in self.edges_final or (l[j],l[i]) in self.edges_final:
                    self.join(l[i],l[j])
                                       
    def Find(self,parent,x):
         if parent[x] != x:
             parent[x] = self.Find(parent,parent[x])
         return parent[x]
     
    def Union(self,parent,rang ,x, y):
     xRacine = self.Find(parent,x)
     yRacine = self.Find(parent,y)
     if xRacine != yRacine:
           if rang[xRacine] < rang[yRacine]:
                 parent[xRacine] = yRacine
           else:
                 parent[yRacine] = xRacine
                 if rang[xRacine] == rang[yRacine]:
                         rang[xRacine] += 1


if __name__ == '__main__':
    g = Graph(500,0.004)
    g.gen_graph()
    for e in g.edges_final:
        print(e[0], e[1]) 
    graph = pgv.Digraph()
    for i in range(g.n):
        graph.node(str(i))
    for e in g.edges_final:
        graph.edge(str(e[0]), str(e[1])) 
    graph.render()