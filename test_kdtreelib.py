import unittest
from testing_dictionary import color_dictionary
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

    def test_exact_emoji(self):
        value_mappings: List[KDValueMapping] = []
        for i in color_dictionary.keys():
            value_mappings.append(KDValueMapping(point=i, value=color_dictionary[i]))

        tree = KDTree(num_dimensions=3, point_list=value_mappings)
        self.assertEqual(tree.tree_size, len(value_mappings))
        self.assertEqual(tree.find_nearest_neighbor((133, 118, 74)).value, ':older_woman:')

    def test_almost_exact_emoji(self):
        value_mappings: List[KDValueMapping] = []
        for i in color_dictionary.keys():
            value_mappings.append(KDValueMapping(point=i, value=color_dictionary[i]))

        tree = KDTree(num_dimensions=3, point_list=value_mappings)
        self.assertEqual(tree.tree_size, len(value_mappings))
        self.assertEqual(tree.find_nearest_neighbor((133, 118, 75)).value, ':older_woman:')

    def test_incorrect_number_of_dimensions(self):
        value_mappings: List[KDValueMapping] = []
        for i in self.five_dimensional_dict.keys():
            value_mappings.append(KDValueMapping(point=i, value=self.five_dimensional_dict[i]))
        tree = KDTree(num_dimensions=5, point_list=value_mappings)
        self.assertEqual(tree.tree_size, len(value_mappings))
        with self.assertRaises(IncorrectDimensionsError):
            tree.find_nearest_neighbor((50,50,50,50))

    def test_five_dimensional_tree(self):
        value_mappings: List[KDValueMapping] = []
        for i in self.five_dimensional_dict.keys():
            value_mappings.append(KDValueMapping(point=i, value=self.five_dimensional_dict[i]))
        tree = KDTree(num_dimensions=5, point_list=value_mappings)
        self.assertEqual(tree.tree_size, len(value_mappings))
        self.assertEqual(tree.find_nearest_neighbor((50, 50, 50, 50, 50)).value, "N3")

if __name__ == "__main__":
    unittest.main()