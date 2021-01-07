import json
from random import uniform
from typing import List
from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
from GraphInterface import GraphInterface
from queue import PriorityQueue
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch


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
            s, w, d = edge.get("src"), edge.get("w"), edge.get("dest")
            self.graph.add_edge(id1=s, id2=d, weight=w)

    def init_my_graph_from_json(self, new_graph) -> None:
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
        for i in self.graph.get_all_v():
            node = self.graph.get_node(i)
            node.set_value(float('inf'))
            node.set_tag(self.unvisited)

    def seek_path(self, id1: int, id2: int, value=float) -> (float, list):
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
        @return: The distance of the path, a list of the nodes ids that the path goes through
        Notes:
        If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
        More info:
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
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
            if curr_node.get_key() is id2 or curr_node.get_value() is float('inf'):
                if curr_node.get_value is float('inf'):
                    return float('inf'), []
                return self.seek_path(id1, id2, curr_node.get_value())
            for i, w in curr_node.get_outside().items():
                weight = curr_node.get_value() + w
                ni = self.graph.get_node(i)
                if ni.get_tag() is self.unvisited and ni.get_value() > weight:
                    ni.set_value(weight)
                    queue.put(ni)
                    sorted(queue.queue)
                    ni.set_prev(curr_node)
                curr_node.set_tag(self.visited)
        return float('inf'), []

    def connected_component(self, id1: int) -> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        @param id1: The node id
        @return: The list of nodes in the SCC

        Notes:
        If the graph is None or id1 is not in the graph, the function should return an empty list []
        """
        if self.graph.get_node(id1) is None:
            return []
        if self.graph.v_size() == 1:
            return [id1]
        self.init_algorithm_graph()
        reverse_graph = self.sub_reverse_graph(id1)
        straight_list = self.direction(id1, self.graph)
        reverse_list = self.direction(id1, reverse_graph)
        return self.union(straight_list, reverse_list)

    def direction(self, id1: int, g: DiGraph) -> list:
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
        return list(set(straight) & set(reverse))

    def sub_reverse_graph(self, id1: int) -> DiGraph:
        d = deque()
        d.append(id1)
        reverse_graph = DiGraph()
        reverse_graph.add_node(id1)
        while len(d) != 0:
            curr_node = d.popleft()
            for ni in self.graph.all_out_edges_of_node(curr_node).keys():
                reverse_graph.add_node(ni)
                w = self.graph.get_node(curr_node).get_outside().get(ni)
                reverse_graph.add_edge(ni, curr_node, w)
                if self.graph.get_node(ni).get_tag() is self.unvisited:
                    d.append(ni)
                    self.graph.get_node(ni).set_tag(self.visited)
        self.init_algorithm_graph()
        return reverse_graph

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Component(SCC) in the graph.
        @return: The list all SCC

        Notes:
        If the graph is None the function should return an empty list []
        """
        if self.graph is None:
            return []
        scc, li = [], []
        for node in self.graph.get_all_v().keys():
            if node not in li:
                connected = self.connected_component(node)
                li.extend(connected)
                scc.append(connected)
        return scc

    def set_pos_for_all(self):
        for node in self.graph.get_all_v().keys():
            if self.graph.get_node(node).get_pos() is None:
                self.graph.get_node(node).set_pos((uniform(0.0, 100), uniform(0.0, 100)))
            else:
                break

    def plot_graph(self) -> None:
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
                con = ConnectionPatch(xyA, xyB, "data", "data", arrowstyle="-|>", shrinkA=5, shrinkB=5,mutation_scale=13, fc="r")
                ax.plot([xyA[0], xyB[0]], [xyA[1], xyB[1]], "o")
                ax.add_artist(con)

        ax.scatter(li_x, li_y)
        for i, txt in enumerate(n):
            ax.annotate(n[i], (li_x[i], li_y[i]))
        plt.show()

    # def plot_graph(self) -> None:
    #     """
    #     Plots the graph.
    #     If the nodes have a position, the nodes will be placed there.
    #     Otherwise, they will be placed in a random but elegant manner.
    #     @return: None
    #     """
    #     fig, ax = plt.subplots()
    #     s = set()
    #
    #     coordsA = "data"
    #     coordsB = "data"
    #     all_v = self.graph.get_all_v().keys()
    #     for node in all_v:
    #         vertex = self.graph.get_node(node)
    #         x, y = uniform(0.0, 100), uniform(0.0, 100)
    #         if vertex.get_pos():
    #             x, y = vertex.get_pos()
    #         else:
    #             vertex.set_pos((x, y))
    #         xyA = (x, y)
    #         for e in self.graph.all_out_edges_of_node(node).keys():
    #             vertex_e = self.graph.get_node(e)
    #             s.add(e)
    #             s.add(node)
    #             x1, y1 = uniform(0.0, 100), uniform(0.0, 100)
    #             if vertex_e.get_pos():
    #                 x1, y1 = vertex_e.get_pos()
    #             else:
    #                 vertex_e.set_pos((x1, y1))
    #             xyB = (x1, y1)
    #             con = ConnectionPatch(xyA, xyB, coordsA, coordsB,
    #                                   arrowstyle="<|-|>", shrinkA=5, shrinkB=5,
    #                                   mutation_scale=13, fc="r")
    #             ax.plot([xyA[0], xyB[0]], [xyA[1], xyB[1]], "o")
    #             ax.add_artist(con)
    #             xyB = 0
    #     for node in all_v:
    #         if node not in s:
    #             x, y = uniform(0.0, 100), uniform(0.0, 100)
    #             if vertex.get_pos():
    #                 x, y = vertex.get_pos()
    #             else:
    #                 vertex.set_pos((x, y))
    #             xyA = (x, y)
    #             xyB = (x, y)
    #             con = ConnectionPatch(xyA, xyB, coordsA, coordsB,
    #                                   arrowstyle="->", shrinkA=5, shrinkB=5,
    #                                   mutation_scale=20, fc="w")
    #             ax.plot([xyA[0], xyB[0]], [xyA[1], xyB[1]], "o")
    #             ax.add_artist(con)
    #     plt.xlabel("x coordinates")
    #     plt.ylabel("y coordinates")
    #     plt.title("My Graph")
    #     plt.show()

    def __str__(self) -> str:
        return self.graph.__str__()

    def __repr__(self) -> str:
        return self.graph.__str__()
    # todo make equals function


if __name__ == '__main__':
    g = GraphAlgo()
    for i in range(10):
        g.graph.add_node(i)
    for i in range(1, 10):
        g.graph.add_edge(i - 1, i, i)
        if i % 2 == 0:
            g.graph.add_edge(i, i - 1, i)
    g.graph.add_node(123)
    g.plot_graph()
    # print(g)
    # g.save_to_json("json_test.json")
    # g.load_from_json("json_test.json")
    g.load_from_json("../data/T0.json")
    g.plot_graph()
    g.save_to_json("json_test.json")
    print(g)
