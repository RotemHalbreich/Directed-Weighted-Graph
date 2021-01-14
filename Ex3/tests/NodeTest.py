import unittest
from Ex3.src.Node import Node
from Ex3.src.DiGraph import DiGraph


class MyTestCase(unittest.TestCase):

    def test_add_inside(self):
        node1 = Node(1)
        self.assertIsNotNone(node1)
        node1.add_inside(2, 13)
        node1.add_inside(3, 12)
        self.assertEqual(2, len(node1.get_inside()))
        node1.add_inside(124, 45687)
        node1.add_inside(124, 45687)
        node1.add_inside(124, 3)
        self.assertEqual(3, len(node1.get_inside()))


    def test_add_outside(self):
        node1 = Node(1)
        self.assertIsNotNone(node1)
        node1.add_outside(5, 124)
        node1.add_outside(7, 12)
        self.assertEqual(2, len(node1.get_outside()))
        node1.add_outside(35, 6)
        node1.add_outside(35, 235)
        self.assertEqual(3, len(node1.get_outside()))



    def test_remove_inside(self):
        pass

    def test_remove_outside(self):
        pass

    def test_get_outside(self):
        pass

    def test_get_inside(self):
        pass


if __name__ == '__main__':
    unittest.main()
