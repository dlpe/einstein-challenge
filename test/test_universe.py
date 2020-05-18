import unittest
import mock

import json
from src.universe import Universe, BrokenUniverseException

class TestUniverse(unittest.TestCase):
    def setUp(self):
        self.fake_dic = {}
        f = mock.MagicMock()
        f.read = lambda: json.dumps(self.fake_dic)

        self.mock_open = mock.patch('src.universe.open', return_value=f)
        self.mock_open.start()
 
    def tearDown(self):
        self.mock_open.stop()

    def test_load(self):
        self.fake_dic = {'colors': ['red', 'blue']}
        u = Universe()

        self.assertEqual(u.dic, self.fake_dic)
        self.assertEqual(u.permutations, [])

    def test_permute(self):
        self.fake_dic = {
            'colors': ['red', 'blue', 'white'],
            'pets': ['cat', 'dog', 'fish']}

        u = Universe()

        self.assertEqual(u.dic, self.fake_dic)
        self.assertEqual(u.permutations, [
            {'cat', 'red'},
            {'red', 'dog'},
            {'red', 'fish'},
            {'blue', 'cat'},
            {'blue', 'dog'},
            {'fish', 'blue'},
            {'white', 'cat'},
            {'dog', 'white'},
            {'fish', 'white'}])

    def test_empty_universe(self):
        self.fake_dic = {}
        self.assertEqual(Universe().dic, self.fake_dic)

    def test_broken_universe(self):
        self.fake_dic = {
            'color': ['red', 'blue', 'green'],
            'pets': ['cats', 'dogs']}

        with self.assertRaises(BrokenUniverseException):
            Universe()


if __name__ == '__main__':
    unittest.main()
