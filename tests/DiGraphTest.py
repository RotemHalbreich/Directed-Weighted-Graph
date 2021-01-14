import unittest
from Node import Node
from DiGraph import DiGraph


class DiGraphTest(unittest.TestCase):

    def test_v_size(self):
        g = DiGraph()
        self.assertEqual(g.v_size(), 0)
        for i in range(6):
            g.add_node(i)
        self.assertEqual(g.v_size(), 6)
        g.remove_node(0)
        self.assertEqual(g.v_size(), 5)
        g.remove_node(1)
        self.assertEqual(g.v_size(), 4)
        g.remove_node(2)
        self.assertEqual(g.v_size(), 3)

    def test_e_size(self):
        g = DiGraph()
        for i in range(6):
            g.add_node(i)
        g.add_edge(1, 2, 14)
        g.add_edge(2, 1, 12)
        g.add_edge(3, 1, 457)
        g.add_edge(2, 3, 15)
        g.add_edge(0, 5, 5)
        self.assertEqual(g.e_size(), 5)
        g.remove_edge(1, 2)
        self.assertEqual(g.e_size(), 4)
        g.add_edge(1, 2, 1000)
        g.add_edge(1, 2, 10010)
        self.assertEqual(g.e_size(), 5)

    def test_get_all_v(self):
        g = DiGraph()
        for i in range(10):
            g.add_node(i)
        all_nodes = g.get_all_v()
        self.assertEqual(len(all_nodes.values()), 10)

    def test_all_in_edges_of_node(self):
        g = DiGraph()
        g.add_node(0)
        for i in range(1, 10):
            g.add_node(i)
            g.add_edge(0, i, i * 2.0)
        g.add_edge(3, 0, 11)
        g.add_edge(4, 0, 12)
        g.add_edge(5, 0, 14)
        in_edges = g.all_in_edges_of_node(0)
        self.assertEqual(3,len(in_edges))
        g.remove_node(5)
        self.assertEqual(2,len(in_edges))
        g.remove_node(3)
        self.assertEqual(1,len(in_edges))
        g.remove_node(4)
        self.assertEqual(in_edges, {})

    def test_all_out_edges_of_node(self):
        g = DiGraph()
        g.add_node(0)
        for i in range(1, 10):
            g.add_node(i)
            g.add_edge(0, i, i * 2.0)
        out_edges = g.all_out_edges_of_node(0)
        self.assertEqual(len(out_edges.values()), 9)
        self.assertEqual(out_edges.get(5), 10)
        self.assertEqual(out_edges.get(3), 6)
        g.remove_node(0)
        self.assertEqual(out_edges, {})
        self.assertEqual(len(out_edges), 0)

    def test_get_mc(self):
        g = DiGraph()
        self.assertEqual(g.get_mc(), 0)
        g.add_node(0)
        self.assertEqual(g.get_mc(), 1)
        for i in range(1, 10):
            g.add_node(i)
            g.add_edge(0, i, i * 2.0)

        self.assertEqual(g.get_mc(), 19)
        g.remove_node(1)
        self.assertEqual(20,g.get_mc())
        for i in range(1, 10):
            g.remove_edge(0, i)
        self.assertEqual(g.get_mc(),28)


    def test_add_node(self):
        g = DiGraph()
        g.add_node(1)
        self.assertEqual(g.get_node(1), Node(1))

    def test_remove_node(self):
        g = DiGraph()
        self.assertEqual(g.v_size(), 0)
        for i in range(5):
            g.add_node(i)
        g.remove_node(0)
        self.assertEqual(g.v_size(), 4)
        g.add_edge(1, 2, 15)
        self.assertEqual(g.e_size(), 1)
        g.remove_node(1)
        self.assertEqual(g.e_size(), 0)

    def test_add_edge(self):
        g = DiGraph()
        g.add_node(0)
        for i in range(1, 10):
            g.add_node(i)
            g.add_edge(0, i, i * 2.0)
        self.assertEqual(len(g.all_out_edges_of_node(0)), 9)
        self.assertEqual(g.all_in_edges_of_node(0), {})

    def test_remove_edge(self):
        g = DiGraph()
        for i in range(5):
            g.add_node(i)
        g.add_edge(2, 3, 346)
        g.add_edge(2, 4, 34)
        self.assertEqual(g.all_out_edges_of_node(2).get(3), 346)
        self.assertEqual(g.all_in_edges_of_node(3).get(2), 346)
        g.remove_edge(2, 3)
        self.assertEqual(g.all_in_edges_of_node(3).get(2), None)
        self.assertEqual(g.all_out_edges_of_node(2).get(3), None)
        self.assertEqual(g.e_size(), 1)


if __name__ == '__main__':
    unittest.main()
