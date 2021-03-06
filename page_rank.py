import os
import time
from progress import Progress
import itertools
import networkx
import random
from progress import Progress
import matplotlib.pyplot as plt
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

def randomnodechooser(graph):#Randomly select a node
    RandomNodenumber = random.randint(0, int(len(graph.nodes)-1))
    node = list(graph.nodes)[RandomNodenumber]
    return node
def stochastic_page_rank(graph,node, n_iter=1000000, n_steps=100):
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
    #create an empty dictionary
    Nodecount={}
    prog = Progress(n_iter, "Permforming stochastic page rank. This may take while")#setting up progress bar
    for nodes in range(0,len(list(graph.nodes))):#loop through all the nodes
        Nodecount[list(graph.nodes)[nodes]]=0#set each node in the dictionary with a value of 0
    for i in range(0,n_iter):
        prog += 1#progress bar
        prog.show()
        node = randomnodechooser(graph)
        for x in range(0,n_steps):#loop for n amount of random links to follow per random node we start from
            RandomNodenumber = random.randint(0, int(len(graph.edges(node)))-1)#seelect a random number
            # use random number to select a random index in the list of edges from the randomnode
            node = (list(graph.edges(node))[RandomNodenumber])[1]
        Nodecount[node]+=(1/n_iter)#Increase the finnally landed node by 1/n iter.
        ## The most common will be largest
    prog.finish()
    return Nodecount

def distribution_page_rank(graph, n_iter=100):
    """Probabilistic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    n_iter (int) -- number of probability distribution updates

    Returns:
    A dict that assigns each page its probability to be reached

    This function estimates the Page Rank by iteratively calculating
    the probability that a random walker is currently on any node.
    """
    node_prob={}#create an empty dictionary
    prog = Progress(n_iter, "Permforming distribution page rank. This may take while")#set up progress bar
    for z in range(0,len(list(graph.nodes))):#loop through each node
        # set each node in the dictionary with an equal value with 1/n amount of nodes
        node_prob[list(graph.nodes)[z]]=1/len(list(graph.nodes))
    for i in range(0,n_iter):#loop n times
        prog += 1#progress bar
        prog.show()
        next_prob={}#second dictionary
        for count in range(0,len(graph.nodes)):#set the second dictionary to all have default values of 0
            next_prob[list(graph.nodes)[count]] = 0
        for node in range(0,len((graph.nodes))):#for each node in the graph
            Currentnode=list(graph.nodes)[node]
            # sets the probability to choose a node to 1/n the current nodes amount of edges
            p=node_prob[Currentnode]/len(graph.edges(Currentnode))
            for edges in range(0,len(graph.edges(Currentnode))):#All edges probabilities are increaseed by p
                CurrentEdges=list(graph.edges(Currentnode))
                next_prob[CurrentEdges[edges][1]]+=p
        node_prob=next_prob#this optimises the algorithim and refutes it being thrown off by random chance
    prog.finish()
    return node_prob



def main():
    """Main function to run other functions

    No Parameters:

    No Returned Values:

    This function handles calling both page ranks aswell as comparing the times to complete each of them
    """
    # Load the web structure from file
    web = load_graph(open(WEB_DATA))

    # print information about the website
    # The graph diameter is the length of the longest shortest path
    # between any two nodes. The number of random steps of walkers
    # should be a small multiple of the graph diameter.
    diameter = networkx.diameter(web)
    print(diameter)

    #Measure how long it takes to estimate PageRank through random walks
    print("Estimate PageRank through random walks:")
    n_iter = len(web)**2
    n_steps = 2*diameter
    start = time.time()
    node=randomnodechooser(web)
    ranking1 = stochastic_page_rank(web,node, n_iter, n_steps)
    print(sum(ranking1.values())*100)
    Outputfile=open("pagerank.txt","w")
    for Items in sorted(ranking1,key=ranking1.get,reverse=True):
        Outputfile.write(str(Items)+" "+str(ranking1[Items])+"\n")
    stop = time.time()
    time_stochastic = stop - start

    #Show top 20 pages with their page rank and time it took to compu te
    top = sorted(ranking1.items(), key=lambda item: item[1], reverse=True)
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:20]))
    print(f'Calculation took {time_stochastic:.2f} seconds.\n')
    #Measure how long it takes to estimate PageRank through probabilities
    print("Estimate PageRank through probability distributions:")
    n_iter = 2*diameter
    start = time.time()
    ranking2 = distribution_page_rank(web, n_iter)
    stop = time.time()
    time_probabilistic = stop - start
    if ranking1==ranking2:
        print("identical 20")
    # Show top 20 pages with their page rank and time it took to compute
    top = sorted(ranking2.items(), key=lambda item: item[1], reverse=True)
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:20]))
    print(f'Calculation took {time_probabilistic:.2f} seconds.\n')
    print(sum(ranking2.values())*100)
    # Compare the compute time of the two methods
    speedup = time_stochastic/time_probabilistic
    print(f'The probabilitic method was {speedup:.0f} times faster.')
    visual=networkx.draw_random(web,node_size=20)
    plt.figure(figsize=(20,20))
    plt.show()

if __name__ == '__main__':
    main()

#graph = load_graph(open("school_web.txt"))
