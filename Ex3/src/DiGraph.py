from Node import Node
from GraphInterface import GraphInterface


class DiGraph(GraphInterface):
    mc = 0

    def __init__(self):
        self.graph = {}

    def increment(self, b) -> bool:
        self.mc = self.mc + 1 if b else self.mc
        return b

    def v_size(self) -> int:
        return len(self.graph)

    def e_size(self) -> int:
        ans = 0
        for node in self.graph.values():
            t=len(node.get_outside())
            ans += len(node.get_outside())
        return ans

    def get_all_v(self) -> dict:
        return self.graph

    def all_in_edges_of_node(self, id1: int) -> dict:
        if self.graph.get(id1):
            return self.graph[id1].get_inside()
        raise RuntimeError

    def all_out_edges_of_node(self, id1: int) -> dict:
        if self.graph.get(id1):
            return self.graph[id1].get_outside()
        raise RuntimeError

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if self.graph.get(id1) is None or self.graph.get(id2) is None:
            return False
        b = self.graph[id1].add_outside(id2, weight) and self.graph[id2].add_inside(id1, weight)
        return self.increment(b)

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if self.graph.get(node_id):
            return False
        self.graph[node_id] = Node(key=node_id, pos=pos)
        self.mc += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        b = self.graph[node_id1].remove_outside(node_id2) and self.graph[node_id2].remove_inside(node_id1)
        return self.increment(b)

    def remove_node(self, node_id: int) -> bool:
        if self.graph.get(node_id) is None:
            return False
        tmp = set()
        for i in self.all_in_edges_of_node(node_id).keys():
            tmp.add(i)
        for i in self.all_out_edges_of_node(node_id).keys():
            tmp.add(i)

        for i in tmp:
            self.remove_edge(node_id, i)
            self.remove_edge(i, node_id)

        del self.graph[node_id]
        self.mc += 1
        return True

    def get_node(self, node_id):
        return self.graph.get(node_id)

    def __str__(self) -> str:
        return self.graph.__str__()

    def __repr__(self) -> str:
        return self.graph.__str__()

    def as_dict(self) -> dict:
        tmp_dict = self.__dict__
        del tmp_dict["mc"]
        return tmp_dict
    #todo make equals function

if __name__ == '__main__':
    g = DiGraph()
    for i in range(6):
        g.add_node(i)
    g.add_edge(1, 2, 10)
    g.add_edge(1, 1, 10)
    g.add_edge(2, 2, 10)
    g.add_edge(1, 3, 10)
    g.add_edge(2, 4, 10)
    g.add_edge(2, 3, 10)
    g.add_edge(4, 5, 10)
    g.add_edge(5, 1, 10)
    g.add_edge(5, 4, 10)
    print(g.get_mc(), 13)
    print(g)
    print(g.remove_edge(5, 1), "true")
    print(g.remove_edge(5, 1), "false")
    print(g.get_mc())
    print(g.remove_node(2), "true")
    print(g.remove_node(2), "false")
    print(g.get_mc(), 18)
    print(g.remove_node(1), "false")
    print(g.get_mc(), 22)
    print(g)
    print(g.remove_edge(3, 1), "false")
    print(g)
    print(g.all_out_edges_of_node(4))
    print(g.all_in_edges_of_node(3))
    print(g.get_all_v())

