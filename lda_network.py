#!/usr/bin/env python

from gensim.models import LdaModel
import networkx as nx
import matplotlib.pyplot as plt
import sys, os


#############
# cf. http://nbviewer.ipython.org/github/sgsinclair/alta/blob/master/ipynb/TopicModelling.ipynb#Graphing-Topic-Terms

def graph_terms_to_topics(lda, outfile, num_terms=30):

    # create a new graph and size it
    G = nx.Graph()
    plt.figure(figsize=(30,30))

    # generate the edges
    for i in range(0, lda.num_topics):
        topicLabel = "topic "+str(i)
        terms = [term for val, term in lda.show_topic(i, num_terms)]
        for term in terms:
            G.add_edge(topicLabel, term)


    # cf. http://networkx.lanl.gov/reference/drawing.html#module-networkx.drawing.layout
    pos = nx.spring_layout(G, k=0.060, iterations=30) # positions for all nodes - k=0.020, iterations=30
    #pos = nx.circular_layout(G)
    #pos = nx.shell_layout(G)
    #pos = nx.spectral_layout(G)


    # we'll plot topic labels and terms labels separately to have different colours
    g = G.subgraph([topic for topic, _ in pos.items() if "topic " in topic])
    nx.draw_networkx_labels(g, pos,  font_color='c')

    g = G.subgraph([term for term, _ in pos.items() if "topic " not in term])
    nx.draw_networkx_labels(g, pos, font_size=10, alpha=0.9)

    # plot edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='g', alpha=0.3)

    for n in G:
        #if 1 < G.degree(n) < num_terms: nx.draw_networkx_edges(G, pos, edgelist=nx.edges(G, nbunch=n), alpha=0.2)
        if G.degree(n) < 2: nx.draw_networkx_edges(G, pos, edgelist=nx.edges(G, nbunch=n), edge_color='r', alpha=0.3)

    plt.axis('off')
    plt.savefig(outfile)
    #plt.show()



if len(sys.argv) < 2:
    print("usage: {0} [path to model.lda]\n".format(sys.argv[0]))
    sys.exit(1)


path, file = os.path.split(sys.argv[1])
corpusname = file.split(".")[0]
outfile = path+"/"+corpusname+"_network.png"

model = LdaModel.load(sys.argv[1])

graph_terms_to_topics(model, outfile)