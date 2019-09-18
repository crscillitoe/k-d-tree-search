from typing import *
from math import sqrt
from functools import reduce

class IncorrectDimensionsError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class KDValueMapping:
    def __init__(self, point: Tuple[int, ...], value: any):
        self.point = point
        self.value = value
    
    def __repr__(self):
        return f"<{self.point}, {self.value}>"

class KDNode:
    def __init__(self, value: KDValueMapping, left: 'KDNode', right: 'KDNode'):
        self.value_mapping = value
        self.right = right
        self.left = left

    def __repr__(self):
        return self.value_mapping.__repr__()

class KDTree:
    def __init__(self, num_dimensions: int, point_list: List[KDValueMapping]):
        self.num_dimensions = num_dimensions
        self.tree_size = 0
        self.root = self._build_tree(point_list)

    def _build_tree(self, point_list: List[KDValueMapping], depth: int=0) -> KDNode:
        if not point_list:
            return None

        axis = depth % self.num_dimensions
        point_list.sort(key=lambda x: x.point[axis])

        median = len(point_list) // 2
        self.tree_size += 1
        return KDNode(
            value=point_list[median],
            left=self._build_tree(point_list[:median], depth + 1),
            right=self._build_tree(point_list[median + 1:], depth + 1)
        )

    def distance(self, node_1: Tuple[int, ...], node_2: Tuple[int, ...]) -> int:
        """
        Computes the distance between the two given tuples
        """
        distances = []
        for i in range(self.num_dimensions):
            distances.append((node_1[i] - node_2[i])**2)
        return sqrt(reduce(lambda x,y: x + y, distances))

    def find_nearest_neighbor(self, search_node: Tuple[int, ...]) -> KDValueMapping:
        if len(search_node) != self.num_dimensions:
            raise IncorrectDimensionsError(f"Expected {self.num_dimensions} dimensions, received {len(search_node)}")
        return self._find_nearest_neighbor(search_node, self.root, 0).value_mapping

    def _find_nearest_neighbor(self, search_node: Tuple[int, ...], root: KDNode, depth: int) -> KDNode:
        """
        Finds the nearest neighbor to the given node in the balanced tree
        """
        if root.left is None and root.right is None:
            return root

        if root.value_mapping.point == search_node:
            return root

        bottom_node = root
        axis = depth % self.num_dimensions
        root_point = root.value_mapping.point

        if root.left is not None and  search_node[axis]<= root_point[axis]:
            bottom_node = self._find_nearest_neighbor(search_node, root.left, depth + 1)
        elif root.right is not None and search_node[axis] > root_point[axis]:
            bottom_node = self._find_nearest_neighbor(search_node, root.right, depth + 1)

        return (bottom_node if self.distance(bottom_node.value_mapping.point, search_node) <
                               self.distance(root.value_mapping.point, search_node)
                else root)