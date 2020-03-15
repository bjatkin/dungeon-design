import numpy as np
import networkx as nx
from networkx.algorithms import isomorphism

class SubgraphFinder:
    @staticmethod
    def get_subgraph_mapping(bigger_graph, smaller_graph):
        graphs = []
        for graph_nodes in [bigger_graph, smaller_graph]:
            graph = nx.Graph()
            graph.clear()
            graph.add_nodes_from(graph_nodes)
            graph.add_edges_from(SubgraphFinder.get_edges(graph_nodes))
            graphs.append(graph)
        
        graph_matcher = isomorphism.GraphMatcher(graphs[0], graphs[1])
        is_subgraph = graph_matcher.subgraph_is_monomorphic()
        if is_subgraph:
            # Switch keys and values to map from smaller_graph to bigger_graph
            return { y:x for x,y in graph_matcher.mapping.items() }
        else:
            return None

    @staticmethod
    def get_edges(graph_nodes):
        edges = []
        for graph_node in graph_nodes:
            edges.extend([ ( graph_node, adjacent_node ) for adjacent_node in graph_node.adjacent_nodes])
        return edges


