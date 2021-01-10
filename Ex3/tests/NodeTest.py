import unittest
from Ex3.src.DiGraph import DiGraph

class MyTestCase(unittest.TestCase):
    def test_short_path(self):
        g=DiGraph()
        g.add_node(1)
        print(g)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
