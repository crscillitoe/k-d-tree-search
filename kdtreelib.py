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
        return self._find_nearest_neighbor(search_node, self.root)

    def _find_nearest_neighbor(self, search_node: Tuple[int, ...], root: KDNode) -> any:
        """
        Finds the nearest neighbor to the given node in the balanced tree
        """
        min_distance: int = self.distance(root.value_mapping.point, search_node)
        smallest_child = root

        for curr_node in [root.left, root.right]:
            breakpoint()
            if curr_node is None:
                continue

            child_distance: int = self.distance(curr_node.value_mapping.point, search_node)
            if child_distance < min_distance:
                smallest_child = curr_node
                min_distance = child_distance

        if smallest_child == root:
            return root.value_mapping

        return self._find_nearest_neighbor(search_node, smallest_child)