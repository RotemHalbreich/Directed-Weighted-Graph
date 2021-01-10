import unittest
from unittest import TestCase
from Ex3.src.Node import Node
from Ex3.src.DiGraph import DiGraph
from Ex3.src.GraphAlgo import GraphAlgo


class TestGraphAlgo(TestCase):
    def setUp(self) -> None:
        self.complex_graph = GraphAlgo()
        for i in range(1, 7):
            self.complex_graph.get_graph().add_node(i)
            self.complex_graph.get_graph().add_edge(i - 1, i, i * 10)

        self.complex_graph.get_graph().add_edge(1, 0, 1)
        self.complex_graph.get_graph().add_edge(3, 1, 1)
        self.complex_graph.get_graph().add_edge(5, 3, 1)

    def test_get_graph(self):
        graph = DiGraph()
        for i in range(1, 7):
            graph.add_node(i)
            graph.add_edge(i - 1, i, i * 10)

        graph.add_edge(1, 0, 1)
        graph.add_edge(3, 1, 1)
        graph.add_edge(5, 3, 1)
        self.assertEqual(self.complex_graph,graph)

    def test_save_to_json_and_load_from_json(self):
        # g = GraphAlgo(self.complex_graph)
        self.complex_graph.save_to_json("../data/text.json")
        g = GraphAlgo()
        g.load_from_json("../data/text.json")

    def test_shortest_path(self):
        pass

    def test_connected_component(self):
        pass

    def test_connected_components(self):
        pass

    def test_plot_graph(self):
        pass


if __name__ == '__main__':
    unittest.main()
