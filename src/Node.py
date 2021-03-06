class Node:
    """This class represents the vertices of a graph"""

    def __init__(self, key: int, tag: int = -1, value: float = 0, pos: tuple = None):
        self.key = key
        self.tag = tag
        self.value = value
        self.pos = pos
        self.inside = {}
        self.outside = {}
        self.prev = None

    def add_inside(self, node_id: int, weight: float) -> bool:
        """
        Adds an inside vertex
        @param: node_id
        @param: float - weight
        @return: bool
        """
        if self.key is node_id:
            return False
        if self.inside.get(node_id):
            if self.inside.get(node_id) != weight:
                self.inside[node_id] = weight
                return True
            return False
        self.inside.setdefault(node_id, weight)
        return True

    def add_outside(self, node_id: int, weight: float) -> bool:
        """
        Adds an outside vertex
        @param: node_id
        @param: float - weight
        @return: bool
        """
        if self.key is node_id:
            return False
        if self.outside.get(node_id):
            if self.outside.get(node_id) != weight:
                self.outside[node_id] = weight
                return True
            return False
        self.outside.setdefault(node_id, weight)
        return True

    def remove_inside(self, node_id: int) -> bool:
        """
        Deletes an inside vertex
        @return: bool
        """
        if self.inside.get(node_id):
            del self.inside[node_id]
            return True
        return False

    def remove_outside(self, node_id: int) -> bool:
        """
        Deletes an outside vertex
        @return: bool
        """
        if self.outside.get(node_id):
            del self.outside[node_id]
            return True
        return False

    def get_outside(self) -> dict:
        """
        Returns a dictionary of the vertices connected to a specific vertex from outside direction
        @return: dict
        """
        return self.outside

    def get_inside(self) -> dict:
        """
        Returns a dictionary of the vertices connected to a specific vertex from inside direction
        @return: dict
        """
        return self.inside

    def set_value(self, v) -> None:
        """
        Sets the value
        """
        self.value = v

    def get_value(self) -> float:
        """
        Gets the value
        @return: float
        """
        return self.value

    def set_tag(self, t) -> None:
        """
        Sets the tag of a vertex
        """
        self.tag = t

    def get_tag(self) -> int:
        """
        Gets the tag of a vertex
        @return: int
        """
        return self.tag

    def get_key(self) -> int:
        """
        Gets the vertex ID
        @return: int
        """
        return self.key

    def set_prev(self, p) -> None:
        """
        Sets the previous vertex
        """
        self.prev = p

    def get_prev(self):
        """
        Gets the previous vertex
        """
        return self.prev

    def get_pos(self) -> tuple:
        """
        Gets the position of a vertex
        @param: tuple
        """
        return self.pos

    def set_pos(self, p: tuple) -> None:
        """
        Sets the position of a vertex
        @param: tuple
        """
        self.pos = p

    def __str__(self) -> str:
        """
        Returns the vertex as a String.
        @return: str
        """
        return f"key:{self.key},inside:{self.get_inside()},outside:{self.get_outside()}"

    def __repr__(self) -> str:
        """
        Returns the vertex as a String.
        @return: str
        """
        return f"key:{self.key},pos:{self.pos},inside:{self.get_inside()},outside:{self.get_outside()}"

    def __eq__(self, other) -> bool:
        """
        Checks if equals
        """
        return other.key == self.key and other.pos == self.pos

    def __lt__(self, other):
        """
        Comparator
        """
        return self.value < other.value

    def as_dict(self) -> dict:
        """
        Returns the vertices as dictionary
        @return dict
        """
        tmp_dict = self.__dict__
        return tmp_dict

    def __eq__(self, other):
        """
        Checks if two vertices are equal
        """
        return self.key == other.key \
               and self.get_inside() == other.get_inside() \
               and self.get_outside() == other.get_outside()


if __name__ == '__main__':
    n = Node(1, pos=(2, 3))
    n1 = Node(1, pos=(2, 3))

    print(n.add_outside(2, 2.5))
    print(n.add_outside(22, 2.5))
    print(n.add_inside(22, 2.52))
    print(n1.add_outside(2, 2.5))
    print(n1.add_outside(22, 2.5))
    print(n1.add_inside(22, 2.52))
    print(n)
    print(n == n1, "ll")
    print(len(n.outside))
    print(n.remove_inside(22))
    print(n.remove_inside(22))
    print(n.remove_outside(2))
    print(n.remove_outside(2))
    print(n)
