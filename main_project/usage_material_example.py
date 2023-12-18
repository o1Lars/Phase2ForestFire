import visualiser_random_forest_graph as vr
import graph_helper as gh
import random

""" edgelist,pos = gh.voronoi_to_edges(300)
print(gh.edges_planar(edgelist))

mvr=vr.Visualiser(edgelist,pos_nodes=pos,node_size=50)
cmap= {i:random.randint(0,265) for i in random.sample(list(pos.keys()),int(0.8*len(pos)))}
mvr.update_node_colours(cmap)
nodes_edges=random.sample(list(pos.keys()),0)
mvr.update_node_edges(nodes_edges)

mvr.wait_close() """

test_edges = [(1, 2), (1,3), (2,3)]
test_colors = {1: 265, 2: -265, 3:2}


test_vis = vr.Visualiser(edges=test_edges, node_size=100)
cmap= test_colors
test_vis.update_node_colours(cmap)
test_vis.wait_close()