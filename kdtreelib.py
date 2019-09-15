from typing import *
from math import sqrt
from functools import reduce

class KDValueMapping:
    def __init__(self, point, value):
        self.point = point
        self.value = value

class KDNode:
    def __init__(self, value: KDValueMapping, left: KDNode, right: KDNode):
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

    def distance(self, node_1: Tuple, node_2: Tuple) -> int:
        """
        Computes the distance between the two given tuples
        """
        distances = []
        for i in range(self.num_dimensions):
            distances.append((node_1[i] - node_2[i])**2)
        return sqrt(reduce(lambda x,y: x + y, distances))

    def find_nearest_neighbor(self, search_node: Tuple):
        return self._find_nearest_neighbor(search_node, self.root)

    def _find_nearest_neighbor(self, search_node: Tuple, root: KDNode) -> any:
        """
        Finds the nearest neighbor to the given node in the balanced tree
        """
        min_distance: int = self.distance(root.value_mapping.point, search_node)
        smallest_child = root

        left_distance = self.distance(root.left.value_mapping.point, search_node)
        right_distance = self.distance(root.right.value_mapping.point, search_node)
        for i in [root.left, root.right]:
            if i is None:
                continue

            child_distance: int = self.distance(i.value_mapping.point, search_node)
            if child_distance < min_distance:
                smallest_child = i
                min_distance = child_distance

        if smallest_child == root:
            return root.value_mapping

        return self.find_nearest_value(search_node, smallest_child)