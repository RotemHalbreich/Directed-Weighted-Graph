import json
from random import uniform
from typing import List

from DiGraph import DiGraph
from GraphInterface import GraphInterface
from Node import Node


class GraphAlgo:
    def __init__(self):
        self.graph = DiGraph()

    def get_graph(self) -> GraphInterface:
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

    def init_my_graph_from_json(self, new_graph):
        self.__init__()
        g = new_graph.get("graph")
        for k, v in g.items():
            tmp = v.get("pos")
            x, y = float(tmp[0]), float(tmp[1])
            self.graph.add_node(node_id=int(k), pos=(x, y))
        for k, v in g.items():
            tmp = v.get("outside")
            for ni, w in tmp.items():
                self.graph.add_edge(id1=int(k), id2=int(ni), weight=w)

    def load_from_json(self, file_name: str) -> bool:
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
        try:
            with open(file_name, "w") as f:
                json.dump(self.graph, default=self.encoder, indent=4, fp=f)

        except IOError:
            return False
        return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        pass

    def connected_component(self, id1: int) -> list:
        pass

    def connected_components(self) -> List[list]:
        pass

    def plot_graph(self) -> None:
        pass

    def __str__(self) -> str:
        return self.graph.__str__()

    def __repr__(self) -> str:
        return self.graph.__str__()


if __name__ == '__main__':
    g = GraphAlgo()
    file = '../data/A5'
    g.load_from_json(file)
    g.save_to_json("json_test.json")
    g.load_from_json("json_test.json")

    print(g)
