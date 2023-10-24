import csv

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


class GraphTopologyReader:
    """Reads the topology from the files nodes.csv and edges.csv."""

    @staticmethod
    def create_graph():
        """Function to create a graph out of the information provided in the topology files."""
        graph = nx.Graph()
        with open("./nodes.csv", 'r') as file:
            csvreader = csv.reader(file, delimiter=',', skipinitialspace=True)
            next(csvreader)
            for row in csvreader:
                name, node_type, x_pos, y_pos, host, memory, region = row
                pos = (int(x_pos), int(y_pos))
                graph.add_node(str(name), node_type=node_type, pos=pos, host=host, memory=memory, region=region)
        with open("./edges.csv", 'r') as file:
            csvreader = csv.reader(file, delimiter=',', skipinitialspace=True)
            next(csvreader)
            for row in csvreader:
                node1, node2, latency, bw = row
                graph.add_edge(str(node1), str(node2), latency=float(latency), bw=float(bw))
        return graph


class GraphTopology:
    """Stores the topology of the network in a graph-based format."""

    def __init__(self, graph_provider=GraphTopologyReader()):
        self.network_graph = graph_provider.create_graph()
        self.storages = self.get_network_nodes_by_node_type('storage')  # Storage node IDs
        self.aps = self.get_network_nodes_by_node_type('ap')  # Access points
        self.storage_ap_latencies = None
        self.storage_ap_bandwidths = None
        self.storage_latencies = None
        self.storage_bandwidths = None
        self._init_latency_and_bw()

    def get_ap_to_storage_latency(self, from_ap, to_storage):
        return self.storage_ap_latencies[self.storages.index(to_storage)][self.aps.index(from_ap)]

    def get_storage_latency(self, from_storage, to_storage):
        return self.storage_latencies[self.storages.index(from_storage)][self.storages.index(to_storage)]

    def get_node_attribute(self, node, attribute):
        return self.network_graph.nodes[node][attribute]

    def get_network_nodes_by_node_type(self, node_type):
        return [node for node in self.network_graph.nodes if self.network_graph.nodes[node]['node_type'] == node_type]

    def _init_latency_and_bw(self):
        self.storage_ap_latencies = np.zeros((len(self.storages), len(self.aps)))
        self.storage_ap_bandwidths = np.zeros((len(self.storages), len(self.aps)))
        for i, storage in enumerate(self.storages):
            for j, ap in enumerate(self.aps):
                shortest = nx.dijkstra_path(self.network_graph, ap, storage)
                self.storage_ap_latencies[i][j] = nx.path_weight(self.network_graph, shortest, "latency")
                self.storage_ap_bandwidths[i][j] = nx.path_weight(self.network_graph, shortest, "bw")
        self.storage_latencies = np.zeros((len(self.storages), len(self.storages)))
        self.storage_bandwidths = np.zeros((len(self.storages), len(self.storages)))
        for i, storage1 in enumerate(self.storages):
            for j, storage2 in enumerate(self.storages):
                shortest = nx.dijkstra_path(self.network_graph, storage1, storage2)
                self.storage_latencies[i][j] = nx.path_weight(self.network_graph, shortest, "latency")
                self.storage_bandwidths[i][j] = nx.path_weight(self.network_graph, shortest, "bw")

    def plot_graph(self, save=False):
        """Plot the network graph with edges."""
        plt.subplots()
        plt.xlabel("X-position of storage and ap nodes")
        plt.ylabel("Y-position")
        plt.grid(False)
        pos = nx.get_node_attributes(self.network_graph, 'pos')
        nx.draw_networkx_nodes(self.network_graph, pos, node_size=500, node_color='lightgray')
        nx.draw_networkx_labels(self.network_graph, pos, font_color='black')
        nx.draw_networkx_edges(self.network_graph, pos,
                               edgelist=self.network_graph.edges(), edge_color='blue', width=2, alpha=0.5)
        nx.draw_networkx_edge_labels(self.network_graph, pos, edge_labels=self.network_graph.edges(), font_size=6)
        if save:
            plt.savefig("graph.png", dpi=400)
        plt.show()
