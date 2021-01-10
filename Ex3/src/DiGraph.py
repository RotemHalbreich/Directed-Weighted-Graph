from GraphAlgoInterface import GraphAlgoInterface

from Node import Node
from GraphInterface import GraphInterface


class DiGraph(GraphInterface):
    """This abstract class represents an interface of a graph."""
    mc = 0

    def __init__(self):
        self.graph = {}

    def increment(self, b) -> bool:
        """
        Increments the mode count while needed
        @return: bool
        """
        self.mc = self.mc + 1 if b else self.mc
        return b

    def v_size(self) -> int:
        """
        Returns the number of vertices in this graph
        @return: int
        """
        return len(self.graph)

    def e_size(self) -> int:
        """
        Returns the number of edges in this graph
        @return: int
        """
        ans = 0
        for node in self.graph.values():
            ans += len(node.get_outside())
        return ans

    def get_all_v(self) -> dict:
        """
        Returns a dictionary of all the vertices in the graph, each vertex is represented using a pair
        (node_id, node_data)
        @return: dict
        """
        return self.graph

    def all_in_edges_of_node(self, id1: int) -> dict:
        """
        Returns a dictionary of all the vertices connected into -> (node_id),
        each node is represented using a pair (other_node_id, weight)
        @return: dict
        """
        if self.graph.get(id1):
            return self.graph[id1].get_inside()
        raise RuntimeError

    def all_out_edges_of_node(self, id1: int) -> dict:
        """
        return a dictionary of all the vertices connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        if self.graph.get(id1):
            return self.graph[id1].get_outside()
        raise RuntimeError

    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        for every change in the graph state - the MC should be increased
        @return: int
        """
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.

        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """
        if self.graph.get(id1) is None or self.graph.get(id2) is None:
            return False
        b = self.graph[id1].add_outside(id2, weight) and self.graph[id2].add_inside(id1, weight)
        return self.increment(b)

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.

        Note: if the node id already exists the node will not be added
        """
        if self.graph.get(node_id):
            return False
        self.graph[node_id] = Node(key=node_id, pos=pos)
        self.mc += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.

        Note: If such an edge does not exists the function will do nothing
        """
        b = self.graph[node_id1].remove_outside(node_id2) and self.graph[node_id2].remove_inside(node_id1)
        return self.increment(b)

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.

        Note: if the node id does not exists the function will do nothing
        """
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
        """
        Get a vertex by ID
        @param node_id: The node ID
        """
        return self.graph.get(node_id)

    def __str__(self) -> str:
        return self.graph.__str__()

    def __repr__(self) -> str:
        return self.graph.__str__()

    def as_dict(self) -> dict:
        tmp_dict = self.__dict__

        try:
            del tmp_dict["mc"]
        except Exception as e:
            print(e)
        return tmp_dict

    def similar(self, g, g1):
        for n in g.get_all_v():
            if n not in g1.get_all_v():
                return False
            if g.get_node(n) != g1.get_node(n):
                return False
        return True

    def __eq__(self, other):
        if isinstance(other,GraphInterface):
            return self.similar(self, other) and self.similar(other, self)
        elif isinstance(other,GraphAlgoInterface):
            return self.similar(self, other.get_graph()) and self.similar(other.get_graph(), self)

if __name__ == '__main__':
    g = DiGraph()
    g1 = DiGraph()
    for i in range(6):
        g.add_node(i)
        g1.add_node(i)

    print(g == g1)
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
