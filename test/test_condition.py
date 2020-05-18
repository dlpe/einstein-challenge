import unittest
import mock
import json

from src.condition import Condition, InvalidMember
from src.universe import Universe

class TestCondition(unittest.TestCase):
    def setUp(self):
        self.fake_dic = {}
        f = mock.MagicMock()
        f.read = lambda: json.dumps(self.fake_dic)

        self.mock_open = mock.patch('src.universe.open', return_value=f)
        self.mock_open.start()

    def tearDown(self):
        self.mock_open.stop()

    def test_link(self):
        self.fake_dic = {
            'colors': ['yellow', 'blue'],
            'pets': ['cats', 'dogs']}

        self.assertTrue(Condition('dogs yellow'))
        self.assertEqual(Universe.instance().permutations, [
            {'yellow', 'dogs'},
            {'blue', 'cats'}
        ])

    def test_inexistent(self):
        self.fake_dic = {
            'colors': ['yellow', 'blue'],
            'pets': ['cats', 'dogs']}

        with self.assertRaises(InvalidMember):
            Condition('fish yellow')

    def test_same_type_link(self):
        self.fake_dic = {
            'colors': ['yellow', 'blue'],
            'pets': ['cats', 'dogs']}

        with self.assertRaises(InvalidMember):
            Condition('blue yellow')



if __name__ == '__main__':
    unittest.main()
