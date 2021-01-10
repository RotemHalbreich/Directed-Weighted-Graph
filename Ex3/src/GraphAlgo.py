import json
from random import uniform
from typing import List, Tuple
from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
from GraphInterface import GraphInterface
from queue import PriorityQueue
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import time


class GraphAlgo(GraphAlgoInterface):
    """This abstract class represents an interface of a graph."""

    visited, unvisited, finish = 1, -1, 0

    def __init__(self, graph: DiGraph = None):
        if graph:
            self.graph = graph
        else:
            self.graph = DiGraph()

    def get_graph(self) -> GraphInterface:
        """
        @return: the directed graph on which the algorithm works on.
        """
        return self.graph

    def init_json(self, new_graph: dict) -> None:
        """
        Initializes a new graph from Json format.
        @param: dict - a new graph
        """
        nodes = new_graph.get("Nodes")
        edges = new_graph.get("Edges")
        for node in nodes:
            k = node.get("id")
            x, y = uniform(0.0, 100), uniform(0.0, 100)
            if node.get("pos"):
                tmp = node.get("pos").split(",")
                x, y = float(tmp[0]), float(tmp[1])
            self.graph.add_node(node_id=k, pos=(x, y))
        for edge in edges:

            self.graph.add_edge(id1=edge.get("src"), id2=edge.get("dest"), weight=edge.get("w"))

    def init_my_graph_from_json(self, new_graph) -> None:
        """
        Initializes our graph from Json file.
        @return: None
        """
        g = new_graph.get("graph")
        for k, v in g.items():
            x, y = uniform(0.0, 100), uniform(0.0, 100)
            if v.get("pos"):
                tmp = v.get("pos")
                x, y = float(tmp[0]), float(tmp[1])
            self.graph.add_node(node_id=int(k), pos=(x, y))
        for k, v in g.items():
            tmp = v.get("outside")
            for ni, w in tmp.items():
                self.graph.add_edge(id1=int(k), id2=int(ni), weight=w)

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """
        self.__init__()
        try:
            with open(file_name, "r") as f:
                new_graph = json.load(f)
        except IOError:
            return False
        if new_graph.get("graph"):
            self.init_my_graph_from_json(new_graph)
        else:
            self.init_json(new_graph)

        return True

    def encoder(self, o):
        """
        Returns a dictionary
        """
        return o.as_dict()

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        try:
            with open(file_name, "w") as f:
                json.dump(self.graph, default=self.encoder, indent=4, fp=f)
        except IOError:
            return False
        return True

    def init_algorithm_graph(self):
        """
        Initializes the GraphAlgo
        """
        for i in self.graph.get_all_v():
            node = self.graph.get_node(i)
            node.set_value(float('inf'))
            node.set_tag(self.unvisited)
            node.set_prev(None)

    def seek_path(self, id1: int, id2: int, value=float) -> (float, list):
        """
        Returns the shortest path distance (as weight) and its route of vertices as a list
        @param: int - id1
        @param: int - id2
        @param: float - value
        @return: (float, list)
        """
        prev = self.graph.get_node(id2)
        path = [prev.get_key()]

        while prev.get_prev() is not None:
            prev = prev.get_prev()
            path.append(prev.get_key())
        path.reverse()
        return value, path

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the vertices IDs which the path goes through
                 If no such path, or one of them doesn't exist the function returns (float('inf'),[])
        """
        if self.graph.get_node(id1) is None or self.graph.get_node(id2) is None:
            return float('inf'), []
        if id1 is id2:
            return 0.0, [self.graph.get_node(id1)]

        self.init_algorithm_graph()
        self.graph.get_node(id1).set_value(0)
        queue = PriorityQueue()
        queue.put(self.graph.get_node(id1))
        while not queue.empty():
            curr_node = queue.get(0)
            if curr_node.get_key() == id2 or curr_node.get_value() == float('inf'):
                if curr_node.get_value is float('inf'):
                    return float('inf'), []
                return self.seek_path(id1, id2, curr_node.get_value())
            for i, w in curr_node.get_outside().items():
                weight = curr_node.get_value() + w
                ni = self.graph.get_node(i)
                if ni.get_tag() is self.unvisited and ni.get_value() > weight:
                    ni.set_value(weight)
                    queue.put(ni)
                    # sorted(queue.queue)
                    ni.set_prev(curr_node)
            curr_node.set_tag(self.visited)
        return float('inf'), []

    def connected_component(self, id1: int, reset: int = 0) -> list:
        """
        Finds the Strongly Connected Component (SCC) which node id1 is a part of.
        @param id1: The vertex id
        @param reset: int
        @return: The list of nodes in the SCC
                 If the graph is None or id1 is not in the graph, the function returns an empty list []
        """

        if self.graph.get_node(id1) is None:
            return []
        if self.graph.v_size() == 1:
            return [id1]
        if reset == 0:
            self.init_algorithm_graph()

        reverse_graph, straight_list = self.sub_graph(id1)
        # straight_list = self.direction(id1, self.graph)
        reverse_list = self.direction(id1, reverse_graph)

        return self.union(straight_list, reverse_list)

    def direction(self, id1: int, g: DiGraph) -> list:
        """
        Returns the list of the neighbors of a vertex
        @param: int: id1
        @param: DiGraph - a graph
        @return: list
        """
        d = deque()
        d.append(id1)
        li = [id1]
        while len(d) != 0:
            curr_node = d.popleft()
            for ni in g.all_out_edges_of_node(curr_node).keys():
                if g.get_node(ni).get_tag() is self.unvisited:
                    d.append(ni)
                    g.get_node(ni).set_tag(self.visited)
                    li.append(ni)
        return li

    def union(self, straight: list, reverse: list) -> list:
        """
        Returns a union of both lists straight & reverse as another list
        @return: list
        """
        return list(set(straight) & set(reverse))

    def sub_graph(self, id1: int) -> Tuple[DiGraph, List]:
        """
        Returns the graph reverse and the list of neighbors which you can get to from a vertex
        @param: int - id1
        @return: Tuple[DiGraph, List]
        """
        d = deque()
        d.append(id1)
        reverse_graph = DiGraph()
        reverse_graph.add_node(id1)
        li = [id1]
        while len(d) != 0:
            curr_node = d.popleft()
            for ni in self.graph.all_out_edges_of_node(curr_node).keys():
                reverse_graph.add_node(ni)
                w = self.graph.get_node(curr_node).get_outside().get(ni)
                reverse_graph.add_edge(ni, curr_node, w)
                if self.graph.get_node(ni).get_tag() is self.unvisited:
                    d.append(ni)
                    self.graph.get_node(ni).set_tag(self.visited)
                    li.append(ni)

        return reverse_graph, li

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Components (SCC) in the graph.
        @return: The list of all SCC
                 If the graph is None, the function returns an empty list []
        """
        if self.graph is None:
            return []
        scc = []
        s = set()
        for i, node in enumerate(self.graph.get_all_v().keys()):

            if node not in s:
                connected = self.connected_component(node, i)
                s.update(connected)
                scc.append(connected)

        return scc

    def set_pos_for_all(self):
        """
        Sets the position for every vertex in the graph randomly
        """
        for node in self.graph.get_all_v().keys():
            if self.graph.get_node(node).get_pos() is None:
                self.graph.get_node(node).set_pos((uniform(0.0, 100), uniform(0.0, 100)))
            else:
                break

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the vertices have a position, the vertices will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        fig, ax = plt.subplots()
        self.init_algorithm_graph()
        self.set_pos_for_all()
        li_x, li_y, n = [], [], []
        for node in self.graph.get_all_v().keys():
            xyA = self.graph.get_node(node).get_pos()
            x, y = self.graph.get_node(node).get_pos()
            li_x.append(x)
            li_y.append(y)
            n.append(node)
            for ni in self.graph.all_out_edges_of_node(node):
                xyB = self.graph.get_node(ni).get_pos()
                con = ConnectionPatch(xyA, xyB, "data", "data", arrowstyle="-|>", shrinkA=5, shrinkB=5,
                                      mutation_scale=13, fc="r")
                ax.plot([xyA[0], xyB[0]], [xyA[1], xyB[1]], "o")
                ax.add_artist(con)

        ax.scatter(li_x, li_y)
        for i, txt in enumerate(n):
            ax.annotate(n[i], (li_x[i], li_y[i]))
        plt.xlabel("x coordinates")
        plt.xlabel("x coordinates")
        plt.ylabel("y coordinates")
        plt.title("My Graph")
        plt.show()

    def __str__(self) -> str:
        """
        @return: Returns the graph as a String.
        """
        return self.graph.__str__()

    def __repr__(self) -> str:
        """
        @return: Returns the graph as a String.
        """
        return self.graph.__str__()

    def __eq__(self, other) -> bool:
        """
        Checks if two GraphAlgo are equals.
        @return: bool
        """
        if isinstance(other, GraphAlgo):
            return self.graph.__eq__(other.graph)
        elif isinstance(other, GraphInterface):
            return self.graph.__eq__(other)
        return False


if __name__ == '__main__':
    g = GraphAlgo()
    s_all = time.time()

    g.load_from_json("../data/G_10_80_0.json")
    start = time.time()
    print(g.shortest_path(0, 8))
    print(f"component 10 take {time.time() - start} second")
    start = time.time()
    # print(g.connected_component(0))
    # print(f"component 10 take {time.time() - start} second")
    #
    g.load_from_json("../data/G_100_800_0.json")

    # print( g.connected_component(10))
    print(g.shortest_path(12,95))
    print(f"component 100 take {time.time() - start} second")
    g.load_from_json("../data/G_1000_8000_0.json")
    start = time.time()
    # print(g.connected_components())

    print(g.shortest_path(10, 850))
    print(f"component 1000 take {time.time() - start} second")
    g.load_from_json("../data/G_10000_80000_0.json")
    start = time.time()
    print(g.shortest_path(0, 9999))
    # print(g.connected_components())
    print(f"component 10000 take {time.time() - start} second")
    g.load_from_json("../data/G_20000_160000_0.json")
    start = time.time()
    print(g.shortest_path(0, 19999))
    # g.connected_components()
    # print(f"component 20000 take {time.time() - start} second")
    g.load_from_json("../data/G_30000_240000_0.json")
    start = time.time()
    print(g.shortest_path(1000, 10000))
    # g.connected_components()
    print(f"component 30000 take {time.time() - start} second")
    # print(f"all component take {time.time() - s_all} second")


    print(f" sum of tests {(time.time() - s_all)} second")

    # g.graph.add_node(123)
    # g.save_to_json("json_test.json")
    # g.load_from_json("json_test.json")
    # g.load_from_json("../data/T0.json")
    # g.save_to_json("json_test.json")
    # # print(g)
    # # g.save_to_json("json_test.json")
    # # g.load_from_json("json_test.json")
    # g.load_from_json("../data/T0.json")
    # g.plot_graph()
    # g.save_to_json("json_test.json")
    # print(g)
