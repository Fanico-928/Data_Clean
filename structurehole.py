

import json
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
 
G = nx.Graph()

G.add_edge('A','B')
G.add_edge('A','B')
G.add_edge('A','D')
G.add_edge('D','B')
G.add_edge('A','Y')
G.add_edge('X','B')
G.add_edge('A','X')


structurehole1  = nx.effective_size(G)

print (structurehole1 )