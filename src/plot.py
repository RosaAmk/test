# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 21:04:12 2021

@author: gr_am
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcol

def violin_plots(data , labels, title):
    fig,ax=plt.subplots(figsize=(5,5))

    ax.violinplot(data, showmeans=False, showmedians=True)
    ax.set_title(title)
    # adding horizontal grid lines
    ax.yaxis.grid(True)
    ax.set_xticks([y + 1 for y in range(len(data))])
    ax.set_xlabel('selection methods')
    ax.set_ylabel('Active agents')

    # add x-tick labels
    plt.setp(ax, xticks=[y + 1 for y in range(len(data))],
        xticklabels=labels)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    plt.show()   

def heatmap_plot(labels_x, labels_y, data , title):
    '''labels_y = ["cucumber", "tomato", "lettuce", "asparagus",
              "potato", "wheat", "barley"]
    labels_x = ["Farmer Joe", "Upland Bros.", "Smith Gardening",
           "Agrifun", "Organiculture", "BioGoods Ltd.", "Cornylee Corp."]

    harvest = np.array([[0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
                    [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
                    [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
                    [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
                    [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
                    [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
                    [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]])'''


    fig, ax = plt.subplots()
    im = ax.imshow(data, cmap='gray_r')
    plt.gray()
    # We want to show all ticks...
    ax.set_xticks(np.arange(len(labels_x)))
    ax.set_yticks(np.arange(len(labels_y)))
    cbar = ax.figure.colorbar(im, ax=ax)

    ax.set_title(title)
    fig.tight_layout()
    plt.show()
    
def chrono_plot( data , title):
    fig, ax = plt.subplots()
    cm1 = mcol.LinearSegmentedColormap.from_list("MyCmapName",["r","b"])

    im = ax.imshow(data,  cmap=cm1 , interpolation='nearest', aspect='auto')
    cbar = ax.figure.colorbar(im, ax=ax)

    ax.set_title(title)
    fig.tight_layout()
    plt.show()


   