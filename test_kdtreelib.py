import unittest
from testing_dictionary import color_dictionary
from kdtreelib import KDNode, KDTree, KDValueMapping

class TestKDTree(unittest.TestCase):
    def test_red_emoji_finder(self):
        value_mappings: List[KDValueMapping] = []
        for i in color_dictionary.keys():
            value_mappings.append(KDValueMapping(point=i, value=color_dictionary[i]))

        tree = KDTree(num_dimensions=3, point_list=value_mappings)
        self.assertEqual(tree.find_nearest_neighbor((133, 118, 74)).value, ':older_woman:')

if __name__ == "__main__":
    unittest.main()