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
        Universe.reset()

    def test_load(self):
        self.fake_dic = {'colors': ['red', 'blue']}
        u = Universe()

        expected = {'positions': ['1', '2']}
        expected.update(self.fake_dic)

        self.assertEqual(u.dic, expected)
        self.assertEqual(u.permutations, [
            {'1', 'red'},
            {'2', 'red'},
            {'1', 'blue'},
            {'2', 'blue'}])

    def test_permute(self):
        self.fake_dic = {
            'colors': ['red', 'blue', 'white'],
            'pets': ['cat', 'dog', 'fish']}

        u = Universe()

        expected = {'positions': ['1', '2', '3']}
        expected.update(self.fake_dic)

        self.assertEqual(u.dic, expected)
        self.assertEqual(u.permutations, [
            {'red', 'cat'},
            {'dog', 'red'},
            {'red', 'fish'},
            {'cat', 'blue'},
            {'dog', 'blue'},
            {'blue', 'fish'},
            {'cat', 'white'},
            {'dog', 'white'},
            {'fish', 'white'},
            {'1', 'red'},
            {'red', '2'},
            {'3', 'red'},
            {'1', 'blue'},
            {'2', 'blue'},
            {'3', 'blue'},
            {'1', 'white'},
            {'2', 'white'},
            {'3', 'white'},
            {'1', 'cat'},
            {'2', 'cat'},
            {'3', 'cat'},
            {'dog', '1'},
            {'dog', '2'},
            {'dog', '3'},
            {'1', 'fish'},
            {'2', 'fish'},
            {'3', 'fish'}])

    def test_empty_universe(self):
        self.fake_dic = {}
        self.assertEqual(Universe().dic, {'positions': []})

    def test_broken_universe(self):
        self.fake_dic = {
            'color': ['red', 'blue', 'green'],
            'pets': ['cats', 'dogs']}

        with self.assertRaises(BrokenUniverseException):
            Universe()

    def test_single_element(self):
        self.fake_dic = {
            'colors': ['gold'],
            'pets': ['fish']}

        u = Universe()

        expected = {'positions': ['1']}
        expected.update(self.fake_dic)

        self.assertEqual(u.dic, expected)
        self.assertEqual(u.permutations, [
            {'fish', 'gold'},
            {'gold', '1'},
            {'fish', '1'}])


if __name__ == '__main__':
    unittest.main()
