import visualiser_random_forest_graph as vr
import graph_helper as gh
import random
edgelist,pos = gh.voronoi_to_edges(300)
print(gh.edges_planar(edgelist))

mvr=vr.Visualiser(edgelist,pos_nodes=pos,node_size=50)
cmap= {i:random.randint(0,265) for i in random.sample(list(pos.keys()),int(0.8*len(pos)))}
mvr.update_node_colours(cmap)
nodes_edges=random.sample(list(pos.keys()),0)
mvr.update_node_edges(nodes_edges)

mvr.wait_close()