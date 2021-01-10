import unittest
from unittest import TestCase
from Ex3.src.DiGraph import DiGraph
from Ex3.src.GraphAlgo import GraphAlgo


class TestGraphAlgo(TestCase):

    def test_get_graph(self):
        g = DiGraph()
        for i in range(0, 7):
            g.add_node(i)
        graph_algo = GraphAlgo(g)
        self.assertEqual(graph_algo.get_graph(), g)

    # def test_load_from_json(self):
    #
    # def test_save_to_json(self):
    #
    # def test_shortest_path(self):
    #
    # def test_connected_component(self):
    #
    # def test_connected_components(self):
    #
    # def test_plot_graph(self):


if __name__ == '__main__':
    unittest.main()
