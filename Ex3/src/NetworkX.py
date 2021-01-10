import networkx as nx
import matplotlib.pyplot as plt
import json
import time


class NetworkX:

    def _init_(self):
        self.graph = nx.DiGraph()

    def read_from_json(self, json_file):
        new_graph = nx.DiGraph()
        for node in json_file.get("Nodes"):
            id = node.get("id")
            pos = None
            if node.get("pos") is not None:
                list_pos = node.get("pos").split(",")
                x = float(list_pos[0])
                y = float(list_pos[1])
                pos = (x, y)
            new_graph.add_node(id, pos=pos)
        for edge in json_file.get("Edges"):
            src = edge.get("src")
            dest = edge.get("dest")
            w = edge.get("w")
            new_graph.add_edge(src, dest, weight=w)
        return new_graph

    def read_json_networkx(self, json_file):
        new_graph = nx.DiGraph()
        for node in json_file.get("nodes"):
            id = node.get("id")
            pos = None
            if node.get("pos") is not None:
                list_pos = node.get("pos")
                x = float(list_pos[0])
                y = float(list_pos[1])
                pos = (x, y)
            new_graph.add_node(id, pos=pos)
        for edge in json_file.get("links"):
            src = edge.get("source")
            dest = edge.get("target")
            w = edge.get("weight")
            new_graph.add_edge(src, dest, weight=w)
        return new_graph

    def load_from_json(self, file_name: str) -> bool:
        try:
            with open(file_name, "r") as file:
                f = json.load(file)
            if f.get("Nodes"):
                new_graph = self.read_from_json(f)
            else:
                new_graph = self.read_json_networkx(f)

            self.graph = new_graph

        except IOError as e:
            print(e)
            return False
        return True

    def shortest_path(self, src: int, dest: int):
        return nx.shortest_path(self.graph, src, dest, weight='weight')

    def shortest_path_dist(self, src: int, dest: int):
        return nx.shortest_path_length(self.graph, src, dest, weight='weight')

    def connected_components(self):
        b = nx.strongly_connected_components(self.graph)
        c = []

        for i in b:
            c.append(i)
        return c

    def save_to_json(self, file) -> bool:
        try:
            with open(file, 'w') as f:
                f.write(json.dumps(nx.node_link_data(self.graph)))
            return True
        except IOError as e:
            print(e)
            return False


if __name__ == '__main__':
    print()
    g = NetworkX()
    print("####### NetworkX #######")
    print()

    print("<----------------------------------------------------------------------->")
    g.load_from_json("../data/G_10_80_0.json")
    s_all = time.time()
    start = time.time()
    print("NetworkX: \nGraph G_10_80_0 coordinates: (0,8)")
    print(f"Connected components {len(g.connected_components())} runtime {time.time() - start}")
    start = time.time()
    print("Shortest path route: ", g.shortest_path(0, 8))
    print("Shortest path distance: ", g.shortest_path_dist(0, 8))
    print(f"Shortest path runtime {time.time() - start} seconds")
    print("<----------------------------------------------------------------------->")

    g.load_from_json("../data/G_100_800_0.json")
    start = time.time()
    print("NetworkX: \nGraph G_100_800_0 coordinates: (12,95)")
    print(f"Connected components {len(g.connected_components())} runtime {time.time() - start}")
    start = time.time()
    print("Shortest path route: ", g.shortest_path(12, 95))
    print("Shortest path distance: ", g.shortest_path_dist(12, 95))
    print(f"Shortest path runtime {time.time() - start} seconds")
    print("<----------------------------------------------------------------------->")

    g.load_from_json("../data/G_1000_8000_0.json")
    start = time.time()
    print("NetworkX: \nGraph G_1000_8000_0 coordinates: (10,850)")
    print(f"Connected components {len(g.connected_components())} runtime {time.time() - start}")
    start = time.time()
    print("Shortest path route: ", g.shortest_path(10, 850))
    print("Shortest path distance: ", g.shortest_path_dist(10, 850))
    print(f"Shortest path runtime {time.time() - start} seconds")
    print("<----------------------------------------------------------------------->")

    g.load_from_json("../data/G_10000_80000_0.json")
    start = time.time()
    print("NetworkX: \nGraph G_10000_80000_0 coordinates: (0,9999)")
    print(f"Connected components {len(g.connected_components())} runtime {time.time() - start}")
    start = time.time()
    print("Shortest path route: ", g.shortest_path(0, 9999))
    print("Shortest path distance: ", g.shortest_path_dist(0, 9999))
    print(f"Shortest path runtime {time.time() - start} seconds")
    print("<----------------------------------------------------------------------->")

    g.load_from_json("../data/G_20000_160000_0.json")
    start = time.time()
    print("NetworkX: \nGraph G_20000_160000_0 coordinates: (0, 19999)")
    print(f"Connected components {len(g.connected_components())} runtime {time.time() - start}")
    start = time.time()
    print("Shortest path route: ", g.shortest_path(0, 19999))
    print("Shortest path distance: ", g.shortest_path_dist(0, 19999))
    print(f"Shortest path runtime {time.time() - start} seconds")
    print("<----------------------------------------------------------------------->")

    g.load_from_json("../data/G_30000_240000_0.json")
    start = time.time()
    print("NetworkX: \nGraph G_30000_240000_0 coordinates: (0, 5000)")
    print(f"Connected components {len(g.connected_components())} runtime {time.time() - start}")
    start = time.time()
    print("Shortest path route: ", g.shortest_path(0, 5000))
    print("Shortest path distance: ", g.shortest_path_dist(0, 5000))
    print(f"Shortest path runtime {time.time() - start} seconds")
    print()
    print(f"Total time: {time.time() - s_all} seconds")
    print("<----------------------------------------------------------------------->")
