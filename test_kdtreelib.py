import unittest
from kdtreelib import KDNode, KDTree, KDValueMapping, IncorrectDimensionsError
from typing import *

class TestKDTree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.five_dimensional_dict: Dict[Tuple[int,...], str] = {
            (0,0,0,0,0): "N1",
            (1,1,1,1,1): "N2",
            (3,1,-2,4,5): "N3",
            (100,100,100,100,100): "N4",
            (-100,-100,-100,50,50): "N5",
            (-100,-100,-100,-50,-50): "N6"
        }
        return super().setUpClass()

    def _build_value_mappings(self, mapping_dictionary: Dict[Tuple[int, ...], str]):
        value_mappings: List[KDValueMapping] = []
        for i in mapping_dictionary.keys():
            value_mappings.append(KDValueMapping(point=i, value=mapping_dictionary[i]))

        return value_mappings

    def test_incorrect_number_of_dimensions(self):
        value_mappings = self._build_value_mappings(self.five_dimensional_dict)
        tree = KDTree(num_dimensions=5, point_list=value_mappings)
        with self.assertRaises(IncorrectDimensionsError):
            tree.find_nearest_neighbor((50,50,50,50))

    def test_reflexive_nearest_neighbor(self):
        value_mappings = self._build_value_mappings(self.five_dimensional_dict)
        tree = KDTree(num_dimensions=5, point_list=value_mappings)
        for point in self.five_dimensional_dict.keys():
            self.assertEqual(tree.find_nearest_neighbor(point).value, self.five_dimensional_dict[point])

    def test_five_dimensional_tree(self):
        value_mappings = self._build_value_mappings(self.five_dimensional_dict)
        tree = KDTree(num_dimensions=5, point_list=value_mappings)
        self.assertEqual(tree.find_nearest_neighbor((50, 50, 50, 50, 50)).value, "N3")

if __name__ == "__main__":
    unittest.main()