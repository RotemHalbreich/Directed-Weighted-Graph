import json
from random import uniform
from typing import List
from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
from GraphInterface import GraphInterface
from queue import PriorityQueue


class GraphAlgo(GraphAlgoInterface):
    visited, unvisited, finish = 1, -1, 0

    def __init__(self, graph: DiGraph = DiGraph()):
        self.graph = graph

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
        #self.__init__()
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
    # g.graph.add_node(1)
    # g.graph.add_node(2)
    # g.graph.add_node(3)
    # g.graph.add_node(4)
    # g.graph.add_node(5)
    # g.graph.add_edge(1, 2, 10)
    # g.graph.add_edge(1, 3, 140)
    # g.graph.add_edge(2, 3, 10)
    # g.graph.add_edge(3, 4, 10)
    # print(g.shortest_path(4, 2))
    g.load_from_json("../data/A5")
    print(g)

