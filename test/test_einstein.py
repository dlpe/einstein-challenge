import unittest
import mock

import json
from src.einstein import Einstein, BrokenUniverseException

class TestEinstein(unittest.TestCase):
    def setUp(self):
        self.fake_universe = {}
        f = mock.MagicMock()
        f.read = lambda: json.dumps(self.fake_universe)

        self.mock_open = mock.patch('src.einstein.open', return_value=f)
        self.mock_open.start()
 
    def tearDown(self):
        self.mock_open.stop()

    def test_load_universe(self):
        self.fake_universe = {'colors': ['red', 'blue']}
        e = Einstein()

        self.assertEqual(e.universe, self.fake_universe)
        self.assertEqual(e.combinations, [])

    def test_combinations(self):
        self.fake_universe = {
            'colors': ['red', 'blue', 'white'],
            'pets': ['cat', 'dog', 'fish']}

        e = Einstein()

        self.assertEqual(e.universe, self.fake_universe)
        self.assertEqual(e.combinations, [
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
        self.fake_universe = {}
        self.assertEqual(Einstein().universe, self.fake_universe)

    def test_broken_universe(self):
        self.fake_universe = {
            'color': ['red', 'blue', 'green'],
            'pets': ['cats', 'dogs']}

        with self.assertRaises(BrokenUniverseException):
            Einstein()


if __name__ == '__main__':
    unittest.main()
