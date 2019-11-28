import os
import time
from progress import Progress
import itertools
import networkx
import random
WEB_DATA = os.path.join(os.path.dirname(__file__), 'school_web.txt')


def load_graph(fd):
    """Load graph from text file

    Parameters:
    fd -- a file like object that contains lines of URL pairs

    Returns:
    A representation of the graph.

    Called for example with


    the function parses the input file and returns a graph representation.
    Each line in the file contains two white space seperated URLs and
    denotes a directed edge (link) from the first URL to the second.
    """
    # Iterate through the file line by line
    websites={}#dictionary of websites: Key is a link, value is a list of links.
    graph=networkx.DiGraph()
    for line in fd:
        # And split each line into two URLs
        node, target = line.split()
        if not graph.has_node(node):#this checks to add the node to the dictionary
            graph.add_node(node)
            graph.add_edge(node,target)
        else:#if the node exists add the next value to the list of values
            graph.add_edge(node, target)
    print("graph created")
    for i in range(0,len(graph.nodes)):
        print(list(graph.nodes)[i])
        print(len(graph.edges(list(graph.nodes)[i])))
    return graph#return the dictionary of connections


def print_stats(graph):
        """Print number of nodes and edges in the given graph"""
        #does (a,b) count as the same edge as (b,a)? if it does we will make a set of sets of connections.
        #Then count the lenth of the largest set
        nodes=0
        edges=0
        for key,values in graph.items():
            edges=edges+len(values)
            nodes=nodes+1
        print("there is "+str(nodes)+" nodes "+"and "+str(edges)+" edges")

def randomnodechooser(graph):
    RandomNodenumber = random.randint(0, int(len(graph.nodes)-1))
    node = list(graph.nodes)[RandomNodenumber]
    return node
def stochastic_page_rank(graph,node, n_iter=100000000000000000, n_steps=100):
    """Stochastic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    n_iter (int) -- number of random walks performed
    n_steps (int) -- number of followed links before random walk is stopped

    Returns:
    A dict that assigns each page its hit frequency

    This function estimates the Page Rank by counting how frequently
    a random walk that starts on a random node will after n_steps end
    on each node of the given graph.
    """
    Nodecount={}
    for i in range(0,n_iter):
        for x in range(0,n_steps):
            RandomNodenumber = random.randint(0, int(len(graph.edges(node)))-1)
            node = (list(graph.edges(node))[RandomNodenumber])[1]
        if node not in Nodecount:
            Nodecount[node]=(1/n_iter)
        else:
            Nodecount[node]=Nodecount[node]+(1/n_iter)
        node = randomnodechooser(graph)
    return Nodecount

    # if n_iter!=0:
    #     if n_steps!=0:
    #         RandomNodenumber = random.randint(0, int(len(graph.edges(node))))
    #         node = list(graph.edges(node))[RandomNodenumber]
    #         stochastic_page_rank(graph,node,n_iter,n_steps-1)
    #         print(node)
    #     else:
    #         node=randomnodechooser(graph)
    #         stochastic_page_rank(graph, node, n_iter-1, n_steps)


def distribution_page_rank(graph, n_iter=10):
    """Probabilistic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    n_iter (int) -- number of probability distribution updates

    Returns:
    A dict that assigns each page its probability to be reached

    This function estimates the Page Rank by iteratively calculating
    the probability that a random walker is currently on any node.
    """
    dict={}
    for z in range(0,len(list(graph.nodes))):
        dict[list(graph.nodes)[z]]=1/len(list(graph.nodes))
    for i in range(0,n_iter):
        next_prob={}
        for count in range(0,len(graph.nodes)):
            next_prob[list(graph.nodes)[count]] = 0
        for node in range(0,len((graph.nodes))):
            p=dict[list(graph.nodes)[node]]/len(graph.edges(list(graph.nodes)[node]))
            for edges in (0,len(graph.edges(list(graph.nodes)[node]))-1):
                next_prob[list(graph.edges(list(graph.nodes)[node]))[edges][1]]=next_prob[list(graph.edges(list(graph.nodes)[node]))[edges][1]]+p
        print("before",dict)
        dict=next_prob
        print("after",dict)
    return dict



def main():
    # Load the web structure from file
    web = load_graph(open(WEB_DATA))

    # print information about the website
    # The graph diameter is the length of the longest shortest path
    # between any two nodes. The number of random steps of walkers
    # should be a small multiple of the graph diameter.
    diameter = networkx.diameter(web)
    print(diameter)

    # #Measure how long it takes to estimate PageRank through random walks
    # print("Estimate PageRank through random walks:")
    # n_iter = len(web)**2
    # n_steps = 2*diameter
    # start = time.time()
    # node=randomnodechooser(web)
    # ranking = stochastic_page_rank(web,node, n_iter, n_steps)
    # Outputfile=open("pagerank.txt","w")
    # for Items in sorted(ranking,key=ranking.get,reverse=True):
    #     Outputfile.write(Items+" "+str(ranking[Items])+"\n")
    # stop = time.time()
    # time_stochastic = stop - start

    # Show top 20 pages with their page rank and time it took to compute
    # top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    # print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:20]))
    # print(f'Calculation took {time_stochastic:.2f} seconds.\n')

    # Measure how long it takes to estimate PageRank through probabilities
    print("Estimate PageRank through probability distributions:")
    n_iter = 2*diameter
    start = time.time()
    ranking = distribution_page_rank(web, n_iter)
    stop = time.time()
    time_probabilistic = stop - start

    # Show top 20 pages with their page rank and time it took to compute
    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:20]))
    print(f'Calculation took {time_probabilistic:.2f} seconds.\n')

    # Compare the compute time of the two methods
    #speedup = time_stochastic/time_probabilistic
    #print(f'The probabilitic method was {speedup:.0f} times faster.')


if __name__ == '__main__':
    main()

#graph = load_graph(open("school_web.txt"))
