import unittest
from Node import Node


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
        node1 = Node(1)
        self.assertIsNotNone(node1)
        node1.add_inside(2, 13)
        node1.add_inside(3, 12)
        self.assertEqual(2, len(node1.get_inside()))
        node1.remove_inside(3)
        self.assertEqual(1, len(node1.get_inside()))
        node1.remove_inside(2)
        self.assertEqual(0, len(node1.get_inside()))

    def test_remove_outside(self):
        node1 = Node(1)
        self.assertIsNotNone(node1)
        node1.add_outside(5, 124)
        node1.add_outside(7, 12)
        self.assertEqual(2, len(node1.get_outside()))
        node1.remove_outside(35)
        self.assertEqual(2, len(node1.get_outside()))
        node1.remove_outside(7)
        self.assertEqual(1, len(node1.get_outside()))


if __name__ == '__main__':
    unittest.main()
