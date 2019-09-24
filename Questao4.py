###########################################################
## CTC-34: Autômata e Linguagens Formais                 ##
## Prof. Forster                                         ##
##                                                       ##
## Equipe:                                               ##
##   Arthur Fernandes de Morais                          ##
##   Gianluigi Dal Toso                                  ##
##   Lucas Alberto Bilobran Lema                         ##
##                                                       ##
###########################################################

from graphviz import Digraph
import networkx as nx
import lightgbm as lgbm
import pydotplus

# Carrega o grafo e-AFN num objeto networkx graph
pydot_graph = pydotplus.graph_from_dot_file("teste1.dot")
NG = nx.nx_pydot.from_pydot(pydot_graph)

def isThereSelfEdges(node, edges):
    s = ''
    x = 0
    for edge in edges:
        if (node, node) == edge:
            a = NG[node][node][x]['label']
            x = x+1
            a = a.replace('"', '')
            if s:
                if a != "&":
                    s = s + "+" + a
            else:
                s = a
        
    if s:
        s = '{' + s + '}*'

    return s

def getPredecessors(node, allEdges):
    l = []
    for edge in allEdges:
        if node == edge[1]:
            if edge[0] not in l:
                l = l + [edge[0]]
    
    return l

def getSucessors(node, allEdges):
    l = []
    for edge in allEdges:
        if node == edge[0]:
            if edge[1] not in l and edge[1] != node:
                l = l + [edge[1]]
    
    return l

def uniteEdges(node1, node2):
    label = ''
    y = 0
    for edge in list(NG.edges):
        if node1==edge[0] and node2==edge[1]:
            x = edge[2]
            if not label:
                if NG[node1][node2][x]['label'] != '"&"':
                    label = NG[node1][node2][x]['label']
            else:
                y = 1
                if NG[node1][node2][x]['label'] != '"&"':
                    label = label + '+' + NG[node1][node2][x]['label']
    
    if label:
        # Remove
        for edge in list(NG.edges):
            if node1==edge[0] and node2==edge[1]:
                NG.remove_edge(node1, node2)
        # Adiciona com nova label
        if y != 0:
            label = '(' + label + ')'
        NG.add_edge(node1, node2, label=label)
    
    if label == '"&"':
        return ""

    return label


for node in list(NG.nodes):
    # Apenas os nós diferentes do final (S1) e inicial (S0) 
    if ( node!='S0' and node!='S1'):
        edges = list( NG.edges(node) )
        # Identifica se ha aresta apontando para o proprio node
        middle = isThereSelfEdges(node, edges)

        # Para cada aresta que chega de a e cada aresta que sai de node
        # e vai para p, adiciona uma aresta de a a p com a label:
        # label(a, node) + middle + label(node, p)
        predecessors = getPredecessors(node, list(NG.edges) )
        sucessors = getSucessors(node, list(NG.edges) )

        for p in predecessors:
            for s in sucessors:
                # simplifica multiplas arestas de p em node e de
                # node em s
                labelOne = uniteEdges(p, node)

                labelTwo = uniteEdges(node, s)

                # adiciona aresta de p em s com o middle
                label = labelOne + middle + labelTwo
                NG.add_edge(p, s, label=label)

                # Unifica arestas entre antecessor e sucessor de node
                a = uniteEdges(p, s)
        
        NG.remove_node(node)


# Verifica arestas voltando pro estado inicial
node = 'S0'
edges = list( NG.edges(node) )
# Identifica se ha aresta apontando para o proprio node
middle = isThereSelfEdges(node, edges)

# Se houver, substitui a aresta apontando para o estado final
if middle:
    lb = NG['S0']['S1'][0]['label']
    NG.remove_edge('S0', 'S1')
    label = middle + lb
    NG.add_edge('S0', 'S1', label=label)

print("Teste1")
print ("Expressao regular: " + NG['S0']['S1'][0]['label'])









