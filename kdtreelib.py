from typing import *
from math import sqrt
from functools import reduce

class KDValueMapping:
    def __init__(self, point: Tuple[int, ...], value: any):
        self.point = point
        self.value = value

class KDNode:
    def __init__(self, value: KDValueMapping, left: 'KDNode', right: 'KDNode'):
        self.value_mapping = value
        self.right = right
        self.left = left

class KDTree:
    def __init__(self, num_dimensions: int, point_list: List[KDValueMapping]):
        self.num_dimensions = num_dimensions
        self.root = self._build_tree(point_list)

    def _build_tree(self, point_list: List[KDValueMapping], depth: int=0) -> KDNode:
        if not point_list:
            return None

        axis = depth % self.num_dimensions
        point_list.sort(key=lambda x: x.point[axis])

        median = len(point_list) // 2
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

    def find_nearest_neighbor(self, search_node: Tuple[int, ...]):
        return self._find_nearest_neighbor(search_node, self.root, 0)

    def _find_nearest_neighbor(self, search_node: Tuple[int, ...], root: KDNode, depth: int) -> any:
        """
        Finds the nearest neighbor to the given node in the balanced tree
        """
        if root.left is None and root.right is None:
            return root.value_mapping

        axis = depth % self.num_dimensions
        if root.left is not None:
            if root.left.value_mapping.point[axis] < search_node[axis]:
                return self._find_nearest_neighbor(search_node, root.left, depth + 1)

        if root.right is not None:
            if root.right.value_mapping.point[axis] <= search_node[axis]:
                return self._find_nearest_neighbor(search_node, root.right, depth + 1)

        return root.value_mapping
